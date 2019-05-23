# http://codeforces.com/problemset/problem/50/A

def solve(M: int, N: int) -> int:
  # 1 <= M <= N <= 16
  return M * N // 2

def compare(user_answer: int, jury_answer: int) -> bool:
  return user_answer == jury_answer