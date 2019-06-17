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
    def __init__(self, solve, compare, inputs):
        self.tests = []
        self.compare = compare
        self.solve = solve
        self.failed_tests = []

        for input in inputs:
            jury_answer = output = self.solve(**input)

            self.tests.append((input, jury_answer))

    def print(self):
        for input, jury_answer in self.tests:
            print('{} => {}'.format(input, jury_answer))

    def run(self, target_function):
        target_function_exec = ast_utils.ast_to_executable(target_function)
        trace = Trace() # dummy trace object: TODO find better way
        exec(target_function_exec, locals(), globals())

        result = 'SUCCESS'  # TODO: use Enum
        killed_by = []
        killed_idx = []
        for idx, pair in enumerate(self.tests):
            input, jury_answer = pair
            try:
                output = self.solve_call(input)
            except (ValueError, KeyError):
                continue

            if self.compare(output, jury_answer) == False:
                killed_by.append((input, jury_answer))
                killed_idx.append(idx)
                if result == 'SUCCESS':
                    result = 'FAIL'

            if len(killed_by) > 3:
                break

        self.failed_tests.extend(killed_by)
        return result, killed_by, killed_idx

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
    def solve_call(input):
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
