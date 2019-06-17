import cotegen


from typing import Tuple


class CF854A(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(3, 1000),
        }

    output_type = Tuple[int, int]

    def solve(n: int) -> Tuple[int, int]:
        a = n // 2
        b = n - n // 2
        if n % 4 == 0:
            a -= 1
            b += 1
        elif n % 4 == 2:
            a -= 2
            b += 2
        return (a, b)

    @staticmethod
    def compare(user_answer: str, jury_answer: str) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(n: int):
        return "%d\n" % n

    @staticmethod
    def convert_output_to_string(output):
        return "%d %d\n" % output


if __name__ == '__main__':
    import os
    CF854A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF854A"))
