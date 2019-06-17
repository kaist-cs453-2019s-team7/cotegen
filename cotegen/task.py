import os

from .my_random import RandomGenerator
from .mutation import MutationGenerator
from .context import Status
from .kill import MutantKiller
from .test import TestSuite
from .exceptions import CotegenTaskConstraintError

from .ast_utils import print_ast


class Task:
    num_test_tries = 10
    input_parameters = {}
    output_type = None
    constraints = []

    @classmethod
    def solve(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def compare(cls, user_answer, jury_answer) -> bool:
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
        tests = RandomGenerator.generate_inputs(cls.input_parameters, cls.constraints, cls.num_test_tries)

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

    def convert_input_to_string(test: dict) -> str:
        raise NotImplementedError

    def convert_output_to_string(output) -> str:
        return str(output)

    @classmethod
    def generate_test_files(cls, target_directory=None):
        # TODO: show progressbar?
        if target_directory is None:
            target_directory = os.getcwd()
        target_directory = os.path.join(target_directory, "data")
        try:
            os.mkdir(target_directory)
        except FileExistsError:
            pass

        test_suite = cls.generate_random_tests()
        tests = test_suite.tests[:]
        mutations = cls.mutate(test_suite)
        for survivor in list(filter(lambda m: m.status ==
                                              Status.SURVIVED, mutations)):
            mutantKiller = MutantKiller(cls, survivor, test_suite)

            inputs = mutantKiller.generate_sbst_inputs()

            inputs.extend(mutantKiller.generate_mutation_sbst_inputs())
            test_suite.add(mutantKiller.generate_new_test_suite(inputs))

        killing_indices = set()
        mutants_killed = []
        mutants_survived = []
        for mutant in mutations:
            test_result, _, indices = test_suite.run(mutant.ast_node)
            if test_result == 'SUCCESS':
                mutants_survived.append(mutant)
            elif test_result == 'FAIL':
                killing_indices = killing_indices | set(indices[:3])
                mutants_killed.append(mutant)

        tests.extend(test_suite.tests[i] for i in killing_indices)

        for idx, test in enumerate(tests):
            with open(os.path.join(target_directory, "%03d.in" % idx), "w") as f:
                f.write(cls.convert_input_to_string(**test[0]))
            with open(os.path.join(target_directory, "%03d.ans" % idx), "w") as f:
                f.write(cls.convert_output_to_string(test[1]))

        print("Generated %d tests" % len(tests))
        print('Killed: {}, Survived: {}'.format(
            len(mutants_killed), len(mutants_survived)))
