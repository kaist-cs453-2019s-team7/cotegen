import cotegen

# http://codeforces.com/problemset/problem/935/A

class CF935A(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(2, 100000)
        }

    output_type = int

    def solve(n: int) -> int:
        # 2 <= n <= int(1e5)
        ret = 0
        for i in range(1, n):
            if n % i == 0:
                ret = ret + 1
        return ret


    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer


if __name__ == '__main__':
    tests = CF935A.generate_tests()
    print(len(tests))
    for test in tests:
        print(test)
