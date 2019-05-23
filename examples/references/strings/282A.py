# http://codeforces.com/problemset/problem/282/A

from typing import List

def solve(lines: List[str]):
  X = 0
  for line in lines:
    if line == "X++" or line == "X--":
      X += 1
    else:
      X -= 1
  return X