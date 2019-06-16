import context
from cotegen.run import MutationRunner

import pytest
import copy
from astor import to_source

from os import listdir
from os.path import isfile, join

import importlib.machinery

path = 'examples/references/integers/'
target_files = [(join(path, f), f[:-3]) for f in listdir(path) if isfile(join(path, f))]

def test_mutate():
    for target_file, file_name in target_files:
        task = importlib.machinery.SourceFileLoader('', target_file).load_module().__dict__['CF' + file_name if file_name[:3] != 'BOJ' else file_name]

        mutation_runner = MutationRunner(task)
        print(target_file)

        original_solve = copy.deepcopy(mutation_runner.target_function)

        mutation_runner.generate_mutations()

        # should not change original `solve` function
        assert to_source(
            original_solve) == to_source(mutation_runner.target_function)

        # should generate mutations different from original
        for mutation in mutation_runner.mutations:
            assert to_source(
                original_solve) != to_source(mutation.ast_node)
