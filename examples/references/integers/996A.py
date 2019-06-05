import cotegen

# http://codeforces.com/problemset/problem/996/A

class CF996A(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(1, 10**9),
        }

    output_type = int

    def solve(n: int) -> int:
        ret = 0
        for bill in [100, 20, 10, 5, 1]:
            if n >= bill:
                cnt = n // bill
                ret += cnt
                n -= bill * cnt
        assert n == 0
        return ret

    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer


if __name__ == '__main__':
    tests = CF996A.generate_random_tests()
    print(len(tests))
    for test in tests:
        print(test)
