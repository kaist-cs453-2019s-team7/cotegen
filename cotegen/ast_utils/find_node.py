import ast
import astor


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
