import astor
import ast
from cotegen.mutate import Mutator


def get_function(node, name):
    if isinstance(node, ast.FunctionDef) and node.name == name:
        return node

    node = astor.iter_node(node)

    for attr in node:
        if attr[1] == 'body':
            body = attr[0]

            for child in body:
                target = get_function(child, name)
                if target:
                    return target


def get_solve_function(target_file):
    return get_function(target_file, 'solve')


if __name__ == "__main__":
    target_file = astor.code_to_ast.parse_file(
        'examples/references/integers/4A.py')
    target_function = get_solve_function(target_file)

    mutator = Mutator(target_function)
    mutator.apply_mutations()

    # should print mutated function
    print(astor.to_source(mutator.get_mutation()))

    # should print original function
    print(astor.to_source(target_function))
