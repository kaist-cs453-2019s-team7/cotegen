# http://codeforces.com/problemset/problem/71/A

from typing import List

def solve(a: List[str]) -> List[str]:
  ret = []
  for word in a:
    if len(word) <= 10:
      new_word = word
    else:
      new_word = word[0] + str(len(word) - 2) + word[-1]
    ret.append(new_word)
  return ret
