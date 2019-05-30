from . import BinaryConstraint


class Leq(BinaryConstraint):
    def is_valid(self, test):
        return test[self.lhs] <= test[self.rhs]
