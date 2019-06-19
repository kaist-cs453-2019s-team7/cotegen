# Coding Test Input Generator

## Adding New Reference Solution

After installing our `cotegen` package, You can write a new reference solution as a simple python file to generate corresponding test cases.

Please locate your reference solution file in `examples/tasks` directory to utilize command line execution.

You should define a new class inherits `cotegen.Task` and with the same with filename. 

`input_parameters`, `solve`(reference solution), `compare`, and `convert_input_to_string` are essential methods to override.

Please refer the example:

```python
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

### Define Input Parameters
Predefine the types of input parameters and the range of each argument as a dictionary format.

Currently, `CoTeGen` supports following types:

```python
cotegen.types.Integer
cotegen.types.IntegerSequence
cotegen.types.NonIncreasingIntegerSequence
cotegen.types.FixedVariableLengthIntegerSequence
cotegen.types.IntegerPermutation
```

### Define constraint

If needed, define the constraints among input parameters as list.
```python
constraints = [
        cotegen.constraints.Leq('M', 'N')
    ]
```

You can utilize these predefined constraints:

```python
cotegen.constraints.Leq (Less than or equal)
cotegen.constraints.ListLengthLeqInteger
cotegen.constraints.ListLengthReqInteger
```

or, use custom constraints giving custom function (which receives parameter dictionary and returns true/false) as an argument

```python
cotegen.constraints.CustomConstraint(lambda test: 'd1' not in test or 'd2' not in test or test['d1'] != test['d2'])
```

## Command Line Usage

```
python -m cotegen run random --filename <filename>

python -m cotegen run mutation --filename <filename> --show-survived <true or false>

python -m cotegen run kill --filename <filename> --save <directory path> --mutation-fitness <true or false>
```

For example:

```
python -m cotegen run random --filename CF158A

python -m cotegen run mutation --filename CF158A

python -m cotegen run kill --filename CF158A --save ~/Downloads --mutation-fitness true
```
