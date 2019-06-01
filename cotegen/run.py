import astor
import ast

from cotegen.mutate import Mutator
from cotegen.task import Task

import cotegen


def _get_function(node, name):
    if isinstance(node, ast.FunctionDef) and node.name == name:
        return node

    node = astor.iter_node(node)

    for attr in node:
        if attr[1] == 'body':
            body = attr[0]

            for child in body:
                target = _get_function(child, name)
                if target:
                    return target


def _get_assign(node, name):
    if isinstance(node, ast.Assign) and node.targets[0].id == name:
        return node

    node = astor.iter_node(node)

    for attr in node:
        if attr[1] == 'body':
            body = attr[0]

            for child in body:
                target = _get_assign(child, name)
                if target:
                    return target


def get_solve_function(target_file):
    return _get_function(target_file, 'solve')


def get_compare_function(target_file):
    return _get_function(target_file, 'compare')


def get_input_parameters(target_file):
    assign_stmt = _get_assign(target_file, 'input_parameters')
    dict_ast = assign_stmt.value

    def convert(ast_call):
        expr = ast.Expression(ast_call)
        return eval(compile(expr, '', 'eval'))

    input_parameters = dict(
        zip(map(lambda key: key.s, dict_ast.keys),
            map(convert, dict_ast.values)))

    return input_parameters


def make_function_call(function_name, args):
    call_str = '{func}('.format(func=function_name)

    for id, value in args.items():
        call_str += '{id}={value},'.format(id=id, value=value)

    call_str = call_str[:-1] + ')'

    return call_str


def to_source(function_def):
    return compile(ast.Module(body=[function_def]), '', 'exec')


if __name__ == "__main__":
    target_file = astor.code_to_ast.parse_file(
        'examples/references/integers/4A.py')
    target_function = get_solve_function(target_file)

    mutator = Mutator(target_function)
    mutator.apply_mutations()

    mutator.print_mutations()

    # TODO: execute each mutation with sample input
    Task.input_parameters = get_input_parameters(target_file)

    inputs = Task.generate_tests()
    print(inputs)

    jury_answers = []

    exec(to_source(target_function), locals())
    for input in inputs:
        solve_call = make_function_call('solve', input)

        jury_answers.append(eval(solve_call))

    survived_mutants = []
    for mutation in mutator.mutations:
        exec(to_source(mutation), locals())

        status = 'SURVIVED'
        for index, input in enumerate(inputs):
            solve_call = make_function_call('solve', input)

            output = eval(solve_call)
            if output != jury_answers[index]:
                status = 'KILLED'
                break

        if status is 'SURVIVED':
            survived_mutants.append(mutation)

    print(jury_answers)
    for mutation in survived_mutants:
        print(astor.to_source(mutation))