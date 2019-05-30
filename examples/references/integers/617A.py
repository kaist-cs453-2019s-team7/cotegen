import cotegen

# http://codeforces.com/problemset/problem/4/A

class CF617A(cotegen.Task):
    input_parameters = {
        'x': cotegen.types.Integer(1, 1000000),
    }

    output_type = int

    constraints = []

    def solve(x: int) -> int:
        if x % 5 >= 1:
            return x // 5 + 1
        else:
            return x // 5

    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer


if __name__ == '__main__':
    tests = CF617A.generate_tests()
    print(len(tests))
    for test in tests:
        print(test)
