import cotegen

# http://codeforces.com/problemset/problem/1/A

class CF1A(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(1, 10**9),
            'm': cotegen.types.Integer(1, 10**9),
            'a': cotegen.types.Integer(1, 10**9),
        }

    output_type = int

    @classmethod
    def solve(n: int, m: int, a: int) -> int:
        # 1 <= n, m, a <= 10**9
        return ((n + (a-1)) // a) * ((m + (a-1)) // a)

    @classmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer


if __name__ == '__main__':
    print(CF1A.generate_tests())
