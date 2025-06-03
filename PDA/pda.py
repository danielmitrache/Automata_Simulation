class PDA:
    def __init__(self, states, sigma, gamma, transitions, start, final):
        self.states = states
        self.sigma = sigma
        self.gamma = gamma
        self.transitions = transitions
        self.start = start
        self.final = final

    def _apply_epsilon_closure(self, curr_state, stack):
        """
        Aplica toate tranzitiile epsilon (t1 == 'e') din starea curenta,
        pana cand nu mai exista niciuna aplicabila. Modifica stiva si starea
        conform regulilor epsilon.
        """
        changed = True
        # Continuam ciclul cat timp gasim tranzitii epsilon aplicabile
        while changed:
            changed = False
            curr_transitions = self.transitions.get(curr_state, [])
            for (t1, t2, t3, next_state) in curr_transitions:
                # Verificam doar tranzitiile cu t1 == 'e' (epsilon)
                if t1 == "e":
                    # Verificam conditia pe varful stivei:
                    # t2 == 'e' inseamna nu se cere nimic,
                    # altfel stack[-1] trebuie sa fie t2
                    if t2 == "e" or (stack and stack[-1] == t2):
                        # Aplicam pop daca t2 != 'e'
                        if t2 != "e":
                            stack.pop()
                        # Aplicam push daca t3 != 'e'
                        if t3 != "e":
                            stack.append(t3)
                        # Trecem in noua stare
                        curr_state = next_state
                        changed = True
                        # Deoarece starea si stiva s-au modificat,
                        # putem avea noi tranzitii epsilon disponibile
                        break
        return curr_state, stack

    def is_accepted(self, input_str):
        """
        Verifica daca PDA-ul deterministic accepta sirul de intrare.
        Algoritm:
          1) Pornim cu starea initiala si stiva goala
          2) Aplicam toate tranzitiile epsilon din starea initiala
          3) Pentru fiecare simbol din input, gasim o tranzitie cu t1 == simbol,
             t2 potrivit varfului stivei, aplicam pop/push, schimbam starea,
             apoi aplicam din nou epsilon-closure.
          4) Dupa ce am consumat toate simbolurile, aplicam inca o data epsilon-closure
          5) Acceptam doar daca starea curenta este finala si stiva e goala
        """
        # Pornim cu starea initiala si stiva goala
        curr_state = self.start
        stack = []

        # Aplicam toate tranzitiile epsilon initiale (posibil sa adaugam marcaje)
        curr_state, stack = self._apply_epsilon_closure(curr_state, stack)

        # Parcurgem fiecare caracter din input
        index = 0
        while index < len(input_str):
            symbol = input_str[index]
            # Daca simbolul nu e in sigma (sau e 'e'), respingem
            if symbol not in self.sigma or symbol == "e":
                return False

            curr_transitions = self.transitions.get(curr_state, [])
            found = False
            # Cautam exact o tranzitie cu t1 == simbol si conditia pe varful stivei
            for (t1, t2, t3, next_state) in curr_transitions:
                if t1 == symbol:
                    # Verificam daca se poate face pop de pe stiva (sau t2 == 'e')
                    if t2 == "e" or (stack and stack[-1] == t2):
                        # Aplicam pop daca t2 != 'e'
                        if t2 != "e":
                            stack.pop()
                        # Aplicam push daca t3 != 'e'
                        if t3 != "e":
                            stack.append(t3)
                        # Trecem in starea urmatoare
                        curr_state = next_state
                        found = True
                        break

            # Daca nu am gasit nicio tranzitie valida pentru simbol, respingem
            if not found:
                return False

            # Am consumat simbolul, deci incrementam index si facem epsilon-closure
            index += 1
            curr_state, stack = self._apply_epsilon_closure(curr_state, stack)

        # Dupa consumul intregului input, aplicam inca o data epsilon-closure
        curr_state, stack = self._apply_epsilon_closure(curr_state, stack)

        # Acceptam daca suntem intr-o stare finala si stiva e goala
        return (curr_state in self.final) and (not stack)


# Exemplu de utilizare:
from pda_config_reader import get_config_pda_data
pda = PDA(*get_config_pda_data("config_pda.txt"))

# Testam cateva siruri de intrare
print(pda.is_accepted('111000'))     
print(pda.is_accepted('000111'))     
print(pda.is_accepted('111000111000'))
