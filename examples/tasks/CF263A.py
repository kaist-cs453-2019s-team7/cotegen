import cotegen

# http://codeforces.com/problemset/problem/263/A

from typing import List


class CF263A(cotegen.Task):
    input_parameters = {
        'x': cotegen.types.Integer(0, 24),
    }

    @staticmethod
    def convert_input_parameters_to_test(test) -> dict:
        ret = [[0] * 5 for _ in range(5)]
        ret[test['x'] // 5][test['x'] % 5] = 1
        return { 'a': ret }

    output_type = int

    def solve(a: List[List[int]]) -> int:
        for i in range(5):
            for j in range(5):
                if a[i][j] == 1:
                    return abs(i - 2) + abs(j - 2)

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(a: List[List[int]]):
        ret = []
        for row in a:
            ret.append(" ".join(map(str, row)) + "\n")
        return "".join(ret)



if __name__ == '__main__':
    import os
    CF263A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF263A"))
