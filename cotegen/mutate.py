import astor
import ast
import copy


def omit_function_call():
    pass


def get_mutated_operator(cur_node):
    new_op = None
    new_test = copy.deepcopy(cur_node.test)

    if isinstance(cur_node.test, ast.Compare):
        op = cur_node.test.ops[0]

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

    elif isinstance(cur_node.test, ast.BoolOp):
        op = cur_node.test.op

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
        self.mutation_candidates = []
        self.target_function = target_function_AST

    def walk(self):
        astor.TreeWalk.walk(self, self.target_function)

    def pre_FunctionDef(self):
        pass

    def _pre_Conditional_statement(self):
        original_test = copy.deepcopy(self.cur_node.test)

        mutated_test = get_mutated_operator(self.cur_node)
        if mutated_test:
            self.cur_node.test = mutated_test

            mutated_function = copy.deepcopy(self.target_function)
            self.cur_node.test = original_test

            self.mutation_candidates.append(mutated_function)

    def pre_If(self):
        self._pre_Conditional_statement()

    def pre_While(self):
        self._pre_Conditional_statement()

    def get_mutation(self):
        mutated_function = self.mutation_candidates.pop()
        return mutated_function
