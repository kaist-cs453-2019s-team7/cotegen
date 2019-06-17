import cotegen
from typing import List
import string

# http://codeforces.com/problemset/problem/831/B


class CF831B(cotegen.Task):
    input_parameters = \
        {
            'a': cotegen.types.IntegerPermutation(26, 26),
            'b': cotegen.types.IntegerPermutation(26, 26),
            's': cotegen.types.IntegerSequence(1, 1000, 0, 51),
        }

    output_type = List[int]

    def solve(a: List[int], b: List[int], s: List[int]) -> List[int]:
        ret = []
        for x in s:
            y = -1
            for i in range(26):
                if a[i] == x % 26:
                    y = b[i]
                    if x >= 26:
                        y += 26
                    break
            ret.append(y)
        return ret

    def compare(user_answer: List[int], jury_answer: List[int]) -> bool:
        return user_answer == jury_answer

    def convert_input_to_string(a: List[int], b: List[int], s: List[int]):
        lines = []
        lines.append("".join(string.ascii_lowercase[x] for x in a))
        lines.append("".join(string.ascii_lowercase[y] for y in b))
        lines.append("".join(string.ascii_letters[z] for z in s))
        return "\n".join(lines) + "\n"

    def convert_output_to_string(output):
        return "".join(string.ascii_letters[x] for x in output)


if __name__ == '__main__':
    import os
    CF831B.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF831B"))
