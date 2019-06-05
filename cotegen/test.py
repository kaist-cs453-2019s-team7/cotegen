import cotegen.ast_utils as ast_utils
from .localsearch.trace import Trace

from typing import List, Tuple


def make_function_call(function_name, args):
    if len(args) == 0:
        return '{func}()'.format(func=function_name)

    call_str = '{func}('.format(func=function_name)

    for id, value in args.items():
        if isinstance(value, str):
            value = '\'{}\''.format(value)

        call_str += '{id}={value},'.format(id=id, value=value)

    call_str = call_str[:-1] + ')'

    return call_str


class TestSuite():
    def __init__(self, original_function, inputs, compare):
        self.tests = []
        self.compare_exec = ast_utils.ast_to_executable(compare)
        self.failed_tests = []

        original_function_exec = ast_utils.ast_to_executable(original_function)

        exec(original_function_exec, locals(), globals())
        for input in inputs:
            jury_answer = output = self.solve(input)

            self.tests.append((input, jury_answer))

    def print(self):
        for input, jury_answer in self.tests:
            print('{} => {}'.format(input, jury_answer))

    def run(self, target_function):
        target_function_exec = ast_utils.ast_to_executable(target_function)
        trace = Trace() # dummy trace object: TODO find better way
        exec(target_function_exec, locals(), globals())
        exec(self.compare_exec, locals(), globals())

        result = 'SUCCESS'  # TODO: use Enum
        for input, jury_answer in self.tests:
            output = self.solve(input)

            if self.compare(output, jury_answer) == False:
                self.failed_tests.append((input, jury_answer))
                if result == 'SUCCESS':
                    result = 'FAIL'

        return result

    def add(self, test_suite):
        self.tests.extend(test_suite.tests)
        # remove duplicate
        new_tests = []
        for input, jury_answer in self.tests:
            duplicate = False
            for test in new_tests:
                if test[0] == input:
                    duplicate = True
                    break
            if not duplicate:
                new_tests.append((input, jury_answer))

        self.tests = new_tests

    @staticmethod
    def solve(input):
        solve_call = make_function_call('solve', input)

        try:
            return eval(solve_call)
        except AssertionError:
            return None
        except ZeroDivisionError:
            return None
        except IndexError:
            return None

        # TODO: handle invalid mutants (generating above Exceptions)

    @staticmethod
    def compare(user_answer, jury_answer):
        comparators = {
            'user_answer': user_answer,
            'jury_answer': jury_answer
        }
        compare_call = make_function_call('compare', comparators)
        return eval(compare_call)
