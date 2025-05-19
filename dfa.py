class DFA:
    def __init__(self, states, sigma, transitions, start, final):
        self.states = states
        self.sigma = sigma
        self.transitions = transitions
        self.start = start
        self.final = final

    def simulate_automat(self, input_data: list | str):

        input_data = input_data[::-1]

        state = self.start
        output = ""
        for letter in input_data:
            output += state + " -> "

            if letter not in self.sigma:
                raise ValueError("Invalid input")
            
            if state not in self.transitions[letter]:
                continue

            state = self.transitions[letter][state][0]
        
        output += state

        return output
        
    def is_accepted(self, input_data: list | str):
        state = self.start
        for letter in input_data:
            if letter not in self.sigma:
                return False
            
            if state not in self.transitions[letter]:
                continue
            
            state = self.transitions[letter][state][0]

        return state in self.final