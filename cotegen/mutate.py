import copy

from .context import Context

from cotegen.mutation_ops import compare_mutation, and_or_mutation, operator_mutation, keyword_mutation
import cotegen.ast_utils as ast_utils


def _mutate_by_op(original, op, set_target_attribute, mutation_op):
    mutants = []
    for key, new_op in mutation_op.items():
        if ast_utils.to_string(op) == key:
            mutant = copy.deepcopy(original)
            set_target_attribute(mutant, ast_utils.to_ast_node(new_op))

            mutants.append(mutant)

    return mutants


def mutate_compare(compare):
    mutants = []

    for index, op in enumerate(compare.ops):
        def set_target_attribute(mutant, new_op):
            mutant.ops[index] = new_op

        mutants.extend(_mutate_by_op(
            compare, op, set_target_attribute, compare_mutation))

    return mutants


def mutate_and_or(boolop):
    mutants = []

    op = boolop.op

    def set_target_attribute(mutant, new_op):
        mutant.op = new_op

    mutants.extend(_mutate_by_op(
        boolop, op, set_target_attribute, and_or_mutation))

    return mutants


def mutate_operation(operation):
    mutants = []

    op = operation.op

    def set_target_attribute(mutant, new_op):
        mutant.op = new_op

    mutants.extend(_mutate_by_op(
        operation, op, set_target_attribute, operator_mutation))

    return mutants


def mutate_number(number):
    mutants = [ast_utils.increment(number), ast_utils.decrement(number)]

    return mutants


class Mutator(ast_utils.TreeWalk):
    def __init__(self, target_function_AST):
        ast_utils.TreeWalk.__init__(self)
        self.mutations = []
        self.target = target_function_AST

        self.in_context_should_not_mutate = False

    def apply_mutations(self):
        ast_utils.TreeWalk.walk(self, self.target)

    def pre_Compare(self):
        if self.in_context_should_not_mutate:
            return

        self.mutations.extend(self.mutate_current_node(mutate_compare))

    def pre_BoolOp(self):
        if self.in_context_should_not_mutate:
            return

        self.mutations.extend(self.mutate_current_node(mutate_and_or))

    def pre_BinOp(self):
        if self.in_context_should_not_mutate:
            return

        self.mutations.extend(self.mutate_current_node(mutate_operation))

    def pre_AugAssign(self):
        if self.in_context_should_not_mutate:
            return

        self.mutations.extend(self.mutate_current_node(mutate_operation))

    def pre_Num(self):
        if self.in_context_should_not_mutate:
            return

        self.mutations.extend(self.mutate_current_node(mutate_number))

    def pre_If(self):
        pass

    def pre_While(self):
        pass

    def pre_FunctionDef(self):
        pass

    def pre_Assert(self):
        self.in_context_should_not_mutate = True

    def post_Assert(self):
        self.in_context_should_not_mutate = False

    # TODO: mutation ID
    def get_mutation(self, id=None):
        if len(self.mutations) > 0:
            mutation = self.mutations.pop()
            return mutation

    def print_mutations(self):
        # should print all mutated functions
        for mutation in self.mutations:
            mutation.print(verbose=True)

    def mutate_current_node(self, mutate_func):
        mutations = []

        original = self.cur_node
        mutants = mutate_func(original)
        for mutant in mutants:
            self.replace(mutant)
            mutation = Context(copy.deepcopy(self.target))
            mutations.append(mutation)

            self.replace(original)

        return mutations
