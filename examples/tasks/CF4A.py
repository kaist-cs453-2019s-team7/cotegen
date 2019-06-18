import cotegen

# http://codeforces.com/problemset/problem/4/A

class CF4A(cotegen.Task):
    input_parameters = \
        {
            'w': cotegen.types.Integer(1, 100),
        }

    output_type = str

    def solve(w: int) -> str:
        if w >= 4 and w % 2 == 0:
            return "YES"
        else:
            return "NO"

    def compare(user_answer: str, jury_answer: str) -> bool:
        return user_answer == jury_answer

    def convert_input_to_string(w: int) -> str:
        return "%d\n" % w



if __name__ == '__main__':
    import os
    CF4A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF4A"))
