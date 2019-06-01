import ast
import astor

def find_function(node, name):
    if isinstance(node, ast.FunctionDef) and node.name == name:
        return node

    node = astor.iter_node(node)

    for attr in node:
        if attr[1] == 'body':
            body = attr[0]

            for child in body:
                target = find_function(child, name)
                if target:
                    return target


def find_assign(node, name):
    if isinstance(node, ast.Assign) and node.targets[0].id == name:
        return node

    node = astor.iter_node(node)

    for attr in node:
        if attr[1] == 'body':
            body = attr[0]

            for child in body:
                target = find_assign(child, name)
                if target:
                    return target
