import cotegen

# http://codeforces.com/problemset/problem/946/A

from typing import List


class CF946A(cotegen.Task):
    input_parameters = \
        {
            'a': cotegen.types.IntegerSequence(1, 100, -100, 100),
        }

    output_type = int

    def solve(a: List[int]) -> int:
        ans = 0
        for x in a:
            if x < 0:
                ans -= x
            else:
                ans += x
        return ans

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(a: List[int]):
        return ("%d\n" % len(a)) + " ".join(map(str, a)) + "\n"



if __name__ == '__main__':
    CF946A.generate_test_files("~/Downloads/CS453/CF946A")
