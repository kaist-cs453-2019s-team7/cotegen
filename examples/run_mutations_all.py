import context

from cotegen.run import MutationRunner

from os import listdir
from os.path import isfile, join

import importlib.machinery


path = 'examples/references/integers/'
target_files = [(join(path, f), f[:-3])
                for f in listdir(path) if isfile(join(path, f))]


if __name__ == "__main__":
    for target_file, file_name in target_files:
        task = importlib.machinery.SourceFileLoader(
            '', target_file).load_module().__dict__['CF' + file_name]

        runner = MutationRunner(task)

        runner.generate_mutations()
        runner.generate_initial_tests()
        runner.execute_mutations()

        # only print cases with survived mutants
        mutations_count = len(runner.mutations)
        survived_count = runner.count_survived_mutants()

        if survived_count > 0:
            print('target: {}'.format(file_name))
            print('{} mutants survived among {}'.format(survived_count, mutations_count))
            runner.print_survived_mutants(verbose=True)
