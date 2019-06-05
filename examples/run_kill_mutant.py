import context
import astor
from cotegen.run import MutationRunner, MutantKiller

import importlib.machinery

# Survived mutants in 617, 791, 4, 977

# 158, 263: List


if __name__ == "__main__":
    filename = 'BOJ2839'
    task = importlib.machinery.SourceFileLoader('','examples/references/integers/{}.py'.format(filename)).load_module().__dict__[filename]

    runner = MutationRunner(task)

    runner.generate_mutations()
    runner.generate_initial_tests()
    runner.execute_mutations()

    # runner.branch_tree.print()
    count = 0
    for survivor in runner.mutations:
        mutantKiller = MutantKiller(task, survivor, runner.test_suite)
        print('*********')
        print(astor.to_source(mutantKiller.mutated_function.node))

        sbst_inputs = mutantKiller.generate_sbst_inputs()
        mutation_inputs = mutantKiller.generate_mutation_sbst_inputs()

        sbst_test_suite = mutantKiller.generate_new_test_suite(sbst_inputs)
        test_result, _ = sbst_test_suite.run(survivor.ast_node)
        
        mutation_test_suite = mutantKiller.generate_new_test_suite(mutation_inputs)
        test_result_mut, _ = mutation_test_suite.run(survivor.ast_node)

        
        def change(result):
            if result == 'FAIL':
                return 'KILLED'
            elif result =='SUCCESS':
                return 'SURVIVED'
        if test_result == 'SUCCESS' and test_result_mut == 'FAIL':
            count += 1

        print('SBST:{}, mutation:{}\n'.format(change(test_result), change(test_result_mut)))

    
    print('mutation fitness did extra job for {} times'.format(count))


