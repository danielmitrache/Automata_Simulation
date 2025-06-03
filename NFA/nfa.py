from collections import deque

class NFA:
    def __init__(self, states, sigma, transitions, start, final):
        self.states = states
        self.sigma = sigma
        self.transitions = transitions
        self.start = start
        self.final = final

    def _epsilon_closure(self, state_set):
        """
        Calculeaza multimea de stari accesibile prin orice numar de epsilon-tranzitii,
        pornind din state_set.
        """
        closure = set(state_set)
        stack = list(state_set)

        while stack:
            q = stack.pop()
            for nxt in self.transitions.get("e", {}).get(q, []):
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
        return closure

    def is_accepted(self, input_str):
        """
        Verifica daca NFA-ul accepta input_str.
        Algoritm: BFS pe configuratii (stare_curenta, rest_de_citit),
                  cu epsilon-closure la fiecare pas.
        """
        # Pornim cu epsilon-closure({start}) si coada initiala
        current = self._epsilon_closure({self.start})
        queue = deque((q, input_str) for q in current)
        visited = set(queue)

        while queue:
            state, rest = queue.popleft()

            # Daca suntem in stare finala si nu mai avem input, acceptam
            if state in self.final and rest == "":
                return True

            # Extindem cu toate tranzitiile epsilon din state
            for nxt in self.transitions.get("e", {}).get(state, []):
                cfg = (nxt, rest)
                if cfg not in visited:
                    visited.add(cfg)
                    queue.append(cfg)

            # Daca mai exista simbol de consumat, il luam pe primul
            if rest:
                letter = rest[0]
                # Daca simbolul nu e in alfabet sau e 'e', nu se consuma
                if letter not in self.sigma or letter == "e":
                    continue
                # Pentru fiecare tranzitie pe letter din state
                for nxt in self.transitions.get(letter, {}).get(state, []):
                    new_rest = rest[1:]
                    # Calculam epsilon-closure pe noua stare
                    closure_nxt = self._epsilon_closure({nxt})
                    for q2 in closure_nxt:
                        cfg2 = (q2, new_rest)
                        if cfg2 not in visited:
                            visited.add(cfg2)
                            queue.append(cfg2)

        # Daca s-a golit coada fara acceptare, respingem
        return False


# Exemplu de utilizare:
from nfa_config_reader import get_config_nfa_data
nfa = NFA(*get_config_nfa_data("config_nfa.txt"))

# Testam un sir de intrare (exemplu)
print(nfa.is_accepted("111000101"))
print(nfa.is_accepted("111011"))
