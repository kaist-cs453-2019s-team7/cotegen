from .mutator import Mutator

import cotegen.ast_utils as ast_utils

class MutationGenerator():
    def __init__(self, target_function, input_parameters):
        self.input_parameters = input_parameters

        target_function_AST = ast_utils.function_to_ast_node(target_function)
        self.mutator = Mutator(target_function_AST)

    def get_mutations(self):
        self.mutator.apply_mutations()
        return self.mutator.mutations

    def execute_mutations(self, test_suite):
        mutations = self.get_mutations()
        for mutation in mutations:
            mutation.execute(test_suite)

        return mutations
