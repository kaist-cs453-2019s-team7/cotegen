class Type:
    def get_random(self):
        raise NotImplementedError
    def is_valid(self, value, test=None):
        raise NotImplementedError
    def sample(self, test=None):
        raise NotImplementedError
    def dependent_variable_names(self):
        return []

from .integer import Integer
from .integersequence import IntegerSequence, NonIncreasingIntegerSequence, FixedVariableLengthIntegerSequence, IntegerPermutation
