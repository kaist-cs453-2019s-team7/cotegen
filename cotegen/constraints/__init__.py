class Constraint:
    def is_valid(self, test):
        raise NotImplementedError
    def is_defined(self, test):
        raise NotImplementedError


class BinaryConstraint(Constraint):
    def __init__(self, lhs: str, rhs: str):
        self.lhs = lhs
        self.rhs = rhs

    def is_defined(self, test):
        return set([self.lhs, self.rhs]).issubset(test.keys())


class CustomConstraint(Constraint):
    def __init__(self, func):
        self.func = func
    def is_valid(self, test):
        return self.func(test)
    def is_defined(self, test):
        return True

from .compare_list_to_element import ListLengthLeqInteger, ListLengthReqInteger

from .compare_integers import Leq
