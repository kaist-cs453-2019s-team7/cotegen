import context
import astor
from cotegen.run import MutationRunner, MutantKiller

import importlib.machinery

# Survived mutants in 617, 791, 4, 977

# 158, 263: List


if __name__ == "__main__":
    filename = '617A'
    task = importlib.machinery.SourceFileLoader('','examples/references/integers/{}.py'.format(filename)).load_module().__dict__['CF' + filename]

    runner = MutationRunner(task)

    runner.generate_mutations()
    runner.generate_initial_tests()
    runner.execute_mutations()

    # runner.branch_tree.print()

    for survivor in runner.mutations:
        mutantKiller = MutantKiller(task, survivor, runner.test_suite)
        print('*********')
        print(astor.to_source(mutantKiller.mutated_function.node))

        sbst_inputs = mutantKiller.generate_sbst_inputs()
        mutation_inputs = mutantKiller.generate_mutation_sbst_inputs()

        print('\nSBST:')
        mutantKiller.generate_new_test_suite(sbst_inputs)
        print('\nmutation:')
        mutantKiller.generate_new_test_suite(mutation_inputs)
        print('\n')


    # TODO: new_input들에 대해 mutant를 kill 시키는지 확인

