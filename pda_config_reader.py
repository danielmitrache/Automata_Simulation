import re

def get_config_pda_data(config_file):
    with open(config_file, "r") as file:
        config_data = file.read()

    config_data = re.sub(r"#.*", "", config_data)

    patterns = {
        "states": r"\[States\](.*?)\[/States\]",
        "sigma": r"\[Sigma\](.*?)\[/Sigma\]",
        "gamma": r"\[Gamma\](.*?)\[/Gamma\]",
        "transitions": r"\[Transitions\](.*?)\[/Transitions\]",
        "start": r"\[Start\](.*?)\[/Start\]",
        "final": r"\[Final\](.*?)\[/Final\]"
    }

    extracted_data = {}

    for key, pattern in patterns.items():
        try:
            extracted_data[key] = re.findall(pattern, config_data, re.DOTALL)[0].strip()
        except IndexError:
            extracted_data[key] = None
        if not extracted_data[key]:
            raise ValueError(f"Invalid config file: {key} not found")
        
    states = [s.strip() for s in extracted_data["states"].split(",")]
    sigma = [l.strip() for l in extracted_data["sigma"].split(",")]
    gamma = [l.strip() for l in extracted_data["gamma"].split(",")]
    if "e" not in sigma:
        sigma += ["e"]
    if "e" not in gamma:
        gamma += ["e"]
    start = extracted_data["start"].strip()
    final = [s.strip() for s in extracted_data["final"].split(",")]

    transitions = extracted_data["transitions"].split(";")
    transitions = [t.strip() for t in transitions]
    transitions = [tuple([x.strip() for x in t.split(",")]) for t in transitions]

    rules = {}
    for transition in transitions:
        if len(transition) != 5:
            continue
        
        curr_state, _, _, _, next_state = transition

        if curr_state not in rules:
            rules[curr_state] = {}

        rules[curr_state][next_state] = tuple(transition[1:4])

    return states, sigma, gamma, rules, start, final
        