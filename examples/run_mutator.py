from cotegen.run import MutationRunner

if __name__ == "__main__":
    import importlib.machinery
    task = importlib.machinery.SourceFileLoader('','references/integers/158A.py').load_module().CF158A

    runner = MutationRunner(task)

    runner.generate_mutations()
    runner.generate_initial_tests()
    runner.execute_mutations()

    runner.print_all_mutants()
