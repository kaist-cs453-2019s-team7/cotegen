import sys

from cotegen.context import Status

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

    mode = sys.argv[2]  # random, mutation, kill
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

    task = importlib.machinery.SourceFileLoader(
        '', 'examples/tasks/{}.py'.format(filename)).load_module().__dict__[classname]

    if mode == 'random':
        initial_test_suite = task.generate_random_tests()
        initial_test_suite.print()
        return

    elif mode == 'mutation':
        initial_test_suite = task.generate_random_tests()
        mutations = task.mutate(initial_test_suite)

        survived = list(filter(lambda m: m.status ==
                                Status.SURVIVED, mutations))
        
        if show_survived:
            for mutation in survived:
                mutation.print()

        else:
            for mutation in mutations:
                mutation.print()

        print('{} mutants survived among {}'.format(
            len(survived), len(mutations)))
        return

    elif mode == 'kill':
        mutants_killed = []
        mutants_survived = []

        new_test_suite, mutations = task.kill_survived_mutants(
            mutation_fitness=mutation_fitness)
        new_test_suite.print()
        print(len(new_test_suite.tests))

        for mutant in mutations:
            test_result, _, _ = new_test_suite.run(mutant.ast_node)
            if test_result == 'SUCCESS':
                mutants_survived.append(mutant)
            elif test_result == 'FAIL':
                mutants_killed.append(mutant)

        print('Killed: {}, Survived: {}'.format(
            len(mutants_killed), len(mutants_survived)))


if __name__ == "__main__":
    execute()
