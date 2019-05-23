# http://codeforces.com/problemset/problem/1/A

def solve(n: int, m: int, a: int) -> int:
  # 1 <= n, m, a <= 10**9
  return ((n + (a-1)) // a) * ((m + (a-1)) // a)

def compare(user_answer: int, jury_answer: int) -> bool:
  return user_answer == jury_answer