import os

from .random import RandomGenerator
from .exceptions import CotegenTaskConstraintError


class Task:
    num_test_tries = 10
    input_parameters = {}
    output_type = None
    constraints = []

    branch_tree = None
    ast_node = {
        'solve': None,
    }

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
    def generate_random_tests(cls):
        tests = RandomGenerator.generate_inputs(cls.input_parameters, cls.constraints, cls.num_test_tries)

        return list(map(cls.convert_input_parameters_to_test,
                         filter(cls.check_input_constraint, tests)))

    def convert_input_to_string(test: dict) -> str:
        raise NotImplementedError

    def convert_output_to_string(output) -> str:
        return str(output)

    @classmethod
    def generate_test_files(cls, target_directory=None):
        # TODO: show progressbar?
        if target_directory is None:
            target_directory = os.getcwd()
        if any(os.scandir(target_directory)):
            raise FileExistsError("target_directory not empty")

        tests = cls.generate_random_tests()
        for idx, test in enumerate(tests):
            with open(os.path.join(target_directory, "%03d.in" % idx), "w") as f:
                f.write(cls.convert_input_to_string(**test))
            with open(os.path.join(target_directory, "%03d.ans" % idx), "w") as f:
                f.write(cls.convert_output_to_string(cls.solve(**test)))

        print("Generated %d tests" % len(tests))
