import cotegen
from typing import Tuple

# http://codeforces.com/problemset/problem/1154/A

class CF1154A(cotegen.Task):
    num_test_tries = 1000

    input_parameters = \
        {
            'x1': cotegen.types.Integer(2, 10**9),
            'x2': cotegen.types.Integer(2, 10**9),
            'x3': cotegen.types.Integer(2, 10**9),
            'x4': cotegen.types.Integer(2, 10**9),
        }

    output_type = int

    def _check_input(x1: int, x2: int, x3: int, x4: int):
        ret = CF1154A.solve(x1, x2, x3, x4)
        return len(ret) == 3 and min(ret) > 0 and \
            set([ret[0] + ret[1], ret[1] + ret[2], ret[2] + ret[0], sum(ret)]) == set([x1, x2, x3, x4])

    constraints = [
        cotegen.constraints.CustomConstraint(lambda test: CF1154A._check_input(**test) > 0)
    ]

    def solve(x1: int, x2: int, x3: int, x4: int) -> Tuple[int, int, int]:
        # 2 <= x_i <= 10**9, answer should be positive
        m = max([x1, x2, x3, x4])
        ret = []
        if x1 < m:
            ret.append(m - x1)
        if x2 < m:
            ret.append(m - x2)
        if x3 < m:
            ret.append(m - x3)
        if x4 < m:
            ret.append(m - x4)
        return tuple(ret)


    def compare(user_answer: Tuple[int,int,int], jury_answer: Tuple[int,int,int]) -> bool:
        return sorted(user_answer) == sorted(jury_answer)


if __name__ == '__main__':
    tests = CF1154A.generate_tests()
    print(len(tests))
    for test in tests:
        print(test, CF1154A.solve(**test))
