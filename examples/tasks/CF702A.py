import cotegen

# http://codeforces.com/problemset/problem/946/A

from typing import List


class CF702A(cotegen.Task):
    input_parameters = \
        {
            'a': cotegen.types.IntegerSequence(1, 100000, 1, 10**9)
        }

    output_type = int

    def solve(a: List[int]) -> int:
        x = 0
        y = 0
        m = 0
        for i in a:
            if i > y:
                m = m + 1
            else:
                m = 1
            if x < m:
                x = m
            y = i
        return x

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(a: List[int]):
        return ("%d\n" % len(a)) + " ".join(map(str, a)) + "\n"


if __name__ == '__main__':
    CF702A.generate_test_files("~/Downloads/CS453/CF702A")
