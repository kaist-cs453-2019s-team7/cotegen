import copy
import ast
import astor

from ..context import Context

from ..localsearch.trace import inject_trace_hook

from .operators import compare_mutation, and_or_mutation, operator_mutation
import cotegen.ast_utils as ast_utils


def _mutate_by_op(original, op, set_target_attribute, mutation_op):
    mutants = []
    for to_mutate, new_op in mutation_op:
        if ast_utils.to_string(op) == to_mutate:
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

    if number.n != 0:
        mutants.append(ast_utils.minus(number))

    return mutants


class Mutator(ast_utils.TreeWalk):
    def __init__(self, target_function_AST):
        ast_utils.TreeWalk.__init__(self)
        self.mutations = []
        self.target = target_function_AST
        self.in_context_should_not_mutate = False

        self.cur_branch_num = 0
        self.prev_branch_id = None
        self.false_branches_stack = []

        self.is_in_bool_expr = False

    def apply_mutations(self):
        ast_utils.TreeWalk.walk(self, self.target)

    def pre_Compare(self):
        self.is_in_bool_expr = True
        if self.in_context_should_not_mutate:
            return

        self.mutations.extend(self.mutate_current_node(mutate_compare))

    def post_Compare(self):
        self.is_in_bool_expr = False

    def pre_BoolOp(self):
        self.is_in_bool_expr = True
        if self.in_context_should_not_mutate:
            return

        self.mutations.extend(self.mutate_current_node(mutate_and_or))

    def post_BoolOp(self):
        self.is_in_bool_expr = False

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
        for mutation in self.mutations:
            mutation.print(verbose=True)

    def is_predicate_test(self):
        return self.is_in_bool_expr and (isinstance(self.parent, ast.If) or isinstance(self.parent, ast.While))

    def mutate_current_node(self, mutate_func):
        mutations = []

        original = self.cur_node
        mutants = mutate_func(original)
        for mutant in mutants:
            if self.is_predicate_test():
                mutant = inject_trace_hook(
                    mutant, self.cur_branch_num, mutation=True, original=original)

            self.replace(mutant)
            mutation = Context(copy.deepcopy(self.target))
            mutation.is_mutant_in_predicate = self.is_predicate_test()
            mutation.branch_id = self._get_branch()

            mutations.append(mutation)

            self.replace(original)

        return mutations

    def pre_If(self):
        self._pre_Conditional_statement()

    def pre_While(self):
        self._pre_Conditional_statement()

    def pre_orelse_name(self):
        if len(self.cur_node) > 0 and hasattr(self.cur_node[0], 'flag') and self.cur_node[0].flag == True:
            self.false_branches_stack.append(self.cur_branch_num)

    def post_orelse_name(self):
        if len(self.cur_node) > 0 and hasattr(self.cur_node[0], 'flag') and self.cur_node[0].flag == True:
            self.cur_node[0].flag == False
            self.false_branches_stack.pop()

    def _pre_Conditional_statement(self):
        self.prev_branch_id = self._get_branch()
        self.cur_branch_num += 1

        if len(self.cur_node.orelse) > 0:
            self.cur_node.orelse[0].flag = True

    def _get_branch(self):
        if self.is_predicate_test():
            return self.prev_branch_id

        branch_num = self.cur_branch_num
        branch_type = not (len(self.false_branches_stack) >
                           0 and self.false_branches_stack[-1] == self.cur_branch_num)

        return (branch_num, branch_type)
