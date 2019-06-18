import cotegen


from typing import Tuple


class CF805A(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(1, 2 * 10**9)
        }

    output_type = int

    def solve(n: int) -> int:
        if n % 2 == 1:
            return 0
        elif n % 4 == 0:
            return n // 4 - 1
        else:
            return n // 4

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(n: int):
        return "%d\n" % (n)


if __name__ == '__main__':
    import os
    CF805A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF610A"))
