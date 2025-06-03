class DFA:
    def __init__(self, states, sigma, transitions, start, final):
        self.states = states
        self.sigma = sigma
        self.transitions = transitions
        self.start = start
        self.final = final

    def simulate_automat(self, input_data: list | str) -> str:
        state = self.start
        output = ""

        for letter in input_data:
            # Adauga starea curenta în traseu
            output += state + " -> "

            # Daca simbolul nu face parte din alfabet, error
            if letter not in self.sigma:
                raise ValueError(f"Invalid input symbol: {letter}")

            # Daca nu exista nicio tranzitie pentru (state, letter), ramanem in starea curenta
            if state not in self.transitions.get(letter, {}):
                continue

            # Obtinem urmatoarea stare
            state = self.transitions[letter][state][0]

        # Adauga starea finala la sfarsitul traseului
        output += state
        return output

    def is_accepted(self, input_data: list | str) -> bool:
        state = self.start

        for letter in input_data:
            # Daca simbolul nu exista în alfabet, automat respinge
            if letter not in self.sigma:
                return False

            # Daca nu exista tranzitie pentru (state, letter), ramanem în starea curentă
            if state not in self.transitions.get(letter, {}):
                continue

            # Trecem la starea următoare
            state = self.transitions[letter][state][0]

        # Acceptam daca starea finala se afla in lista de stari de acceptare
        return state in self.final


# Exemplu de utilizare:
from dfa_config_reader import get_config_dfa_data
dfa = DFA(*get_config_dfa_data("config_dfa.txt"))


print(dfa.is_accepted("1001011")) 
print(dfa.is_accepted("10010110"))
