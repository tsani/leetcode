# Dynamic programming solution

"""
What does this 2D DP table mean exactly?
T[i][j] = true
    when the regex obtained from the last `i` characters of the pattern matches
    the string obtained from the last `j` characters of the string.

Goal: grow the table until we find T[len(p)][len(s)]

Therefore:
- T[0][0] = true
    -> the empty pattern matches the empty string.
- T[0][j], j>0 = false
    -> the empty pattern cannot match a nonempty string
- T[i][0], i>0
    | p[len(p)-i] == _:'*' = T[i-1][0]
    | otherwise = False
- T[i][j], i>0, j>0
    | p[len(p)-i] == '.' = T[i-1][j-1]
    | p[len(p)-i] == s[len(s)-j] = T[i-1][j-1]
    | p[len(p)-i] == '.*' = T[i-1][j-1] || T[i][j-1]
    | p[len(p)-i] == c:'*' = (c == s[len(s)-j]) && T[i][j-1] || T[i-1][j-1]
    | otherwise = False
"""

def preprocess(p):
    """Tokenizes a pattern so that starred characters live in their own 'cell'."""
    out = []
    i = 0
    while i < len(p):
        if i + 1 < len(p) and p[i+1] == '*':
            out.append(p[i:i+2])
            i += 1
        else:
            out.append(p[i])
        i += 1
    return out

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        p = preprocess(p)
        T = [[True] + [False] * len(s)]

        for i in range(1, len(p) + 1):
            q = p[len(p)-i]
            T.append([q.endswith('*') and T[i-1][0]])
            for j in range(1, len(s) + 1):
                c = s[len(s)-j]
                if q == '.' or q == c: T[i].append(T[i-1][j-1])
                elif q == '.*': T[i].append(T[i][j-1] or T[i-1][j])
                elif q.endswith('*'): T[i].append(
                    (q[0] == c and T[i][j-1]) or T[i-1][j]
                )
                else: T[i].append(False)

        return T[len(p)][len(s)]

