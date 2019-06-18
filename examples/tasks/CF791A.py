import cotegen

# http://codeforces.com/problemset/problem/791/A

class CF791A(cotegen.Task):
    input_parameters = \
        {
            'a': cotegen.types.Integer(1, 10),
            'b': cotegen.types.Integer(1, 10),
        }

    output_type = int

    constraints = [
        cotegen.constraints.Leq('a', 'b')
    ]

    def solve(a: int, b: int) -> int:
        # 1 <= a <= b <= 10
        for i in range(100):
            if a > b:
                return i
            a *= 3
            b *= 2
        return False


    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer


if __name__ == '__main__':
    tests = CF791A.generate_random_tests()
    print(len(tests))
    for test in tests:
        print(test)
