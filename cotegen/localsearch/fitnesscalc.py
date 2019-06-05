from .trace import Trace

from typing import List, Tuple

import logging


def normalize(n):
    alpha = 0.001

    return 1.0 - pow(1 + alpha, -n)


class FitnessCalculator():
    def __init__(self, target_function, target_branch):
        self.exec = target_function.exec
        self.target_function = target_function
        self.is_always_reachable = (target_branch[0] == 0)
        self.target_branch = target_branch
        self.nodes_on_path = []

        if self.is_always_reachable:
            return
        
        branch_tree = target_function.branch_tree
        self.nodes_on_path = branch_tree.get_nodes_on_path(target_branch)

    def get_variables(self, args):
        if self.is_always_reachable:
            return (0, 0, 0, 0)

        trace = Trace()

        exec(self.exec, locals(), globals())

        try:
            eval(self.target_function.call(args))
        except (AssertionError, ZeroDivisionError):
            # TODO: ZeroDivisionError is just to avoid the program to be terminated for BOJ2839
            return (10000, 0, 0, 0)

        executed_branches = trace.get_executed_branches()

        for num, result, _, _, _ in executed_branches:
            if (num, result) == self.target_branch:
                return (0, 0, 0, 0)

        approach_level = 0
        for branch_num, branch_type in self.nodes_on_path:
            for num, result, branch_distance, mutation_distance, pmd in executed_branches:
                if branch_num == num and branch_type != result:

                    logging.debug(
                        (branch_num, result, branch_distance, mutation_distance, pmd))

                    return (approach_level, branch_distance, mutation_distance, pmd)

            approach_level += 1

        # no executed branch on target branch path
        return (10000, 0, 0, 0)

    def calculate(self, args):
        approach_level, branch_distance, _, _ = self.get_variables(args)

        return approach_level + normalize(branch_distance)


class MutationFitnessCalculator(FitnessCalculator):
    def calculate(self, args):
        approach_level, branch_distance, mutation_distance, pmd = self.get_variables(
            args)

        reach_dis = 2 * approach_level + normalize(branch_distance)

        mutation_dis = normalize(mutation_distance)

        impact_dis = approach_level + normalize(branch_distance)

        return reach_dis + mutation_dis + impact_dis
