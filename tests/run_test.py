import context
from cotegen.run import MutationRunner

import pytest
import copy
from astor import to_source

from os import listdir
from os.path import isfile, join


path = 'examples/references/integers/'
target_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

def test_mutate():
    for target_file in target_files:
        mutation_runner = MutationRunner(target_file)
        print(target_file)

        original_solve = copy.deepcopy(mutation_runner.target_function)

        mutation_runner.generate_mutations()

        # should not change original `solve` function
        assert to_source(
            original_solve) == to_source(mutation_runner.target_function)

        # should generate mutations diffrent from original
        for mutation in mutation_runner.mutations:
            assert to_source(
                original_solve) != to_source(mutation.ast_node)
