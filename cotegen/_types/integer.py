import random

from . import Type
from cotegen.exceptions import CotegenTypeDeclarationError

class Integer(Type):
    _NUM_RANDOM = 5
    _BOUNDARY = 2

    def __init__(self, lower_bound: int = (-2**31), upper_bound: int = (2**31) - 1):
        if type(lower_bound) is not int:
            raise CotegenTypeDeclarationError("lower_bound of Integer type is not an integer")
        if type(upper_bound) is not int:
            raise CotegenTypeDeclarationError("upper_bound of Integer type is not an integer")
        if lower_bound > upper_bound:
            raise CotegenTypeDeclarationError("lower_bound > upper_bound")
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_random(self):
        return random.randint(self.lower_bound, self.upper_bound)

    def is_valid(self, value, test=None):
        return self.lower_bound <= value <= self.upper_bound

    def sample(self, test=None):
        ret = []
        for v in range(self.lower_bound, self.lower_bound + Integer._BOUNDARY + 1):
            ret.append(v)
        for v in range(self.upper_bound - Integer._BOUNDARY, self.upper_bound + 1):
            ret.append(v)

        remaining_interval = (self.lower_bound + Integer._BOUNDARY + 1,
                                self.upper_bound - Integer._BOUNDARY - 1)
        if remaining_interval[0] <= remaining_interval[1]:
            for i in range(Integer._NUM_RANDOM):
                ret.append(random.randint(*remaining_interval))

        return sorted(set(filter(self.is_valid, ret)))
