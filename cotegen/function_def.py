import ast

import copy
import astor

import cotegen.ast_utils as ast_utils

from .branch_tree import BranchTree, BranchNode


class FunctionDef():
    def __init__(self, node):
        self.node = copy.deepcopy(node)
        self.name = self.node.name
        self.args_count = len(self.node.args.args)

        self.insert_hooks_on_predicates()
        self.exec = self._to_executable(self.node)

    def insert_hooks_on_predicates(self):
        walker = WalkPredicates()
        walker.walk(self.node)

        self.branch_tree = walker.branch_tree

    def _to_executable(self, node):
        return ast_utils.ast_to_executable(node)

    def call(self, args):
        source = '{func}('.format(func=self.name)

        for arg in args:
            source += '{arg}, '.format(arg=arg)

        source += 'trace)'

        return source
    
    def print(self):
        ast_utils.print_ast(self.node)


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
        self.predicates_stack = []
        self.false_branches_stack = []
        self.branch_tree = BranchTree()

    def pre_FunctionDef(self):
        trace = ast.copy_location(
            ast.arg(arg='trace', annotation=None), self.cur_node)
        self.cur_node.args.args.append(trace)

    def pre_If(self):
        self._pre_Conditional_statement()

    def post_If(self):
        self._post_Conditional_statement()

    def pre_While(self):
        self._pre_Conditional_statement()

    def post_While(self):
        self._post_Conditional_statement()

    def pre_orelse_name(self):
        if len(self.cur_node) > 0 and hasattr(self.cur_node[0], 'flag') and self.cur_node[0].flag == True:
            self.false_branches_stack.append(self.cur_branch_num)

    def post_orelse_name(self):
        if len(self.cur_node) > 0 and hasattr(self.cur_node[0], 'flag') and self.cur_node[0].flag == True:
            self.cur_node[0].flag == False
            self.false_branches_stack.pop()

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

            f_call_node.args[1] = self._inject_trace_hook(
                f_call_node.args[1], None)
            f_call_node.args[2] = self._inject_trace_hook(
                f_call_node.args[2], None)

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

    def _create_branch_tree(self):
        parent = self.branch_tree.root

        if len(self.predicates_stack) > 0:
            true_node, false_node = self.predicates_stack[-1]

            if len(self.false_branches_stack) > 0 and self.false_branches_stack[-1] == self.cur_branch_num - 1:
                parent = false_node

        true_branch_node = BranchNode(
            num=self.cur_branch_num, type=True, ast_node=self.cur_node, parent=parent)
        false_branch_node = BranchNode(
            num=self.cur_branch_num, type=False, ast_node=self.cur_node, parent=parent)

        self.predicates_stack.append((true_branch_node, false_branch_node))

    def _pre_Conditional_statement(self):
        self.cur_branch_num += 1

        try:
            self.cur_node.test = self._inject_trace_hook(
                self.cur_node.test, self.cur_branch_num)

        except NotInterceptableException as err:
            print('{}: {}'.format(err.message, err.predicate))
            exit(1)

        self._create_branch_tree()

    def _post_Conditional_statement(self):
        self.predicates_stack.pop()
