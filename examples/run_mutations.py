import context

from cotegen.run import MutationRunner

import importlib.machinery

if __name__ == "__main__":
    filename = '263A'
    task = importlib.machinery.SourceFileLoader('','examples/references/integers/{}.py'.format(filename)).load_module().__dict__['CF' + filename]

    runner = MutationRunner(task)

    runner.generate_mutations()
    runner.generate_initial_tests()
    runner.execute_mutations()

    runner.print_all_mutants(verbose=True)
