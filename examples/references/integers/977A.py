import cotegen

# http://codeforces.com/problemset/problem/977/A

class CF977A(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(2, 10**9),
            'k': cotegen.types.Integer(1, 50)
        }

    output_type = int

    constraints = [
        cotegen.constraints.CustomConstraint(lambda test: CF977A.solve(**test) > 0)
    ]

    def solve(n: int, k: int) -> int:
        # 2 <= n <= 10**9, 1 <= k <= 50
        # answer > 0 (hard-to-satisfy condition)
        ans = n
        for _ in range(k):
            if ans % 10 == 0:
                ans = ans // 10
            else:
                ans -= 1
        return ans


    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer



if __name__ == '__main__':
    tests = CF977A.generate_random_tests()
    print(len(tests))
    for test in tests:
        print(test)
