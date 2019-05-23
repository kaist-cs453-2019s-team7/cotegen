# http://codeforces.com/problemset/problem/935/A

from typing import Tuple

def solve(x1: int, x2: int, x3: int, x4: int) -> Tuple[int, int, int]:
  # 2 <= x_i <= 10**9, answer should be positive
  m = max([x1, x2, x3, x4])
  ret = []
  if x1 < m:
    ret.append(m - x1)
  if x2 < m:
    ret.append(m - x2)
  if x3 < m:
    ret.append(m - x3)
  if x4 < m:
    ret.append(m - x4)
  return tuple(ret)


def compare(user_answer: Tuple[int,int,int], jury_answer: Tuple[int,int,int]) -> bool:
  return sorted(user_answer) == sorted(jury_answer)

