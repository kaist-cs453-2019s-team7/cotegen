from typing import List, Tuple

from .mutate import Mutator
from .task import Task
from .context import Status
from .test import TestSuite

import cotegen.ast_utils as ast_utils
import cotegen


class MutationRunner():
    def __init__(self, file_location):
        target_file = ast_utils.code_to_ast(file_location)
        Task.input_parameters = ast_utils.get_input_parameters(target_file)
        self.target_function = ast_utils.get_solve_function(target_file)
        self.compare_function = ast_utils.get_compare_function(target_file)

        # TODO: make `Context` object containing each mutation and its corresponding information
        self.mutations = []

        # TODO: make `Test` object
        self.tests = None

        self.survived = []

    def generate_mutations(self):
        mutator = Mutator(self.target_function)
        mutator.apply_mutations()
        mutator.print_mutations()
        self.mutations = mutator.mutations

    def generate_initial_tests(self):
        inputs = Task.generate_tests()

        self.tests = TestSuite(self.target_function,
                               inputs, self.compare_function)

    def execute_mutations(self):
        for mutation in self.mutations:
            mutation.execute(self.tests)

    def print_survived_mutants(self):
        for mutation in self.mutations:
            if mutation.status == Status.SURVIVED:
                mutation.print(verbose=True)

    def print_all_mutants(self):
        for mutation in self.mutations:
            mutation.print(verbose=False)


if __name__ == "__main__":
    # 996A: AssertionError
    # 263A: handle convert_input_parameters function
    runner = MutationRunner('examples/references/integers/4A.py')

    runner.generate_mutations()
    runner.generate_initial_tests()
    runner.execute_mutations()

    runner.print_all_mutants()
