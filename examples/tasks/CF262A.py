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
            while x > 0:
                if x % 10 == 4 or x % 10 == 7:
                    cnt += 1
                x //= 10
            if cnt <= k:
                ans += 1
        return ans

    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer


if __name__ == '__main__':
    testsuite = CF262A.generate_random_tests()
    print(len(testsuite.tests))
    for test in testsuite.tests:
        print(test)
