import context

import pytest
import copy
import astor

from cotegen.mutate import Mutator
from cotegen.task import Task
from cotegen.run import get_solve_function

def test_mutate():
    target_file = astor.code_to_ast.parse_file(
        'examples/references/integers/4A.py')
    target_function = get_solve_function(target_file)
    target_function_copy = copy.deepcopy(target_function)

    mutator = Mutator(target_function)
    mutator.apply_mutations()

    assert astor.to_source(
        target_function_copy) == astor.to_source(mutator.target)
    assert len(mutator.mutations) > 0
