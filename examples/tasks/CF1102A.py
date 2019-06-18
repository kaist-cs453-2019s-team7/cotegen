import cotegen


from typing import Tuple


class CF1102A(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(2, 10**9)
        }

    output_type = int

    def solve(n: int) -> int:
        if n % 4 == 0 or n % 4 == 3:
            return 0
        else:
            return 1

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(n: int):
        return "%d\n" % (n)


if __name__ == '__main__':
    import os
    CF1102A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF1102A"))
