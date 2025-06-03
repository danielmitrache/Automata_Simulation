import re

def get_config_tm_data(config_file):
    with open(config_file, "r") as f:
        content = f.read()

    # Eliminăm comentariile (# … până la sfârșit de linie)
    content = re.sub(r"#.*", "", content)

    patterns = {
        "states": r"\[States\](.*?)\[/States\]",
        "sigma": r"\[Sigma\](.*?)\[/Sigma\]",
        "gamma": r"\[Gamma\](.*?)\[/Gamma\]",
        "blank": r"\[Blank\](.*?)\[/Blank\]",
        "transitions": r"\[Transitions\](.*?)\[/Transitions\]",
        "start": r"\[Start\](.*?)\[/Start\]",
        "final": r"\[Final\](.*?)\[/Final\]"
    }

    extracted = {}
    for key, pat in patterns.items():
        m = re.findall(pat, content, re.DOTALL)
        if not m or not m[0].strip():
            raise ValueError(f"Secțiunea '{key}' lipsește sau e goală")
        extracted[key] = m[0].strip()

    # 1. States
    states = [s.strip() for s in extracted["states"].split(",") if s.strip()]

    # 2. Sigma (alfabetul de intrare)
    sigma = [s.strip() for s in extracted["sigma"].split(",") if s.strip()]

    # 3. Gamma (alfabetul benzii)
    gamma = [g.strip() for g in extracted["gamma"].split(",") if g.strip()]

    # 4. Blank (simbolul pentru spațiile goale de pe bandă)
    blank = extracted["blank"].strip()
    if blank not in gamma:
        raise ValueError(f"Simbolul Blank '{blank}' nu apare în [Gamma]")

    # 5. Transitions (separăm după punct și virgulă)
    raw_trans = [line.strip() for line in extracted["transitions"].split(";") if line.strip()]
    transitions = {}
    # vom construi un dicționar de forma:
    #   transitions[stare_curentă] = { simbol_citit: (simbol_scris, direcție, stare_următoare), … }

    for line in raw_trans:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 5:
            raise ValueError(f"Linie de tranziție invalidă: '{line}' (trebuie 5 câmpuri)")
        src, read_sym, write_sym, direction, dst = parts

        # validări de existență în listele corespunzătoare
        if src not in states:
            raise ValueError(f"Stare '{src}' din tranziții nu există în [States]")
        if dst not in states:
            raise ValueError(f"Stare '{dst}' din tranziții nu există în [States]")
        if read_sym not in gamma:
            raise ValueError(f"Simbol citit '{read_sym}' nu există în [Gamma]")
        if write_sym not in gamma:
            raise ValueError(f"Simbol scris '{write_sym}' nu există în [Gamma]")
        if direction not in ("L", "R", "S"):
            raise ValueError(f"Direcție invalidă '{direction}'; trebuie L, R sau S")

        # în dict, la cheia src, adăugăm un sub‐dicționar:
        if src not in transitions:
            transitions[src] = {}
        if read_sym in transitions[src]:
            raise ValueError(f"Tranziție dublă pentru ({src}, {read_sym})")

        transitions[src][read_sym] = (write_sym, direction, dst)

    # 6. Start
    start = extracted["start"].strip()
    if start not in states:
        raise ValueError(f"Stare de start '{start}' nu există în [States]")

    # 7. Final
    final = [s.strip() for s in extracted["final"].split(",") if s.strip()]
    for f in final:
        if f not in states:
            raise ValueError(f"Stare finală '{f}' nu există în [States]")

    return states, sigma, gamma, transitions, blank, start, final
