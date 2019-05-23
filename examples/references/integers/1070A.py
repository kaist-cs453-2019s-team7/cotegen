# http://codeforces.com/problemset/problem/1070/A

from typing import List

def solve(a: List[int]) -> str:
  # 1 <= len(a) <= 100, 0 <= a[i] <= 1
  for x in a:
    if x == 1:
      return "HARD"
  return "EASY"


def compare(user_answer: str, jury_answer: str) -> bool:
  return user_answer.strip().lower() == jury_answer.strip().lower()