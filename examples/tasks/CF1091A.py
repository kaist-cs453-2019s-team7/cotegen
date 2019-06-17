import cotegen

# http://codeforces.com/problemset/problem/946/A

from typing import List


class CF1091A(cotegen.Task):
    input_parameters = \
        {
            'y': cotegen.types.Integer(1, 100),
            'b': cotegen.types.Integer(2, 100),
            'r': cotegen.types.Integer(3, 100),
        }

    output_type = int

    def solve(y: int, b: int, r: int) -> int:
        return 3 * min(y + 1, b, r-1)

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(y: int, b: int, r: int):
        return "%d %d %d\n" % (y, b, r)


if __name__ == '__main__':
    CF1091A.generate_test_files("~/Downloads/CS453/CF1091A")
