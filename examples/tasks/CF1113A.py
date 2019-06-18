import cotegen


from typing import Tuple


class CF1113A(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(2, 100),
            'v': cotegen.types.Integer(2, 100),
        }

    output_type = int

    def solve(n: int, v: int) -> int:
        if n < v:
            return n - 1
        else:
            return v + ((n - v) * (n - v + 1) // 2) - 1

    @staticmethod
    def compare(user_answer: str, jury_answer: str) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(n: int, v: int):
        return "%d %d\n" % (n, v)


if __name__ == '__main__':
    import os
    CF1113A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF1113A"))
