import cotegen.ast_utils as ast_utils


def make_function_call(function_name, args):
    call_str = '{func}('.format(func=function_name)

    for id, value in args.items():
        if isinstance(value, str):
            value = '\'{}\''.format(value)

        call_str += '{id}={value},'.format(id=id, value=value)

    call_str = call_str[:-1] + ')'

    return call_str


class TestSuite():
    def __init__(self, original_function, inputs, compare=None):
        self.tests = []
        self.compare_exec = ast_utils.ast_to_executable(compare)
        self.failed_tests = []

        original_function_exec = ast_utils.ast_to_executable(original_function)

        exec(original_function_exec, locals(), globals())
        for input in inputs:
            solve_call = make_function_call('solve', input)
            jury_answer = eval(solve_call)

            self.tests.append((input, jury_answer))

    def run(self, target_function):
        target_function_exec = ast_utils.ast_to_executable(target_function)
        exec(target_function_exec, locals(), globals())
        exec(self.compare_exec, locals(), globals())

        result = 'SUCCESS'  # TODO: use Enum
        for input, jury_answer in self.tests:
            solve_call = make_function_call('solve', input)
            output = eval(solve_call)

            comparators = {
                'user_answer': output,
                'jury_answer': jury_answer
            }
            compare_call = make_function_call('compare', comparators)
            if eval(compare_call) == False:
                self.failed_tests.append((input, jury_answer))
                result = 'FAIL'

        return result
