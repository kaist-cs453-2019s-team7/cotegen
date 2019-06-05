import sys

from cotegen.run import MutationRunner, MutantKiller

import importlib.machinery

def print_help():
    print('Usage: python -m cotegen run random --filename <filename>')
    print(
        '       python -m cotegen run mutation --filename <filename> --show-survived <true or false>')
    print(
        '       python -m cotegen run kill --filename <filename>')
    print(
        '       python -m cotegen run kill --filename <filename> --mutation-fitness <true or false>')


def execute():
    if len(sys.argv) < 3:
        print_help()
        exit(1)

    mode = sys.argv[2] # random, mutation, kill
    filename = None
    mutation_fitness = False
    show_survived = False

    index = 3
    while index + 1 < len(sys.argv):
        option = sys.argv[index]
        if option == '-f' or option == '--filename':
            filename = sys.argv[index+1]

        elif option == '-m' or option == '--mutation-fitness':
            mutation_fitness = True if sys.argv[index+1] == 'true' else False

        elif option == '-s' or option == '--show-survived':
            show_survived = True if sys.argv[index+1] == 'true' else False

        else:
            print('unknown option: {}'.format(option))
            print_help()
            exit(1)

        index = index + 2

    classname = filename
    if filename[:3] != 'BOJ':
        classname = 'CF' + filename

    task = importlib.machinery.SourceFileLoader(
        '', 'examples/references/integers/{}.py'.format(filename)).load_module().__dict__[classname]

    runner = MutationRunner(task)

    runner.generate_initial_tests()
    if mode == 'random':
        runner.test_suite.print()
        return
    
    runner.generate_mutations()
    runner.execute_mutations()

    if mode == 'mutation':
        mutations = runner.survived if show_survived else runner.mutations

        for mutation in mutations:
            mutation.print()

        print('{} mutants survived among {}'.format(len(runner.survived), len(runner.mutations)))
        return

    if mode != 'kill':
        return

    mutants_killed = []
    mutants_survived = []

    new_test_suite = runner.test_suite

    for survivor in runner.mutations:
        mutantKiller = MutantKiller(task, survivor, runner.test_suite)
        
        inputs = mutantKiller.generate_sbst_inputs()
        
        if mutation_fitness:
            inputs.extend(mutantKiller.generate_mutation_sbst_inputs())

        generated_test_suite = mutantKiller.generate_new_test_suite(inputs)
        new_test_suite.add(generated_test_suite)
    
    new_test_suite.print()
    
    for survivor in runner.mutations:
        test_result, _ = new_test_suite.run(survivor.ast_node)
        if test_result == 'SUCCESS':
            mutants_survived.append(survivor)
        elif test_result == 'FAIL':
            mutants_killed.append(survivor)

    print('Killed: {}, Survived: {}'.format(
        len(mutants_killed), len(mutants_survived)))
    


    


if __name__ == "__main__":
    execute()
