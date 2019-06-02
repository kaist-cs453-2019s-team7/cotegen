import ast
import astor

import cotegen

def code_to_ast(file_location):
    return astor.code_to_ast.parse_file(file_location)

def get_solve_function(target_file):
    return find_function(target_file, 'solve')


def get_compare_function(target_file):
    return find_function(target_file, 'compare')


def get_input_parameters(target_file):
    assign_stmt = find_assign(target_file, 'input_parameters')
    dict_ast = assign_stmt.value

    def convert(ast_call):
        expr = ast.Expression(ast_call)
        return eval(compile(expr, '', 'eval'))

    input_parameters = dict(
        zip(map(lambda key: key.s, dict_ast.keys),
            map(convert, dict_ast.values)))

    return input_parameters


def find_function(node, name):
    def is_target_node(node, name): return isinstance(
        node, ast.FunctionDef) and node.name == name

    return find(is_target_node, node, name)


def find_assign(node, name):
    def is_target_node(node, name): return isinstance(
        node, ast.Assign) and node.targets[0].id == name

    return find(is_target_node, node, name)


def find(is_target_node, node, name):
    if is_target_node(node, name):
        return node

    node = astor.iter_node(node)

    for attr in node:
        if attr[1] != 'body':
            continue

        body = attr[0]

        for child in body:
            target = find(is_target_node, child, name)
            if target:
                return target
