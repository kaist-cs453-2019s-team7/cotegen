import cotegen

# http://codeforces.com/problemset/problem/158/A

from typing import List

class CF158A(cotegen.Task):
    input_parameters = \
        {
            'k': cotegen.types.Integer(1, 50),
            'a': cotegen.types.NonIncreasingIntegerSequence(1, 100, 0, 100),
        }

    output_type = int

    constraints = [
        cotegen.constraints.ListLengthReqInteger('a', 'k')
    ]

    def solve(k: int, a: List[int]) -> int:
        # 1 <= k <= len(a) <= 50, 0 <= a[i] <= 100, a nonincreasing
        ret = 0
        for x in a:
            if x > 0 and x >= a[k-1]:
                ret += 1
        return ret


    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer


if __name__ == '__main__':
    tests = CF158A.generate_tests()
    print(len(tests))
    for test in tests:
        print(test)
