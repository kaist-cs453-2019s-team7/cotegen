import astor
import ast

from cotegen.mutate import Mutator
from cotegen.task import Task

from cotegen.ast_utils import find_assign, find_function

import cotegen


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


def make_function_call(function_name, args):
    call_str = '{func}('.format(func=function_name)

    for id, value in args.items():
        if isinstance(value, str):
            value = '\'{}\''.format(value)

        call_str += '{id}={value},'.format(id=id, value=value)

    call_str = call_str[:-1] + ')'

    return call_str


def to_source(function_def):
    return compile(ast.Module(body=[function_def]), '', 'exec')


class MutationRunner():
    def __init__(self, file_location):
        target_file = astor.code_to_ast.parse_file(file_location)
        Task.input_parameters = get_input_parameters(target_file)
        self.target_function = get_solve_function(target_file)
        self.compare_function = get_compare_function(target_file)

        # TODO: make `Context` object containing each mutation and its corresponding information
        self.mutations = []

        # TODO: make `Test` object
        self.tests = []

        self.survived = []

    def generate_mutations(self):
        mutator = Mutator(self.target_function)
        mutator.apply_mutations()
        self.mutations = mutator.mutations

    def generate_initial_tests(self):
        inputs = Task.generate_tests()

        jury_answers = []
        exec(to_source(self.target_function), locals())
        for input in inputs:
            solve_call = make_function_call('solve', input)

            jury_answers.append(eval(solve_call))

        self.tests = list(zip(inputs, jury_answers))

    def execute_mutations(self):
        exec(to_source(self.compare_function), locals())

        for mutation in self.mutations:
            exec(to_source(mutation), locals())

            status = 'SURVIVED'
            for input, jury_answer in self.tests:
                solve_call = make_function_call('solve', input)

                output = eval(solve_call)
                targets = {
                    'user_answer': output,
                    'jury_answer': jury_answer
                }
                compare_call = make_function_call('compare', targets)

                if eval(compare_call) == False:
                    status = 'KILLED'
                    break

            if status is 'SURVIVED':
                self.survived.append(mutation)

    def print_survived_mutants(self):
        for mutation in self.survived:
            print(astor.to_source(mutation))


if __name__ == "__main__":
    runner = MutationRunner('examples/references/integers/4A.py')

    runner.generate_mutations()
    runner.generate_initial_tests()
    runner.execute_mutations()

    runner.print_survived_mutants()
