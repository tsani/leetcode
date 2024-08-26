# NFA: use numbered states. The NFA itself therefore consists of list. Indexing
# into the list gives us the information for a state.
# At an index L, we need to know what transitions are possible, and what
# letters (if any) are required. Therefore L[i] is a list of tuples.
# Epsilon-moves are allowed by using the string ''.

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        nfa = []

        i = 0
        while i < len(p):
            state = []
            if i + 1 < len(p) and p[i+1] == '*':
                state.append( (0, len(nfa) + 1) )
                state.append( (ord(p[i]), len(nfa)) )
                i += 1
            else:
                state.append( (ord(p[i]), len(nfa) + 1) )
            nfa.append(state)
            i += 1

        nfa.append( [] )
        # add one empty state at the end to act as the accept state

        return run(nfa, s)

def run(nfa, s):
    def epsilon_close(reachable, state):
        """Adds the epsilon closure of the given state (the set of states
        reachable using only epsilon-moves) to the given set."""
        for (t, s_prime) in nfa[state]:
            if t == 0:
                reachable |= (1 << s_prime)
                reachable = epsilon_close(reachable, s_prime)
        return reachable

    live_states = 1 # only state 0 is live at first
    live_states = epsilon_close(live_states, 0) # ... plus its epsilon-closure

    for letter in s:
        new_states = 0
        state_index = 0
        while live_states > 0:
            if live_states & 1 > 0:
                for (t, s_prime) in nfa[state_index]:
                    if t == 46 or t == ord(letter): # ord('.') = 46
                        new_states |= (1 << s_prime)
                        new_states = epsilon_close(new_states, s_prime)

            state_index += 1
            live_states = live_states >> 1
        live_states = new_states

    return live_states >> (len(nfa) - 1) > 0
