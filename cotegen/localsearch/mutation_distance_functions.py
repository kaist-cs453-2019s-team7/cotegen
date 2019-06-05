
K = 1.0


def GtE_to_Gt(lhs, rhs):
    return abs(lhs - rhs)


def Gt_to_GtE(lhs, rhs):
    return abs(lhs - rhs)


def LtE_to_Lt(lhs, rhs):
    return abs(lhs - rhs)


def Lt_to_LtE(lhs, rhs):
    return abs(lhs - rhs)


def Eq_to_NEq(lhs, rhs):
    return 0


def NEq_to_Eq(lhs, rhs):
    return 0

def and_to_or(lhs, rhs):
    if lhs > rhs:
        return 0

    return (rhs - lhs) + K


def or_to_and(lhs, rhs):
    if lhs >= rhs:
        return 0

    return (rhs - lhs) + K
