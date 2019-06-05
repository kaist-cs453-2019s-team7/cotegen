import ast

import copy
import astor

import cotegen.ast_utils as ast_utils


class FunctionDef():
    def __init__(self, node, branch_tree):
        self.branch_tree = branch_tree
        self.node = copy.deepcopy(node)
        self.name = self.node.name
        self.args_count = len(self.node.args.args)

        self.insert_hooks_on_predicates()
        self.exec = self._to_executable(self.node)

    def insert_hooks_on_predicates(self):
        walker = WalkPredicates()
        walker.walk(self.node)

    def _to_executable(self, node):
        return ast_utils.ast_to_executable(node)

    def call(self, args):
        source = '{func}('.format(func=self.name)

        for arg in args:
            source += '{arg}, '.format(arg=arg)

        source += 'trace)'

        return source


class NotInterceptableException(Exception):
    """Exception raised for errors when not able to inject trace

    Attributes:
        predicate -- predicate in not expected form
        message -- explanation of the error
    """

    def __init__(self, predicate, message):
        self.predicate = predicate
        self.message = message


class WalkPredicates(ast_utils.TreeWalk):
    def __init__(self):
        ast_utils.TreeWalk.__init__(self)

        self.cur_branch_num = 0

    def add_trace_argument(self):
        pass

    def pre_FunctionDef(self):
        trace = ast.copy_location(
            ast.arg(arg='trace', annotation=None), self.cur_node)
        self.cur_node.args.args.append(trace)

    def _inject_trace_hook(self, compare_node, branch_id):
        op = ''
        lhs = ''
        rhs = ''
        f_call = ''

        if isinstance(compare_node, ast.Call) and compare_node.func.value.id == 'trace':
            return compare_node

        if isinstance(compare_node, ast.BoolOp):
            lhs = astor.to_source(compare_node.values[0]).rstrip()
            rhs = astor.to_source(compare_node.values[1]).rstrip()
            # TODO: handle <3 values in boolop?

            if isinstance(compare_node.op, ast.And):
                op = 'bool_and'
            elif isinstance(compare_node.op, ast.Or):
                op = 'bool_or'

            f_call = 'trace.{fname}({branch_id}, {lhs}, {rhs})'.format(
                fname=op, branch_id=branch_id, lhs=lhs, rhs=rhs)

            f_call_node = ast.parse(f_call, '', 'eval').body

            f_call_node.args[1] = self._inject_trace_hook(f_call_node.args[1], None)
            f_call_node.args[2] = self._inject_trace_hook(f_call_node.args[2], None)

            return f_call_node



        elif not hasattr(compare_node, 'left') or not hasattr(compare_node, 'comparators'):
            op = 'is_true'
            arg = astor.to_source(compare_node).rstrip()

            f_call = 'trace.{fname}({branch_id}, {arg})'.format(
                fname=op, branch_id=branch_id, arg=arg)

        else:
            lhs = astor.to_source(compare_node.left).rstrip()
            rhs = astor.to_source(compare_node.comparators[0]).rstrip()

            if isinstance(compare_node.ops[0], ast.Gt):
                op = 'greater_than'
            elif isinstance(compare_node.ops[0], ast.GtE):
                op = 'greater_than_or_equals'
            elif isinstance(compare_node.ops[0], ast.Lt):
                op = 'less_than'
            elif isinstance(compare_node.ops[0], ast.LtE):
                op = 'less_than_or_equals'
            elif isinstance(compare_node.ops[0], ast.Eq):
                op = 'equals'
            elif isinstance(compare_node.ops[0], ast.NotEq):
                op = 'not_equals'
            else:
                raise NotInterceptableException(list(astor.iter_node(compare_node)),
                                                'Unexpected form of predicate in target function. All predicate in the target function should only involve relational operators.')

            f_call = 'trace.{fname}({branch_id}, {lhs}, {rhs})'.format(
                fname=op, branch_id=branch_id, lhs=lhs, rhs=rhs)

        f_call_node = ast.parse(f_call, '', 'eval').body


        return f_call_node

    def _pre_Conditional_statement(self):
        self.cur_branch_num += 1

        try:
            self.cur_node.test = self._inject_trace_hook(
                self.cur_node.test, self.cur_branch_num)

        except NotInterceptableException as err:
            print('{}: {}'.format(err.message, err.predicate))
            exit(1)

    def pre_If(self):
        self._pre_Conditional_statement()

    def pre_While(self):
        self._pre_Conditional_statement()
