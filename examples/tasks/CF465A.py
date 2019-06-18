import cotegen
from typing import List

# http://codeforces.com/problemset/problem/937/A


class CF465A(cotegen.Task):
    input_parameters = \
        {
            'a': cotegen.types.IntegerSequence(1, 100, 0, 1)
        }

    output_type = int

    def solve(a: List[int]) -> int:
        cur = 1
        ret = 0
        for x in a:
            ret += 1
            cur += x
            if cur < 2:
                break
            cur //= 2
        return ret

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(a: List[int]):
        return "%d\n%s\n" % (len(a), "".join(map(str, a)))


if __name__ == '__main__':
    import os
    CF465A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF465A"))
