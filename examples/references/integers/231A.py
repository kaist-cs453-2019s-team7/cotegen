# http://codeforces.com/problemset/problem/231/A

from typing import List

def solve(a: List[int], b: List[int], c: List[int]) -> int:
  ret = 0
  n = len(a)
  for i in range(n):
    if a[i] + b[i] + c[i] >= 2:
      ret += 1
  return ret


def compare(user_answer: int, jury_answer: int) -> bool:
  return user_answer == jury_answer