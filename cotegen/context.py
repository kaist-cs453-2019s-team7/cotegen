from typing import List, Tuple

import cotegen.ast_utils as ast_utils

from enum import Enum


class Status(Enum):
    UNEXECUTED = 0
    SURVIVED = 1
    KILLED = 2


class Context():
    def __init__(self, mutation):
        self.mutation = mutation
        self.ID = None
        self.status = Status.UNEXECUTED
        self.killed_by = []

    def execute(self, test_suite):
        self.status = Status.SURVIVED
        result = test_suite.run(self.mutation)

        if result == 'FAIL':
            self.status = Status.KILLED
            self.killed_by = test_suite.failed_tests

    def print(self, verbose=True):
        print(self.status)
        if self.status == Status.KILLED:
            print('KILLED BY:')
            print(self.killed_by)

        if verbose:
            ast_utils.print_ast(self.mutation)

        print('\n')
