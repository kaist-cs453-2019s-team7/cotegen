# http://codeforces.com/problemset/problem/4/A


def solve(x: int) -> int:
  # 1 <= x <= int(1e6)
  if x % 5 >= 1:
    return x // 5 + 1
  else:
    return x // 5


def compare(user_answer: int, jury_answer: int) -> bool:
  return user_answer == jury_answer