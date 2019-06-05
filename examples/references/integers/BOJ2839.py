import cotegen


class BOJ2839(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(1, 10**9),
        }

    output_type = int

    def solve(n: int) -> int:
        for i in range(5): # i: number of 3kg weights
            if n >= 3 * i and (n - 3 * i) % 5 == 0:
                return (n - 3 * i) // 5 + i
        return -1

    def compare(user_answer: int, jury_answer: int):
        return user_answer == jury_answer


if __name__ == '__main__':
    print(BOJ2839.generate_tests())
