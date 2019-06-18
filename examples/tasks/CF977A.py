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
        cotegen.constraints.CustomConstraint(lambda test: 'n' not in test or 'k' not in test or CF977A.solve(**test) > 0)
    ]

    def solve(n: int, k: int) -> int:
        ans = n
        for _ in range(k):
            if ans % 10 == 0:
                ans = ans // 10
            else:
                ans -= 1
        return ans

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    def convert_input_to_string(n: int, k: int) -> str:
        return "%d %d\n" % (n, k)


if __name__ == '__main__':
    import os
    CF977A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF977A"))
