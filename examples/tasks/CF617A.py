import cotegen

class CF617A(cotegen.Task):
    input_parameters = {
        'x': cotegen.types.Integer(1, 1000000),
    }

    output_type = int

    constraints = []

    def solve(x: int) -> int:
        if x % 5 >= 1:
            return x // 5 + 1
        else:
            return x // 5

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    def convert_input_to_string(x: int) -> str:
        return "%d\n" % x

if __name__ == '__main__':
    import os
    CF617A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF617A"))
