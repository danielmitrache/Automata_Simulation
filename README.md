# Automata Simulation

Simulate [automatons](https://en.wikipedia.org/wiki/Automata_theory) using their config files. <br>
The project includes [DFA](https://en.wikipedia.org/wiki/Deterministic_finite_automaton), [NFA](https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton), [PDA](https://en.wikipedia.org/wiki/Deterministic_pushdown_automaton) and [Turing Machine](https://en.wikipedia.org/wiki/Turing_machine). <br>
Setup:
```bash
git clone <repo link>
cd <repo>

cd <DFA/NFA/PDA/TM> # Choose which automaton to test

# Edit desired config file and test different inputs
# Run with py -3 / python3 
```
Once you clone this repo, select one of the folders containing the names of the 4 automatons. There, you will find a configuration file where you can describe your own automaton. Also, you can add comments with '#'. From there, you can test the automaton directly in the python file containing it's name, or you can import the class together with the config reader to any project and use it from there.

