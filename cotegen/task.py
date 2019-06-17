import os

from .my_random import RandomGenerator
from .mutation import MutationGenerator
from .context import Status
from .kill import MutantKiller
from .test import TestSuite
from .exceptions import CotegenTaskConstraintError

from .ast_utils import print_ast

import time
import copy


class Task:
    num_test_tries = 10
    input_parameters = {}
    output_type = None
    constraints = []

    @classmethod
    def solve(cls, **kwargs):
        raise NotImplementedError

    @staticmethod
    def compare(user_answer, jury_answer) -> bool:
        return user_answer == jury_answer

    @classmethod
    def convert_input_parameters_to_test(cls, test) -> dict:
        return test

    @classmethod
    def check_input_constraint(cls, test) -> bool:
        return set(test.keys()) == set(cls.input_parameters.keys()) \
            and all(typ.is_valid(test[key], test) for key, typ in cls.input_parameters.items()) \
            and all(constraint.is_valid(test) for constraint in cls.constraints)

    @classmethod
    def generate_random_tests(cls):
        tests = RandomGenerator.generate_inputs(
            cls.input_parameters, cls.constraints, cls.num_test_tries)

        inputs = list(map(cls.convert_input_parameters_to_test,
                          filter(cls.check_input_constraint, tests)))

        return TestSuite(cls.solve, cls.compare, inputs)

    @classmethod
    def mutate(cls, test_suite):
        generator = MutationGenerator(cls.solve, cls.input_parameters)

        return generator.execute_mutations(test_suite)

    @classmethod
    def kill_survived_mutants(cls, mutation_fitness=False, verbose=False):
        survived = []

        test_suite = cls.generate_random_tests()
        mutations = cls.mutate(test_suite)

        for survivor in list(filter(lambda m: m.status ==
                                    Status.SURVIVED, mutations)):
            mutantKiller = MutantKiller(cls, survivor, test_suite)

            inputs = mutantKiller.generate_sbst_inputs()

            if mutation_fitness:
                inputs.extend(mutantKiller.generate_mutation_sbst_inputs())

            test_suite.add(mutantKiller.generate_new_test_suite(inputs))

            if verbose:
                print('*********')
                mutantKiller.mutated_function.print()

        return test_suite, mutations

    @staticmethod
    def convert_input_to_string(**kwargs) -> str:
        return str(kwargs)

    @staticmethod
    def convert_output_to_string(output) -> str:
        return str(output)

    @classmethod
    def generate_test_files(cls, target_directory=None, mutation_fitness=True):
        # TODO: show progressbar?
        if target_directory is None:
            target_directory = os.getcwd()

        target_directory = os.path.expanduser(target_directory)

        try:
            os.mkdir(target_directory)
        except FileExistsError:
            pass 

        target_directory = os.path.join(
            target_directory, "data%s" % int(time.time()))
        print(target_directory)

        try:
            os.mkdir(target_directory)
        except FileExistsError:
            pass

        test_suite = cls.generate_random_tests()
        test_suite_with_only_pure_sbst = copy.deepcopy(test_suite)
        tests = test_suite.tests[:]
        num_random_tests = len(tests)

        mutations = cls.mutate(test_suite)
        print_later_for_random = ('Only random -> Killed: {}, Survived: {}'.format(
            sum(m.status == Status.KILLED for m in mutations), sum(m.status == Status.SURVIVED for m in mutations)))
        print(print_later_for_random)

        for survivor in list(filter(lambda m: m.status ==
                                    Status.SURVIVED, mutations)):
            mutantKiller = MutantKiller(cls, survivor, test_suite)

            inputs = mutantKiller.generate_sbst_inputs()
            test_suite_with_only_pure_sbst.add(
                mutantKiller.generate_new_test_suite(inputs))

            inputs.extend(mutantKiller.generate_mutation_sbst_inputs())
            test_suite.add(mutantKiller.generate_new_test_suite(inputs))

            mutantKiller.mutated_function.print()

        killing_indices = set()
        killing_indices_sbst = set()
        mutants_killed = list(
            filter(lambda m: m.status == Status.KILLED, mutations))
        mutants_survived = []
        
        sbst_mutants_killed, sbst_mutants_survived = \
            mutants_killed[:], []
        
        for mutcnt, mutant in enumerate(filter(lambda m: m.status ==
                                               Status.SURVIVED, mutations)):
            print("start running %d (%s)" % (mutcnt, mutant))
            test_result, _, indices = test_suite.run(mutant.ast_node)

            print("end running %d (%s) -> %s" % (mutcnt, mutant, test_result))
            if test_result == 'SUCCESS':
                mutants_survived.append(mutant)
            elif test_result == 'FAIL':
                killing_indices = killing_indices | set(indices[:5])
                mutants_killed.append(mutant)

            test_sbst_result, _, indices_sbst = test_suite_with_only_pure_sbst.run(
                mutant.ast_node)
            if test_sbst_result == 'SUCCESS':
                sbst_mutants_survived.append(mutant)
            elif test_sbst_result == 'FAIL':
                killing_indices_sbst = killing_indices_sbst | set(indices_sbst[:3])
                sbst_mutants_killed.append(mutant)

        if mutation_fitness:
            tests.extend(test_suite.tests[i] for i in killing_indices)
        else:
            tests.extend(test_suite_with_only_pure_sbst.tests[i] for i in killing_indices_sbst)

        for idx, test in enumerate(tests):
            key = "random" if idx < num_random_tests else "sbst"
            with open(os.path.join(target_directory, "%s-%03d.in" % (key, idx)), "w") as f:
                f.write(cls.convert_input_to_string(**test[0]))
            with open(os.path.join(target_directory, "%s-%03d.out" % (key, idx)), "w") as f:
                f.write(cls.convert_output_to_string(test[1]))

        print("-------------")
        print(target_directory)
        print("Generated %d tests" % len(tests))
        print(print_later_for_random)
        print('SBST with branch fitness -> Killed: {}, Survived: {}'.format(
            len(sbst_mutants_killed), len(sbst_mutants_survived)))
        print('SBST with mutation fitness -> Killed: {}, Survived: {}'.format(
            len(mutants_killed), len(mutants_survived)))
