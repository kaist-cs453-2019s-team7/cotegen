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
            distance_false = distance_to_alternative = df.equals_bool(
                exp, False)

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
            distance_false = distance_to_alternative = df.not_equals_num(
                lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.equals_num(lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        mutation_distance = mdf.NEq_to_Eq(lhs, rhs)

        original_distance_true, original_distance_false = self.not_equals(None, lhs, rhs)[
            2:]

        pmd = min(original_distance_true + distance_false,
                  original_distance_false, distance_true)

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, pmd))

        return result

    def mutated_not_equals(self, id, lhs, rhs):
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

        mutation_distance = mdf.Eq_to_NEq(lhs, rhs)

        original_distance_true, original_distance_false = self.equals(None, lhs, rhs)[
            2:]

        pmd = min(original_distance_true + distance_false,
                  original_distance_false, distance_true)

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, pmd))

        return result

    def mutated_less_than(self, id, lhs, rhs):
        result = lhs < rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.greater_than_or_equals(
                lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.less_than(lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        mutation_distance = mdf.LtE_to_Lt(lhs, rhs)

        original_distance_true, original_distance_false = self.less_than_or_equals(None, lhs, rhs)[
            2:]

        pmd = min(original_distance_true + distance_false,
                  original_distance_false, distance_true)

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, pmd))
        return result

    def mutated_less_than_or_equals(self, id, lhs, rhs):
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

        mutation_distance = mdf.Lt_to_LtE(lhs, rhs)

        original_distance_true, original_distance_false = self.less_than(None, lhs, rhs)[
            2:]

        pmd = min(original_distance_true + distance_false,
                  original_distance_false, distance_true)

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, pmd))

        return result

    def mutated_greater_than(self, id, lhs, rhs):
        result = lhs > rhs

        distance_to_alternative = 0

        distance_true = 0
        distance_false = 0

        if result:
            distance_false = distance_to_alternative = df.less_than_or_equals(
                lhs, rhs)

        else:
            distance_true = distance_to_alternative = df.greater_than(lhs, rhs)

        if id == None:
            return result, distance_to_alternative, distance_true, distance_false

        mutation_distance = mdf.GtE_to_Gt(lhs, rhs)

        original_distance_true, original_distance_false = self.greater_than_or_equals(None, lhs, rhs)[
            2:]

        pmd = min(original_distance_true + distance_false,
                  original_distance_false, distance_true)

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, pmd))

        return result

    def mutated_greater_than_or_equals(self, id, lhs, rhs):
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

        mutation_distance = mdf.Gt_to_GtE(lhs, rhs)

        original_distance_true, original_distance_false = self.greater_than(None, lhs, rhs)[
            2:]

        pmd = min(original_distance_true + distance_false,
                  original_distance_false, distance_true)

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, pmd))

        return result

    def mutated_bool_or(self, id, lhs, rhs):
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

        lhs_true, lhs_false = lhs[2:]
        rhs_true, rhs_false = rhs[2:]

        mutation_distance = min(lhs_true + rhs_false, lhs_false + rhs_true)

        original_distance_true, original_distance_false = self.bool_and(None, lhs, rhs)[
            2:]

        pmd = min(original_distance_true + distance_false,
                  original_distance_false, distance_true)

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, pmd))


        return result

    def mutated_bool_and(self, id, lhs, rhs):
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
            
        lhs_true, lhs_false = lhs[2:]
        rhs_true, rhs_false = rhs[2:]

        mutation_distance = min(lhs_true + rhs_false, lhs_false + rhs_true)

        original_distance_true, original_distance_false = self.bool_or(None, lhs, rhs)[
            2:]

        pmd = min(original_distance_true + distance_false,
                  original_distance_false, distance_true)

        self.executed_branches.append(
            (id, result, distance_to_alternative, mutation_distance, pmd))


        return result


def inject_trace_hook(compare_node, branch_id, mutation=False):
    op = ''
    lhs = ''
    rhs = ''
    f_call = ''

    if isinstance(compare_node, ast.Call) and compare_node.func.value.id == 'trace':
        return compare_node

    if isinstance(compare_node, ast.BoolOp):
        lhs = astor.to_source(compare_node.values[0]).rstrip()
        rhs = astor.to_source(compare_node.values[1]).rstrip()
        # TODO: handle <3 values in boolop?

        if isinstance(compare_node.op, ast.And):
            op = 'bool_and'
        elif isinstance(compare_node.op, ast.Or):
            op = 'bool_or'

        if mutation:
            op = 'mutated_' + op

        f_call = 'trace.{fname}({branch_id}, {lhs}, {rhs})'.format(
            fname=op, branch_id=branch_id, lhs=lhs, rhs=rhs)

        f_call_node = ast.parse(f_call, '', 'eval').body

        f_call_node.args[1] = inject_trace_hook(
            f_call_node.args[1], None)
        f_call_node.args[2] = inject_trace_hook(
            f_call_node.args[2], None)

        return f_call_node

    elif not hasattr(compare_node, 'left') or not hasattr(compare_node, 'comparators'):
        op = 'is_true'
        arg = astor.to_source(compare_node).rstrip()

        if mutation:
            op = 'mutated_' + op

        f_call = 'trace.{fname}({branch_id}, {arg})'.format(
            fname=op, branch_id=branch_id, arg=arg)

    else:
        lhs = astor.to_source(compare_node.left).rstrip()
        rhs = astor.to_source(compare_node.comparators[0]).rstrip()

        if isinstance(compare_node.ops[0], ast.Gt):
            op = 'greater_than'
        elif isinstance(compare_node.ops[0], ast.GtE):
            op = 'greater_than_or_equals'
        elif isinstance(compare_node.ops[0], ast.Lt):
            op = 'less_than'
        elif isinstance(compare_node.ops[0], ast.LtE):
            op = 'less_than_or_equals'
        elif isinstance(compare_node.ops[0], ast.Eq):
            op = 'equals'
        elif isinstance(compare_node.ops[0], ast.NotEq):
            op = 'not_equals'
        else:
            return compare_node

        if mutation:
            op = 'mutated_' + op

        f_call = 'trace.{fname}({branch_id}, {lhs}, {rhs})'.format(
            fname=op, branch_id=branch_id, lhs=lhs, rhs=rhs)

    f_call_node = ast.parse(f_call, '', 'eval').body

    return f_call_node
