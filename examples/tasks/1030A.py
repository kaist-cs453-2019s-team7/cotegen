import cotegen

# http://codeforces.com/problemset/problem/1030/A

from typing import List

class CF1030A(cotegen.Task):
    input_parameters = \
        {
            'a': cotegen.types.IntegerSequence(1, 100, 0, 1),
        }

    output_type = str

    def solve(a: List[int]) -> str:
        # 1 <= len(a) <= 100, 0 <= a[i] <= 1
        for x in a:
            if x == 1:
                return "HARD"
        return "EASY"


    def compare(user_answer: str, jury_answer: str) -> bool:
        return user_answer.strip().lower() == jury_answer.strip().lower()


if __name__ == '__main__':
    tests = CF1030A.generate_random_tests()
    print(len(tests))
    for test in tests:
        print(test)
