from collections import defaultdict

class TM:
    def __init__(self, states, sigma, gamma, transitions, blank, start, final):
        self.states = states
        self.sigma = sigma
        self.gamma = gamma
        self.transitions = transitions   # { state: { read_sym: (write_sym, dir, next_state) } }
        self.blank = blank
        self.start = start
        self.final = final

    def print_transitions(self):
        print("Tranziții:")
        print(self.transitions)

    def print_final_tape(self, tape):
        # Gasim toate pozitiile care contin un simbol diferit de blank
        nonblank = [i for i, sym in tape.items() if sym != self.blank]
        if not nonblank:
            # Daca nu avem niciun simbol nenul, aratam un B singur
            print(f"[] B")
            return

        left = min(nonblank)
        right = max(nonblank)

        # Construim sirul
        tape_slice = ''.join(tape[i] for i in range(left, right + 1))

        print(f"Banda (de la {left} la {right}):")
        print(tape_slice)

    def is_accepted(self, input_str: str) -> bool:
        # Construim banda (infinite tape) cu default blank
        tape = defaultdict(lambda: self.blank)
        for i, ch in enumerate(input_str):
            tape[i] = ch

        head = 0
        state = self.start

        step = 0
        while True:
            current_sym = tape[head]

            # Daca suntem intr-o stare finala, acceptam
            if state in self.final:
                return True

            # Daca nu exista vreo tranzitie pentru (state, current_sym), respinge
            if state not in self.transitions or current_sym not in self.transitions[state]:
                return False

            write_sym, direction, next_state = self.transitions[state][current_sym]

            # Scriem pe bandă
            tape[head] = write_sym

            # Mutam capul
            if direction == "R":
                head += 1
            elif direction == "L":
                head -= 1
            # daca e "S", head ramane neschimbat

            # Schimbam starea
            state = next_state

            step += 1
            if step > 100000: # prevenim bucle infinite
                return False
            
    def get_tape(self, input_str: str) -> str:
        """
        Returneaza banda finala dupa procesarea input_str.
        """
        tape = defaultdict(lambda: self.blank)
        for i, ch in enumerate(input_str):
            tape[i] = ch

        head = 0
        state = self.start

        step = 0
        while True:
            current_sym = tape[head]

            if (state in self.final) or (state not in self.transitions or current_sym not in self.transitions[state]):
                break

            write_sym, direction, next_state = self.transitions[state][current_sym]
            tape[head] = write_sym
            if direction == "R":
                head += 1
            elif direction == "L":
                head -= 1

            state = next_state

            step += 1
            if step > 100000: 
                break
        
        nonblank = [i for i, s in tape.items() if s != self.blank]
        if not nonblank:
            return ""  # bandă goală
        left, right = min(nonblank), max(nonblank)
        return ''.join(tape[i] for i in range(left, right+1))            

# Exemplu de utilizare:
from tm_config_reader import get_config_tm_data
tm = TM(*get_config_tm_data("config_tm.txt"))

print(tm.is_accepted("000111"))
print(tm.get_tape("000111"))
print(tm.is_accepted("101010"))
print(tm.get_tape("101010"))
