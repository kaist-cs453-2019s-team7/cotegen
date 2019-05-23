# http://codeforces.com/problemset/problem/263/A

from typing import List

def solve(a: List[List[int]]) -> int:
  for i in range(5):
    for j in range(5):
      if a[i][j] == 1:
        return abs(i - 2) + abs(j - 2)


def compare(user_answer: int, jury_answer: int) -> bool:
  return user_answer == jury_answer