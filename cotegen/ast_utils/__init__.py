import astor
import ast

from .tree_walk import TreeWalk
# TODO: handle both directions with one predifined dictionary
# Now it's quite stupid

def to_source(op):
    op_string = None
    if isinstance(op, ast.GtE):
        op_string = '<='
    elif isinstance(op, ast.Gt):
        op_string = '<'
    elif isinstance(op, ast.LtE):
        op_string = '>='
    elif isinstance(op, ast.Lt):
        op_string = '>'
    elif isinstance(op, ast.NotEq):
        op_string = '!='
    elif isinstance(op, ast.Eq):
        op_string = '=='
    elif isinstance(op, ast.And):
        op_string = 'and'
    elif isinstance(op, ast.Or):
        op_string = 'or'

    return op_string


def to_ast_node(op_string):
    op = None
    if op_string == '<=':
        op = ast.GtE()
    elif op_string == '<':
        op = ast.Gt()
    elif op_string == '>=':
        op = ast.LtE()
    elif op_string == '>':
        op = ast.Lt()
    elif op_string == '!=':
        op = ast.NotEq()
    elif op_string == '==':
        op = ast.Eq()
    elif op_string == 'and':
        op = ast.And()
    elif op_string == 'or':
        op = ast.Or()

    return op

def print_ast(node):
    print(astor.to_source(node))

