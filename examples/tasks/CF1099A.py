import cotegen



class CF1099A(cotegen.Task):
    input_parameters = \
        {
            'w': cotegen.types.Integer(0, 100),
            'h': cotegen.types.Integer(2, 100),
            'u1': cotegen.types.Integer(0, 100),
            'd1': cotegen.types.Integer(1, 100),
            'u2': cotegen.types.Integer(0, 100),
            'd2': cotegen.types.Integer(1, 100)
        }

    output_type = int

    constraints = [
        cotegen.constraints.Leq('d1', 'h'),
        cotegen.constraints.Leq('d2', 'h'),
        cotegen.constraints.CustomConstraint(lambda test: 'd1' not in test or 'd2' not in test or test['d1'] != test['d2'])
    ]

    def solve(w: int, h: int, u1: int, d1: int, u2: int, d2: int) -> int:
        ans = w
        for i in reversed(range(h)):
            ans += i
            if i == d1:
                ans -= u1
            if i == d2:
                ans -= u2
            if ans < 0:
                ans = 0
        return ans

    @staticmethod
    def compare(user_answer: str, jury_answer: str) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(w: int, h: int, u1: int, d1: int, u2: int, d2: int):
        return "%d %d\n%d %d\n%d %d\n" % (w, h, u1, d1, u2, d2)


if __name__ == '__main__':
    CF1099A.generate_test_files("~/Downloads/CS453/CF1099A")
