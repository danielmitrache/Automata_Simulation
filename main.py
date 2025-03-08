from automat import Automat, get_config_data

INPUT_FILE = "input.txt"
CONFIG_FILE = "config_automat.txt"

with open(INPUT_FILE, "r") as file:
    input_data = file.read()

try:
    config_data = get_config_data(CONFIG_FILE)
except ValueError as e:
    print(e)
    exit(1)

automat = Automat(*config_data)

for input in input_data.split("\n"):
    skip = False

    if ',' in input:
        input = input.split(",") 
        input = [i.strip() for i in input]
    else:
        input = input.strip()

    for i in input:
        if i not in automat.sigma:
            print(f"Invalid input: {input}")
            skip = True
            break

    if skip:
        continue

    print(automat.simulate_automat(input), end = " | ")
    print(automat.is_accepted(input))