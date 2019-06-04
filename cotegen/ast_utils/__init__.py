import astor
import ast

from .tree_walk import TreeWalk
from .parse_file import find_assign, find_function, get_solve_function, get_compare_function, get_input_parameters, get_convert_function


ast_string = {
    ast.Gt: '<',
    ast.GtE: '<=',
    ast.Lt: '>',
    ast.LtE: '>=',
    ast.NotEq: '!=',
    ast.Eq: '==',
    ast.And: 'and',
    ast.Or: 'or',
    ast.Add: '+',
    ast.Sub: '-',
    ast.Mult: '*',
    ast.Div: '/',
    ast.FloorDiv: '//',
    ast.Mod: '%',
    ast.LShift: '<<',
    ast.RShift: '>>',
    ast.BitAnd: '&',
    ast.BitOr: '|',
    ast.BitXor: '^',
}


def increment(number):
    return ast.copy_location(ast.Num(number.n + 1), number)


def decrement(number):
    return ast.copy_location(ast.Num(number.n - 1), number)


def is_division_operation(node):
    if isinstance(node.op, ast.Div) or isinstance(node.op, ast.FloorDiv) or isinstance(node.op, ast.Mod):
        return True

    return False


def to_string(op):
    for ast_node, string in ast_string.items():
        if isinstance(op, ast_node):
            return string


def to_ast_node(op_string):
    for ast_node, string in ast_string.items():
        if op_string == string:
            return ast_node()


def ast_to_executable(ast_expr):
    return compile(ast.Module(body=[ast_expr]), '', 'exec')


def print_ast(node):
    print(astor.to_source(node))
