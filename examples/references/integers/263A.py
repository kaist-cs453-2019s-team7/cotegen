import cotegen

# http://codeforces.com/problemset/problem/263/A

from typing import List


class CF263A(cotegen.Task):
    input_parameters = {
        'x': cotegen.types.Integer(0, 24),
    }

    @classmethod
    def convert_input_parameters_to_test(cls, test) -> dict:
        ret = [[0] * 5 for _ in range(5)]
        ret[test['x'] // 5][test['x'] % 5] = 1
        return ret

    output_type = int

    def solve(a: List[List[int]]) -> int:
        for i in range(5):
            for j in range(5):
                if a[i][j] == 1:
                    return abs(i - 2) + abs(j - 2)

    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer


if __name__ == '__main__':
    tests = CF263A.generate_tests()
    print(len(tests))
    for test in tests:
        print(test)
