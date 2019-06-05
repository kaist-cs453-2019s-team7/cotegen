from typing import List, Tuple

from .mutate import Mutator
from .task import Task
from .context import Context, Status
from .test import TestSuite
from .function_def import FunctionDef

from cotegen.localsearch.fitnesscalc import FitnessCalculator, MutationFitnessCalculator
from cotegen.localsearch.avm import AVM

import cotegen.ast_utils as ast_utils
import cotegen

import astor
import ast
import inspect


class MutantKiller():
    # Kill given survived mutant
    # TODO: task가 모든 것을 담고 있게 만들기
    def __init__(self, task: Task, mutant: Context, test_suite: TestSuite, retry_count=10):
        #assert mutant.status == Status.SURVIVED

        self.task = task
        self.mutant = mutant
        self.test_suite = test_suite
        self.retry_count = retry_count

        solve_ast = self.task.ast_node['solve']
        branch_tree = self.task.branch_tree
        self.target_function = FunctionDef(solve_ast, branch_tree)
        self.mutated_function = FunctionDef(self.mutant.ast_node, branch_tree)

    def generate_sbst_input(self):
        fitness_calculator = FitnessCalculator(
            self.target_function, self.mutant.branch_id)

        searcher = AVM(fitness_calculator, input_parameters=self.task.input_parameters,
                       constraints=self.task.constraints)

        minimised_args, fitness_value = searcher.minimise()

        if fitness_value == 0:
            return minimised_args

        else:
            return None

    def generate_sbst_inputs(self, count=100):
        inputs = []
        for i in range(count):
            args = self.generate_sbst_input()
            if args:
                inputs.append(args)

        return inputs

    def generate_mutation_sbst_input(self):
        fitness_calculator = MutationFitnessCalculator(
            self.mutated_function, self.mutant.branch_id)

        # print(astor.to_source(self.mutated_function.node))

        searcher = AVM(fitness_calculator, input_parameters=self.task.input_parameters,
                       constraints=self.task.constraints)

        minimised_args, fitness_value = searcher.minimise()

        if fitness_value == 0:
            return minimised_args

        else:
            return None

    def generate_mutation_sbst_inputs(self, count=100):
        inputs = []
        for i in range(count):
            args = self.generate_mutation_sbst_input()
            if args:
                inputs.append(args)

        return inputs

    def generate_new_test_suite(self, raw_inputs):
        inputs = []  # with parameter id

        for args in raw_inputs:
            input = {}
            for index, id in enumerate(self.task.input_parameters.keys()):
                input[id] = args[index]

            if self.task.convert_input_parameters_to_test:
                input = self.task.convert_input_parameters_to_test(input)
            inputs.append(input)

        new_test_suite = TestSuite(
            self.task.ast_node['solve'], inputs, self.task.ast_node['compare'])

        print(new_test_suite.run(self.mutant.ast_node))
        return new_test_suite


class MutationRunner():
    def __init__(self, task: Task):
        self.task = task
        # TODO: 이렇게 하면 class가 indent되어 있을 때 오류가 발생할 수 있음.
        target_file = ast.parse(inspect.getsource(task))

        self.input_parameters = ast_utils.get_input_parameters(target_file)
        self.target_function = ast_utils.get_solve_function(target_file)
        self.task.ast_node['solve'] = self.target_function
        self.compare_function = ast_utils.get_compare_function(target_file)
        self.task.ast_node['compare'] = self.compare_function

        self.mutations = []
        self.branch_tree = None
        self.test_suite = None
        self.survived = []

    def generate_mutations(self):
        mutator = Mutator(self.target_function)
        mutator.apply_mutations()
        self.mutations = mutator.mutations
        self.task.branch_tree = self.branch_tree = mutator.branch_tree

    def generate_initial_tests(self):
        inputs = self.task.generate_tests()

        self.test_suite = TestSuite(self.target_function,
                                    inputs, self.compare_function)

    def execute_mutations(self):
        for mutation in self.mutations:
            mutation.execute(self.test_suite)

            if mutation.status == Status.SURVIVED:
                self.survived.append(mutation)

    def count_survived_mutants(self, verbose=True):
        return len(self.survived)

    def print_survived_mutants(self, verbose=True):
        for mutation in self.survived:
            mutation.print(verbose)

    def print_all_mutants(self, verbose=False):
        for mutation in self.mutations:
            mutation.print(verbose)
