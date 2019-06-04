import context
import astor
from cotegen.run import MutationRunner, MutantKiller

import importlib.machinery


if __name__ == "__main__":
    filename = '4A'
    task = importlib.machinery.SourceFileLoader('','examples/references/integers/{}.py'.format(filename)).load_module().__dict__['CF' + filename]

    runner = MutationRunner(task)

    runner.generate_mutations()
    runner.generate_initial_tests()
    runner.execute_mutations()

    # runner.branch_tree.print()

    for survivor in runner.survived:
        mutantKiller = MutantKiller(task, survivor, runner.test_suite)
        new_inputs = mutantKiller.generate_sbst_inputs()
        print(new_inputs)

    # TODO: new_input들에 대해 mutant를 kill 시키는지 확인

