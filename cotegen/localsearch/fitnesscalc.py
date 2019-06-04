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

    def get_args_count(self):
        return self.target_function.args_count

    def calculate(self, args):
        if self.is_always_reachable:
            return 0

        trace = Trace()

        exec(self.exec, locals(), globals())

        eval(self.target_function.call(args))

        executed_branches = trace.get_executed_branches()

        for num, result, distance in executed_branches:
            if (num, result) == self.target_branch:
                return 0

        approach_level = 0
        for branch_num, branch_type in self.nodes_on_path:
            for num, result, distance_to_alternative in executed_branches:
                if branch_num == num and branch_type != result:
                    
                    logging.debug((branch_num, result, distance_to_alternative))

                    return normalize(distance_to_alternative) + approach_level

            approach_level += 1
        
        # no executed branch on target branch path
        return 10000
