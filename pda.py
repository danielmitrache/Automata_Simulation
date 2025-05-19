from pda_config_reader import get_config_pda_data

pda_config = get_config_pda_data("config_pda.txt")

class PDA:
    def __init__(self, states, sigma, gamma, transitions, start, final):
        self.states = states
        self.sigma = sigma
        self.gamma = gamma
        self.transitions = transitions
        self.start = start
        self.final = final

    def is_accepted(self, input_data: list | str):
        stack = []
        curr_state = self.start

        for ch in input_data:
            if ch not in self.sigma:
                return False
            
            tansition = self.transitions