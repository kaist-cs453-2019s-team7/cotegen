import astor
import ast
import copy


def mutate_predicate(predicate):
    new_op = None
    new_test = copy.deepcopy(predicate)

    if isinstance(predicate, ast.Compare):
        op = predicate.ops[0]

        if isinstance(op, ast.Gt):
            new_op = ast.GtE()
        elif isinstance(op, ast.GtE):
            new_op = ast.Gt()
        elif isinstance(op, ast.Lt):
            new_op = ast.LtE()
        elif isinstance(op, ast.LtE):
            new_op = ast.Lt()
        elif isinstance(op, ast.Eq):
            new_op = ast.NotEq()
        elif isinstance(op, ast.NotEq):
            new_op = ast.Eq()

        if new_op:
            new_test.ops[0] = new_op

    elif isinstance(predicate, ast.BoolOp):
        op = predicate.op

        if isinstance(op, ast.And):
            new_op = ast.Or()
        elif isinstance(op, ast.Or):
            new_op = ast.And()

        if new_op:
            new_test.op = new_op

    if new_op:
        return new_test


class Mutator(astor.TreeWalk):
    def __init__(self, target_function_AST):
        astor.TreeWalk.__init__(self)
        self.mutations = []
        self.target = target_function_AST

    def apply_mutations(self):
        astor.TreeWalk.walk(self, self.target)

    def pre_FunctionDef(self):
        pass

    def _pre_Conditional_statement(self):
        original_test = copy.deepcopy(self.cur_node.test)

        mutated_test = mutate_predicate(self.cur_node.test)
        if mutated_test:
            self.cur_node.test = mutated_test

            mutation = copy.deepcopy(self.target)
            self.cur_node.test = original_test

            self.mutations.append(mutation)

    def pre_If(self):
        self._pre_Conditional_statement()

    def pre_While(self):
        self._pre_Conditional_statement()

    def get_mutation(self):
        mutation = self.mutations.pop()
        return mutation
