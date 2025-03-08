import re

with open("config_automat.txt", "r") as file:
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

with open("input.txt", "r") as file:
    input_data = file.read()

# Preprocessing the data (removing comments)
input_data = re.sub(r"#.*", "", input_data)

inputs = input_data.split("\n")
