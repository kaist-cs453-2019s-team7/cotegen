import copy

from .context import Context

from cotegen.mutation_ops import compare_mutation, and_or_mutation, operator_mutation, keyword_mutation
import cotegen.ast_utils as ast_utils


def mutate_compare(compare):
    mutants = []

    for index, op in enumerate(compare.ops):
        for key, new_op in compare_mutation.items():
            if ast_utils.to_string(op) == key:
                mutant = copy.deepcopy(compare)
                mutant.ops[index] = ast_utils.to_ast_node(new_op)

                mutants.append(mutant)

    return mutants


def mutate_and_or(boolop):
    mutants = []

    op = boolop.op

    for key, new_op in and_or_mutation.items():
            if ast_utils.to_string(op) == key:
                mutant = copy.deepcopy(boolop)
                mutant.op = ast_utils.to_ast_node(new_op)

                mutants.append(mutant)

    return mutants


class Mutator(ast_utils.TreeWalk):
    def __init__(self, target_function_AST):
        ast_utils.TreeWalk.__init__(self)
        self.mutations = []
        self.target = target_function_AST

    def apply_mutations(self):
        ast_utils.TreeWalk.walk(self, self.target)

    def pre_Compare(self):
        original = self.cur_node
        mutants = mutate_compare(original)
        for mutant in mutants:
            self.replace(mutant)
            mutation = Context(copy.deepcopy(self.target))
            self.mutations.append(mutation)

            self.replace(original)

    def pre_BoolOp(self):
        original = self.cur_node
        mutants = mutate_and_or(original)
        for mutant in mutants:
            self.replace(mutant)
            mutation = Context(copy.deepcopy(self.target))
            self.mutations.append(mutation)

            self.replace(original)

    def pre_If(self):
        pass

    def pre_While(self):
        pass

    def pre_FunctionDef(self):
        pass

    # TODO: mutation ID
    def get_mutation(self, id=None):
        if len(self.mutations) > 0:
            mutation = self.mutations.pop()
            return mutation

    def print_mutations(self):
        # should print all mutated functions
        for mutation in self.mutations:
            mutation.print(verbose=True)
