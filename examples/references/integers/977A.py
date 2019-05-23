# http://codeforces.com/problemset/problem/977/A


def solve(n: int, k: int) -> int:
  # 2 <= n <= 10**9, 1 <= k <= 50
  # answer > 0 (hard-to-satisfy condition)
  ans = n
  for _ in range(k):
    if ans % 10 == 0:
      ans = ans // 10
    else:
      ans -= 1
  return ans


def compare(user_answer: int, jury_answer: int) -> bool:
  return user_answer == jury_answer