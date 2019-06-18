import cotegen

# http://codeforces.com/problemset/problem/231/A

from typing import List


class CF231A(cotegen.Task):
    input_parameters = {
        'n': cotegen.types.Integer(1, 1000),
        'a': cotegen.types.FixedVariableLengthIntegerSequence('n', 0, 1),
        'b': cotegen.types.FixedVariableLengthIntegerSequence('n', 0, 1),
        'c': cotegen.types.FixedVariableLengthIntegerSequence('n', 0, 1),
    }

    output_type = int

    constraints = []

    def solve(n: int, a: List[int], b: List[int], c: List[int]) -> int:
        ret = 0
        for i in range(n):
            if a[i] + b[i] + c[i] >= 2:
                ret += 1
        return ret

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(n: int, a: List[int], b: List[int], c: List[int]):
        lines = ["%d\n" % n]
        for i in range(n):
            lines.append("%d %d %d\n" % (a[i], b[i], c[i]))
        return "\n".join(lines)


if __name__ == '__main__':
    import os
    CF231A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF231A"))
