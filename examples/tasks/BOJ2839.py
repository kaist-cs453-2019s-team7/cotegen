import cotegen


class BOJ2839(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(1, 10**9),
        }

    output_type = int

    def solve(n: int) -> int:
        if n % 5 == 0:
            return n // 5
        elif n % 5 == 3:
            return (n - 3) // 5 + 1
        elif n >= 6 and n % 5 == 1:
            return (n - 6) // 5 + 2
        elif n >= 9 and n % 5 == 4:
            return (n - 9) // 5 + 3
        elif n >= 12 and n % 5 == 2:
            return (n - 12) // 5 + 4
        return -1

    def compare(user_answer: int, jury_answer: int):
        return user_answer == jury_answer


if __name__ == '__main__':
    print(BOJ2839.generate_random_tests())
