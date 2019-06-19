# Coding Test Input Generator

## Adding New Reference Solution

After installing our `cotegen` package, You can write a new reference solution to generate corresponding test cases.

You should define a new class inherits `cotegen.Task` and with the same with filename. 

`input_parameters`, `solve`(reference solution), `compare`, and `convert_input_to_string` are essential methods to override.

Please refer the example:

```
import cotegen

# http://codeforces.com/problemset/problem/1/A

class CF1A(cotegen.Task):
    input_parameters = \
        {
            'n': cotegen.types.Integer(1, 10**9),
            'm': cotegen.types.Integer(1, 10**9),
            'a': cotegen.types.Integer(1, 10**9),
        }

    def solve(n: int, m: int, a: int) -> int:
        # 1 <= n, m, a <= 10**9
        return ((n + (a-1)) // a) * ((m + (a-1)) // a)

    @staticmethod
    def compare(user_answer: int, jury_answer: int) -> bool:
        return user_answer == jury_answer

    @staticmethod
    def convert_input_to_string(n: int, m: int, a: int):
        return "%d %d %d\n" % (n, m, a)


if __name__ == '__main__':
    import os
    CF1A.generate_test_files(os.path.expanduser("~/Downloads/CS453/CF1A"))

```

## Usage
```
python -m cotegen run random --filename <filename>

python -m cotegen run mutation --filename <filename> --show-survived <true or false>

python -m cotegen run kill --filename <filename> --save <directory path> --mutation-fitness <true or false>
```