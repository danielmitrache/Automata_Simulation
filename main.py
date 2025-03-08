from automat import Automat, get_config_data

INPUT_FILE = "input.txt"
CONFIG_FILE = "config_automat.txt"

with open(INPUT_FILE, "r") as file:
    input_data = file.read()

automat = Automat(*get_config_data(CONFIG_FILE))

for input in input_data.split("\n"):
    print(automat.simulate_automat(input), end = " | ")
    print(automat.is_accepted(input))