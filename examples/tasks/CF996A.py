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
        if n >= 100:
            cnt = n // 100
            ret += cnt
            n -= 100 * cnt
        if n >= 20:
            cnt = n // 20
            ret += cnt
            n -= 20 * cnt
        if n >= 10:
            cnt = n // 10
            ret += cnt
            n -= 10 * cnt
        if n >= 5:
            cnt = n // 5
            ret += cnt
            n -= 5 * cnt
        if n >= 1:
            cnt = n // 1
            ret += cnt
            n -= 1 * cnt
        assert n == 0
        return ret

    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    def convert_input_to_string(n: int) -> str:
        return "%d\n" % n


if __name__ == '__main__':
    import os
    CF996A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF996A"))
