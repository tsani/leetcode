def trieify(words):
    """Represent a trie as nested dicts, one char at a time.
    Use an empty string key to represent end-of-string."""
    trie = {}
    if len(words) == 0: return trie
    for w in words:
        if '' == w:
            trie[''] = {}
            continue # sus but works
        start, rest = w[0], w[1:]
        ws = trie.get(start, [])
        ws.append(rest)
        trie[start] = ws
    # now trie maps chars to lists of words starting with that char
    for c, ws in trie.items():
        trie[c] = trieify(ws) # turn each of those into a trie in turn
    return trie

class Solution(object):
    def findWords(self, board, words):
        """
        :type board: List[List[str]]
        :type words: List[str]
        :rtype: List[str]
        """
        # equip each character in the board with a bool indicating whether we
        # visited it
        self.board = [
            [ (c, False) for c in row ]
            for row in board
        ]

        self.height = len(board)
        self.width = len(board[0])

        trie = trieify(words)

        words = []
        for i in range(self.height):
            for j in range(self.width):
                self.go(words, (i, j), '', trie)
        return words


    def go(self, words, (i, j), prefix, trie):
        if '' in trie:
            words.append(prefix)
            del trie[''] # avoids finding same word multiple ways/times

        if len(trie) == 0: return
        if i < 0 or i >= self.height or j < 0 or j >= self.width: return

        (c, visited) = self.board[i][j]
        if visited: return
        if c not in trie: return
        subtrie = trie[c]

        self.board[i][j] = (c, True)
        self.go(words, (i+1, j), prefix + c, subtrie)
        self.go(words, (i-1, j), prefix + c, subtrie)
        self.go(words, (i, j+1), prefix + c, subtrie)
        self.go(words, (i, j-1), prefix + c, subtrie)
        self.board[i][j] = (c, False)

        if len(subtrie) == 0:
            del trie[c] # further prune the trie if possible
