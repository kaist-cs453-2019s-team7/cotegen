from typing import List, Tuple

from .mutate import Mutator
from .task import Task
from .context import Status
from .test import TestSuite

import cotegen.ast_utils as ast_utils
import cotegen

import astor, ast
import inspect


class MutationRunner():
    def __init__(self, task: Task):
        self.task = task
        # TODO: 이렇게 하면 class가 indent되어 있을 때 오류가 발생할 수 있음.
        target_file = ast.parse(inspect.getsource(task))

        self.input_parameters = ast_utils.get_input_parameters(target_file)
        self.target_function = ast_utils.get_solve_function(target_file)
        self.compare_function = ast_utils.get_compare_function(target_file)
        self.convert = ast_utils.get_convert_function(target_file)

        self.mutations = []
        self.test_suite = None
        self.survived = []

    def generate_mutations(self):
        mutator = Mutator(self.target_function)
        mutator.apply_mutations()
        self.mutations = mutator.mutations

    def generate_initial_tests(self):
        inputs = self.task.generate_tests()

        self.test_suite = TestSuite(self.target_function,
                               inputs, self.compare_function, self.convert)

    def execute_mutations(self):
        for mutation in self.mutations:
            mutation.execute(self.test_suite)

    def print_survived_mutants(self):
        for mutation in self.mutations:
            if mutation.status == Status.SURVIVED:
                mutation.print(verbose=True)

    def print_all_mutants(self):
        for mutation in self.mutations:
            mutation.print(verbose=False)
