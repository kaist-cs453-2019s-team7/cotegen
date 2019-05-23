# http://codeforces.com/problemset/problem/4/A

def solve(w: int) -> str:
  # 1 <= w <= 100
  if w >= 4 and w % 2 == 0:
    return "YES"
  else:
    return "NO"

def compare(user_answer: str, jury_answer: str) -> bool:
  return user_answer.strip().lower() == jury_answer.strip().lower()