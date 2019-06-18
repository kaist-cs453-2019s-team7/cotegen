import cotegen

from typing import List


class CF344A(cotegen.Task):
    input_parameters = \
        {
            'a': cotegen.types.IntegerSequence(1, 100000, 0, 1),
        }

    output_type = int

    def solve(a: List[int]):
        ret = 1
        for i in range(len(a) - 1):
            if a[i] != a[i+1]:
                ret += 1
        return ret

    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(a: List[int]):
        return ("%d\n" % len(a)) + "\n".join(map(lambda x: ["10","01"][x], a)) + "\n"


if __name__ == '__main__':
    import os
    CF344A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF344A"))
