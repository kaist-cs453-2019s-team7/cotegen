# http://codeforces.com/problemset/problem/791/A

from typing import List

def solve(a: int, b: int) -> int:
  # 1 <= a <= b <= 10
  for i in range(100):
    if a > b:
      return i
    a *= 3
    b *= 2
  assert False


def compare(user_answer: int, jury_answer: int) -> bool:
  return user_answer == jury_answer

