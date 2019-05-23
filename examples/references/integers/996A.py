# http://codeforces.com/problemset/problem/935/A

from typing import List

def solve(n: int) -> int:
  # 1 <= n <= 10**9
  ret = 0
  for bill in [100, 20, 10, 5, 1]:
    if n >= bill:
      cnt = n // bill
      ret += cnt
      n -= bill * cnt
  assert n == 0
  return ret


def compare(user_answer: int, jury_answer: int) -> bool:
  return user_answer == jury_answer

