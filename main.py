from dfa import DFA
from nfa import NFA
from configreader import get_config_data

INPUT_FILE = "input.txt"
CONFIG_FILE = "config_automat.txt"

with open(INPUT_FILE, "r") as file:
    input_data = file.read()

try:
    config_data = get_config_data(CONFIG_FILE)
except ValueError as e:
    print(e)
    exit(1)

print(*config_data)

dfa = NFA(*config_data)

for input in input_data.split("\n"):
    skip = False

    if ',' in input:
        input = input.split(",") 
        input = [i.strip() for i in input]
    else:
        input = input.strip()

    for i in input:
        if i not in dfa.sigma:
            print(f"Invalid input: {input}")
            skip = True
            break

    if skip:
        continue

    print(dfa.is_accepted(input))