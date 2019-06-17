import cotegen
from typing import List

# http://codeforces.com/problemset/problem/937/A


class CF937A(cotegen.Task):
    input_parameters = \
        {
            'a': cotegen.types.IntegerSequence(1, 100, 0, 600)
        }

    output_type = int

    constraints = [
        cotegen.constraints.CustomConstraint(lambda test: any(x > 0 for x in test['a']))
    ]

    def solve(a: List[int]) -> int:
        ans = 0
        n = len(a)
        for i in range(n):
            good = (a[i] > 0)
            for j in range(i):
                if a[i] == a[j]:
                    good = False
            if good:
                ans += 1
        return ans

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(a: List[int]):
        return "%d\n%s\n" % (len(a), " ".join(map(str, a)))


if __name__ == '__main__':
    CF937A.generate_test_files("~/Downloads/CS453/CF937A")
