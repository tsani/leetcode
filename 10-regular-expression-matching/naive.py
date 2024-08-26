# This solution is not pretty.
# It uses a recursive CPS backtracking approach that wastes a lot of
# memory creating lambdas. The implementation of `Seq` is also pretty bad.
# To get around pathological backtracking regexes such as a*a*a*a*b, I added an
# ad hoc optimization to collapse equal Star nodes in a Seq. If the regexes
# supported parentheses this optimization would not work!
# A better approach is to 'inline' all the matching logic into one while loop
# and to use d17n to store a list of 'frames' to jump back to when we need to
# backtrack.
# An even better approach is probably to implement the Thomson construction to
# construct a DFA from the regex.

class Backtrack(Exception):
    pass

class Star:
    def __init__(self, inner):
        self._inner = inner

    def match(self, s, i, next):
        try:
            return self._inner.match(s, i, lambda i: self.match(s, i, next))
        except Backtrack:
            return next(i)

    def __eq__(self, other):
        return isinstance(other, Star) and self._inner == other._inner

class Seq:
    def __init__(self, inners):
        self._inners = inners

    def match(self, s, i, next, j=0):
        if j == len(self._inners): return next(i)
        return self._inners[j].match(s, i, lambda i: self.match(s, i, next, j+1))

class Letter:
    def __init__(self, c):
        self._c = c

    def match(self, s, i, next):
        if i < len(s) and (self._c == '.' or self._c == s[i]): return next(i+1)
        raise Backtrack()

    def __eq__(self, other):
        return isinstance(other, Letter) and self._c == other._c

def compile(p):
    seq = []
    i = 0
    # plus little optimization to collapse adjacent stars of the same letter
    while i < len(p):
        if i + 1 < len(p) and p[i+1] == '*':
            r = Star(Letter(p[i]))
            if not len(seq) or not (seq[-1] == r): seq.append(r)
            i += 1
        else:
            seq.append(Letter(p[i]))
        i += 1

    return Seq(seq)


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        r = compile(p)
        try:
            return len(s) == r.match(s, 0, lambda i: i)
        except Backtrack:
            return False

if __name__ == '__main__':
    s = Solution()
    print(s.isMatch('mississippi', 'mis*is*ip*.'))
