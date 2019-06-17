import cotegen
from typing import List
import string


# http://codeforces.com/problemset/problem/92/A


class CF92A(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(1, 50),
            'm': cotegen.types.Integer(1, 10000),
        }

    output_type = int

    def solve(n: int, m: int) -> int:
        for i in range(m):
            if m <= i % n:
                break
            m = m - i % n - 1
        return m

    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(n: int, m: int):
        return "%d %d\n" % (n, m)


if __name__ == '__main__':
    CF92A.generate_test_files("~/Downloads/CS453/CF92A")
