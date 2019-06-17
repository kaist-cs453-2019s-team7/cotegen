import cotegen

# http://codeforces.com/problemset/problem/946/A

from typing import List
import string


class CF841A(cotegen.Task):
    input_parameters = \
        {
            'k': cotegen.types.Integer(1, 100),
            'a': cotegen.types.IntegerSequence(1, 100, 0, 25)
        }

    output_type = int

    def solve(k: int, a: List[int]) -> bool:
        for x in a:
            cnt = 0
            for i in a:
                if i == x:
                    cnt += 1
            if cnt > k:
                return False
        return True

    @staticmethod
    def compare(user_answer: bool, jury_answer: bool) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(k: int, a: List[int]):
        return ("%d %d\n" % (len(a), k)) + "".join(string.ascii_lowercase[x] for x in a) + "\n"

    @staticmethod
    def convert_output_to_string(output):
        return ["NO", "YES"][output]


if __name__ == '__main__':
    import os
    CF841A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF841A"))
