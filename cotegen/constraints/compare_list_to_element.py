from . import BinaryConstraint


class ListLengthLeqInteger(BinaryConstraint):
    def is_valid(self, test):
        return len(test[self.lhs]) <= test[self.rhs]


class ListLengthReqInteger(BinaryConstraint):
    def is_valid(self, test):
        return len(test[self.lhs]) >= test[self.rhs]
