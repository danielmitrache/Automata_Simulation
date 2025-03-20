class NFA:
    def __init__(self, states, sigma, transitions, start, final):
        self.states = states
        self.sigma = sigma
        self.transitions = transitions
        self.start = start
        self.final = final


    def is_accepted(self, input_data: list | str):

        #input_data = input_data[::-1]

        state = self.start

        queue = [(state, input_data)]
        while queue:
            state, input_data = queue.pop(0)
            print(state, input_data)
            if state in self.final and not input_data:
                return True
            
            if self.transitions.get("e"):
                for next_state in self.transitions["e"].get(state, []):
                    if (next_state, input_data) not in queue:
                        queue.append((next_state, input_data))

            for i, letter in enumerate(input_data):
                if letter not in self.sigma:
                    return False
                
                if state not in self.transitions[letter]:
                    continue
                
                for next_state in self.transitions[letter][state]:
                    if (next_state, input_data[i + 1:]) not in queue:
                        queue.append((next_state, input_data[i + 1:]))

        return False