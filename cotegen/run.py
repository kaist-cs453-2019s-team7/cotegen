import astor
from cotegen.mutate import Mutator

def get_solve_function(target_file):
  body = list(astor.iter_node(target_file))[0][0]

  for functionDef in body:
    if functionDef.name == 'solve':
      return functionDef

if __name__ == "__main__":
  target_file = astor.code_to_ast.parse_file('examples/references/integers/4A.py')
  target_function = get_solve_function(target_file)

  mutator = Mutator(target_function)
  mutator.walk()

  # should print mutated function
  print(astor.to_source(mutator.get_mutation()))

  # should print original function
  print(astor.to_source(target_function))