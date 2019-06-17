import context
from cotegen.task import Task
from cotegen.context import Status
from cotegen.kill import MutantKiller

import importlib.machinery

# Survived mutants in 617, 791, 4, 977

# 158, 263: List


if __name__ == "__main__":
    filename = 'BOJ2839'
    task = importlib.machinery.SourceFileLoader('','examples/references/integers/{}.py'.format(filename)).load_module().__dict__[filename]

    initial_test_suite = task.generate_random_tests()
    mutations = task.mutate(initial_test_suite)

    survived = list(filter(lambda m: m.status ==
                           Status.SURVIVED, mutations))

    count = 0
    for survivor in mutations:
        mutantKiller = MutantKiller(task, survivor, initial_test_suite)

        print('*********')
        mutantKiller.mutated_function.print()

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


