import re

def get_config_data(config_file):
    with open(config_file, "r") as file:
        config_data = file.read()

    # Preprocessing the data (removing comments)
    config_data = re.sub(r"#.*", "", config_data)

    patterns = {
        "states": r"\[States\](.*?)\[/States\]",
        "sigma": r"\[Sigma\](.*?)\[/Sigma\]",
        "transitions": r"\[Transitions\](.*?)\[/Transitions\]",
        "start": r"\[Start\](.*?)\[/Start\]",
        "final": r"\[Final\](.*?)\[/Final\]"
    }

    extracted_data = {}

    for key, pattern in patterns.items():
        extracted_data[key] = re.findall(pattern, config_data, re.DOTALL)[0].strip()

    # Extracting states
    states = extracted_data["states"].split(",")
    states = [state.strip() for state in states]

    # Extracting sigma
    sigma = extracted_data["sigma"].split(",")
    sigma = [s.strip() for s in sigma]

    # Extracting transitions
    transitions_unp = extracted_data["transitions"].split(";")
    transitions_unp = [t.strip() for t in transitions_unp]
    transitions_unp = [tuple(t.split(",")) for t in transitions_unp]
    transitions = []
    for t in transitions_unp:
        tpl = []
        for i in t:
            tpl.append(i.strip())
        transitions.append(tuple(tpl)) if len(tpl) == 3 else None

    # Extracting start state
    start = extracted_data["start"].strip()

    # Extracting final states
    final = extracted_data["final"].split(",")
    final = [f.strip() for f in final]


    # Making a dictionary (key = letter) of dictionaries (key = current state) of rules (current state -> next state)
    rules = {}
    for letter in sigma:
        rules[letter] = {}
    for t in transitions:
        rules[t[1]][t[0]] = t[2]

    return states, sigma, rules, start, final

class Automat:
    def __init__(self, states, sigma, transitions, start, final):
        self.states = states
        self.sigma = sigma
        self.transitions = transitions
        self.start = start
        self.final = final

    def simulate_automat(self, input_data):
        state = self.start
        for cnt, letter in enumerate(input_data[::-1]):
            
            if cnt == len(input_data) - 1:
                print(state, end="\n")
            else:
                print(state + ' -> ', end="")

            if letter not in self.sigma:
                raise ValueError("Invalid input")
            state = self.transitions[letter][state]
        
    def is_accepted(self, input_data):
        state = self.start
        for letter in input_data[::-1]:
            if letter not in self.sigma:
                return False
            state = self.transitions[letter][state]
        return state in self.final