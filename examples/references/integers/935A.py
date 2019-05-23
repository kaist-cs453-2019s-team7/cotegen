# http://codeforces.com/problemset/problem/935/A

from typing import List

def solve(n: int) -> int:
  # 2 <= n <= int(1e5)
  ret = 0
  for i in range(1, n):
    if n % i == 0:
      ret = ret + 1
  return ret


def compare(user_answer: int, jury_answer: int) -> bool:
  return user_answer == jury_answer

