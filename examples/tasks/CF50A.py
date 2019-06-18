import cotegen

# http://codeforces.com/problemset/problem/50/A

class CF50A(cotegen.Task):
    input_parameters = \
        {
            'M': cotegen.types.Integer(1, 16),
            'N': cotegen.types.Integer(1, 16),
        }

    output_type = int

    constraints = [
        cotegen.constraints.Leq('M', 'N')
    ]

    def solve(M: int, N: int) -> int:
        return M * N // 2

    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(N: int, M: int):
        return "%d %d\n" % (N, M)

if __name__ == '__main__':
    import os
    CF50A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF50A"))
