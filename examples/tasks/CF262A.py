import cotegen
from typing import List

# http://codeforces.com/problemset/problem/262/A


class CF262A(cotegen.Task):
    input_parameters = \
        {
            'k': cotegen.types.Integer(1, 100),
            'a': cotegen.types.IntegerSequence(2, 5000, 0, 600)
        }

    output_type = int

    def solve(k: int, a: List[int]) -> int:
        ans = 0
        for x in a:
            cnt = 0
            for c in str(x):
                if c in "47":
                    cnt += 1
            if cnt <= k:
                ans += 1
        return ans

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(k: int, a: List[int]):
        return ("%d %d\n" % (len(a), k)) + " ".join(map(str, a)) + "\n"


if __name__ == '__main__':
    CF262A.generate_test_files("~/Downloads/CS453/CF262A")

