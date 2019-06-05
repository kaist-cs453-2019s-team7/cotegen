import cotegen.localsearch.distance_functions as df
import cotegen.localsearch.mutation_distance_functions as mdf

import ast
import astor


class Trace():
    def __init__(self):
        self.executed_branches = []

    def get_executed_branches(self):
        return self.executed_branches

    def is_true(self, id, exp):
        result = self.equals(id, exp, True)
        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.equals_bool(exp, False)

        else:
            distance_true = distance_to_alternative = df.equals_bool(
                exp, True)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, 0, 0))

        return result

    def is_false(self, id, exp):
        result = self.equals(id, exp, False)
        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.equals_bool(
                exp, True)

        else:
            distance_true = distance_to_alternative = df.equals_bool(
                exp, False)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, 0, 0))

        return result

    def equals(self, id, lhs, rhs):
        result = lhs == rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.not_equals_num(
                lhs, rhs)

        else:
            distance_false = distance_to_alternative = df.equals_num(lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, 0, 0))

        return result

    def not_equals(self, id, lhs, rhs):
        result = lhs != rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.equals_num(lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.not_equals_num(
                lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, 0, 0))

        return result

    def less_than(self, id, lhs, rhs):
        result = lhs < rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.greater_than_or_equals(
                lhs, rhs)

        else:
            distance_false = distance_to_alternative = df.less_than(lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, 0, 0))
        return result

    def less_than_or_equals(self, id, lhs, rhs):
        result = lhs <= rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.greater_than(
                lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.less_than_or_equals(
                lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, 0, 0))

        return result

    def greater_than(self, id, lhs, rhs):
        result = lhs > rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.less_than_or_equals(
                lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.greater_than(
                lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, 0, 0))

        return result

    def greater_than_or_equals(self, id, lhs, rhs):
        result = lhs >= rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.less_than(lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.greater_than_or_equals(
                lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, 0, 0))

        return result

    def bool_or(self, id, lhs, rhs):
        result = lhs[0] or rhs[0]

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = lhs[1] + rhs[1]

        else:
            distance_true = distance_to_alternative = min(lhs[1], rhs[1])
        
        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, 0, 0))

        return result

    def bool_and(self, id, lhs, rhs):
        result = lhs[0] and rhs[0]

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = min(lhs[1], rhs[1])

        else:
            distance_true = distance_to_alternative = lhs[1] + rhs[1]

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, 0, 0))

        return result


    '''
    Mutation Fitness
    '''

    def mutated_equals(self, id, lhs, rhs):
        result = lhs == rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.not_equals_num(lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.equals_num(lhs, rhs)

        mutation_distance = mdf.NEq_to_Eq(lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, 0))

        return result

    def mutated_not_equals(self, id, lhs, rhs):
        result = lhs != rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.equals_num(lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.not_equals_num(lhs, rhs)

        mutation_distance = mdf.Eq_to_NEq(lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, 0))

        return result

    def mutated_less_than(self, id, lhs, rhs):
        result = lhs < rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.greater_than_or_equals(lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.less_than(lhs, rhs)

        mutation_distance = mdf.LtE_to_Lt(lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, 0))
        return result

    def mutated_less_than_or_equals(self, id, lhs, rhs):
        result = lhs <= rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.greater_than(lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.less_than_or_equals(lhs, rhs)

        mutation_distance = mdf.Lt_to_LtE(lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, 0))

        return result

    def mutated_greater_than(self, id, lhs, rhs):
        result = lhs > rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.less_than_or_equals(lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.greater_than(lhs, rhs)

        mutation_distance = mdf.GtE_to_Gt(lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, 0))

        return result

    def mutated_greater_than_or_equals(self, id, lhs, rhs):
        result = lhs >= rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.less_than(lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.greater_than_or_equals(lhs, rhs)

        mutation_distance = mdf.Gt_to_GtE(lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, 0))

        return result

    def mutated_or(self, id, lhs, rhs):
        result = lhs[0] or rhs[0]

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = lhs[1] + rhs[1]

        else:
            distance_true = distance_to_alternative = min(lhs[1], rhs[1])

        lhs_true, lhs_false = lhs[2:]
        rhs_true, rhs_false = rhs[2:]

        mutation_distance = min(lhs_true + rhs_false, lhs_false + rhs_true)

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, 0))
        
        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        return result

    def mutated_and(self, id, lhs, rhs):
        result = lhs[0] and rhs[0]

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = min(lhs[1], rhs[1])

        else:
            distance_true = distance_to_alternative = lhs[1] + rhs[1]

        lhs_true, lhs_false = lhs[2:]
        rhs_true, rhs_false = rhs[2:]

        mutation_distance = min(lhs_true + rhs_false, lhs_false + rhs_true)

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, 0))

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        return result
