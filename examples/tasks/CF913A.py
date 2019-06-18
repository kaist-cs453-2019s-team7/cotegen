import cotegen


from typing import Tuple


class CF913A(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(2, 10**8),
            'm': cotegen.types.Integer(2, 10**8),
        }

    output_type = int

    def solve(n: int, m: int) -> int:
        if m <= 30:
            return n % (2 ** m)
        else:
            return n

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(n: int, m: int):
        return "%d\n%d\n" % (n, m)


if __name__ == '__main__':
    import os

    CF913A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF913A"))
