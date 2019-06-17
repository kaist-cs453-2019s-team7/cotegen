from .context import Status
from .test import TestSuite
from .function_def import FunctionDef

from cotegen.localsearch.fitnesscalc import FitnessCalculator, MutationFitnessCalculator
from cotegen.localsearch.avm import AVM

import cotegen.ast_utils as ast_utils


class MutantKiller():
    # Kill given survived mutant
    def __init__(self, task, mutant, test_suite, retry_count=10):
        # assert mutant.status == Status.SURVIVED

        self.task = task
        self.mutant = mutant
        self.test_suite = test_suite
        self.retry_count = retry_count

        solve_ast = ast_utils.function_to_ast_node(task.solve)

        self.target_function = FunctionDef(solve_ast)
        self.mutated_function = FunctionDef(self.mutant.ast_node)

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
            self.task.solve, self.task.compare, inputs)

        return new_test_suite

