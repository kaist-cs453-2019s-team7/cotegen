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
        return user_answer.strip().lower() == jury_answer.strip().lower()


if __name__ == '__main__':
    print(CF4A.generate_tests())
