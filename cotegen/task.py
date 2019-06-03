import random

class Task:
    num_test_tries = 10
    input_parameters = {}
    output_type = None
    constraints = []

    @classmethod
    def solve(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def compare(cls, user_answer, jury_answer) -> bool:
        return user_answer == jury_answer

    @classmethod
    def convert_input_parameters_to_test(cls, test) -> dict:
        return test

    @classmethod
    def check_input_constraint(cls, test) -> bool:
        return set(test.keys()) == set(cls.input_parameters.keys()) \
            and all(typ.is_valid(test[key], test) for key, typ in cls.input_parameters.items()) \
            and all(constraint.is_valid(test) for constraint in cls.constraints)

    @classmethod
    def generate_tests(cls):
        tests = [{}]
        input_parameters_until_now = dict()

        while len(input_parameters_until_now) < len(cls.input_parameters):
            input_parameters_step = {}

            input_parameters_until_now_keys = set(input_parameters_until_now.keys())
            for key, typ in cls.input_parameters.items():
                if key not in input_parameters_until_now_keys and set(typ.dependent_variable_names()).issubset(input_parameters_until_now_keys):
                    input_parameters_step[key] = typ

            if len(input_parameters_step) == 0:
                # TODO: make exception a name
                raise CotegenTaskConstraintError("dependencies have a cycle")

            for key, typ in input_parameters_step.items():
                input_parameters_until_now[key] = typ

            def check_partial_input_constraint(test):
                return set(test.keys()).issubset(set(input_parameters_until_now.keys())) \
                    and all(typ.is_valid(test[key], test) for key, typ in input_parameters_until_now.items() if key in test.keys()) \
                    and all(not constraint.is_defined(test) or constraint.is_valid(test) for constraint in cls.constraints)

            nxt_tests = []
            for cur_test in tests:
                variable_tests = { k: typ.sample(cur_test) for k, typ in input_parameters_step.items() }

                def add_test(test_function):
                    nonlocal nxt_tests
                    for _ in range(cls.num_test_tries):
                        test = {**cur_test, **test_function()}
                        if check_partial_input_constraint(test):
                            nxt_tests.append(test)
                            return True
                    return False

                if len(variable_tests) == 1:
                    for key, k_tests in variable_tests.items():
                        for test in k_tests:
                            add_test(lambda: {key: test})
                    tests = nxt_tests
                    continue

                # small/large random
                for idx, bound in enumerate([1, 2, 5]):
                    for _ in range(idx+1):
                        # TODO: greedy set cover와 같은 방식으로 바꾸는 것 고려해 보기
                        add_test(lambda: { k: random.choice(k_tests[:min(bound, len(k_tests))]) for k, k_tests in variable_tests.items() })
                        add_test(lambda: { k: random.choice(k_tests[-min(bound, len(k_tests)):]) for k, k_tests in variable_tests.items() })

                # total random
                for _ in range(10):
                    add_test(lambda: { k: random.choice(k_tests) for k, k_tests in variable_tests.items() })

                tests = nxt_tests

        tests = list(map(cls.convert_input_parameters_to_test, filter(cls.check_input_constraint, tests)))
        return tests
