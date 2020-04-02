# FINITE AUTOMATONS COMPUTATION

A program that runs finite automatons and operate with them (reading, determinizing and minimizing). 
I'm working on automaton algebra operations such as concatenation, union and intersection. ^^

To work with the program you need to create a json file with the automaton settings.

The json must contains the following attributes:

    + states -> A map whose keys are the label of the state 
                and whose values are a list with each type
                corresponding to the state.
                The types are: 'I' for initial states,
                               'F' for final states,
                               'N' for non-initial and non-final states.
    + alphabet -> A list with each symbol accepted by the automaton.
    + transitions -> A map whose keys are the label of the state
                    and whose values are another map that represents
                    each transition for each symbol for the corresponding state.

                    The transition map must have as key a valid symbol on the alphabet
                    and as value a list of the states the corresponding state goes with that symbol.
