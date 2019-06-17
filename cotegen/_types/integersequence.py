import random

from . import Type

from cotegen.exceptions import CotegenTypeDeclarationError

import itertools

class IntegerSequence(Type):
    _NUM_RANDOM = 5
    _NUM_ELEMENT_BOUNDARY = 2
    _NUM_LENGTH_BOUNDARY = 1
    _MAX_LENGTH = 100000
    _NUM_SMALL_TESTS_BOUND = 10

    def __init__(self, min_length: int = 1, max_length: int = 100000,
                        lower_bound: int = (-2**31), upper_bound: int = (2**31) - 1):
        if type(lower_bound) is not int:
            raise CotegenTypeDeclarationError("lower_bound of Integer type is not an integer")
        if type(upper_bound) is not int:
            raise CotegenTypeDeclarationError("upper_bound of Integer type is not an integer")
        if lower_bound > upper_bound:
            raise CotegenTypeDeclarationError("lower_bound > upper_bound")
        if not(1 <= min_length <= max_length <= IntegerSequence._MAX_LENGTH):
            raise CotegenTypeDeclarationError("not(1 <= min_length <= max_length <= _MAX_LENGTH)")

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.min_length = min_length
        self.max_length = max_length

    def random_length (self, min_length: int, max_length: int):
        return random.randint(min_length, max_length)

    def random_element (self, lower_bound: int, upper_bound: int):
        return random.randint(lower_bound, upper_bound)

    def get_random(self):
        n = self.random_length(self.min_length, self.max_length)
        return [random.randint(self.lower_bound, self.upper_bound) for _ in range(n)]

    def is_valid(self, value, test=None):
        return type(value) is list and self.min_length <= len(value) <= self.max_length and \
                all(self.lower_bound <= x <= self.upper_bound for x in value)

    def sample(self, test=None):
        ret = []
        for n in set(range(self.min_length, self.min_length + self._NUM_LENGTH_BOUNDARY + 1)) \
                    | set(range(self.max_length - self._NUM_LENGTH_BOUNDARY, self.max_length + 1)):
            if n <= 4 and ((self.upper_bound - self.lower_bound + 1) ** n) <= self._NUM_SMALL_TESTS_BOUND:
                ret.extend(map(list, itertools.product(range(self.lower_bound, self.upper_bound + 1), repeat=n)))
                continue

            if self.min_length <= n <= self.max_length:
                for v in range(self.lower_bound, self.lower_bound + self._NUM_ELEMENT_BOUNDARY + 1):
                    ret.append([self.random_element(self.lower_bound, v) for _ in range(n)])
                for v in range(self.upper_bound - self._NUM_ELEMENT_BOUNDARY, self.upper_bound + 1):
                    ret.append([self.random_element(v, self.upper_bound) for _ in range(n)])

        remaining_length_interval = (self.min_length + self._NUM_LENGTH_BOUNDARY + 1,
                                        self.max_length - self._NUM_LENGTH_BOUNDARY - 1)
        remaining_element_interval = (self.lower_bound + self._NUM_ELEMENT_BOUNDARY + 1,
                                        self.upper_bound - self._NUM_ELEMENT_BOUNDARY - 1)

        if remaining_length_interval[0] <= remaining_length_interval[1]:
            for i in range(self._NUM_RANDOM):
                n = self.random_length(*remaining_length_interval)
                ret.append([self.random_element(self.lower_bound, self.upper_bound) for _ in range(n)])

        if remaining_element_interval[0] <= remaining_element_interval[1]:
            for i in range(self._NUM_RANDOM):
                n = self.random_length(self.min_length, self.max_length)
                ret.append([self.random_element(*remaining_element_interval) for _ in range(n)])

        return sorted(filter(self.is_valid, ret))


class NonIncreasingIntegerSequence(IntegerSequence):
    def sample(self, test=None):
        return [sorted(v, reverse=True) for v in super(NonIncreasingIntegerSequence, self).sample()]


class FixedVariableLengthIntegerSequence(IntegerSequence):
    _NUM_RANDOM = 5
    _NUM_ELEMENT_BOUNDARY = 2
    _NUM_LENGTH_BOUNDARY = 1
    _MAX_LENGTH = 100000

    def __init__(self, length_var: str,
                        lower_bound: int = (-2**31), upper_bound: int = (2**31) - 1):
        if type(lower_bound) is not int:
            raise CotegenTypeDeclarationError("lower_bound of Integer type is not an integer")
        if type(upper_bound) is not int:
            raise CotegenTypeDeclarationError("upper_bound of Integer type is not an integer")
        if lower_bound > upper_bound:
            raise CotegenTypeDeclarationError("lower_bound > upper_bound")

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.length_var = length_var

    def sample(self, test):
        self.min_length = test[self.length_var]
        self.max_length = test[self.length_var]
        ret = super(FixedVariableLengthIntegerSequence, self).sample()
        del self.min_length
        del self.max_length
        return ret

    def dependent_variable_names(self):
        return [self.length_var]

    def is_valid(self, value, test=None):
        if test is None:
            return super(FixedVariableLengthIntegerSequence, self).is_valid(value)
        return type(value) is list and len(value) == test.get(self.length_var, -1) and \
                all(self.lower_bound <= x <= self.upper_bound for x in value)
