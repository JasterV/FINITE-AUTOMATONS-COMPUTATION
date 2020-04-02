from collections.abc import Iterable
from queue import Queue

empty_set = u"\u00F8"
lmbda = u"\u03BB"


class FiniteAutomaton():
    def __init__(self, json: dict):
        try:
            states = json["states"]
            alphabet = json["alphabet"]
            transitions = json["transitions"]
        except Exception:
            raise ValueError(
                "The json file must have the keys 'states', 'alphabet' and 'transitions'")
        self.__assert_states(states)
        self.__assert_alphabet(alphabet)
        self.__assert_transitions(transitions, alphabet, states)
        # Create all the Automaton Attributes
        self.__states = set(states.keys())
        self.__initial_states = set(
            filter(lambda state: 'I' in states[state], states))
        self.__final_states = set(
            filter(lambda state: 'F' in states[state], states))
        self.__alphabet = set(alphabet)
        self.__transitions = transitions

    # -----------------------------------------------------
    # ----------------- PUBLIC METHODS --------------------
    # -----------------------------------------------------

    def determinize(self):
        """ This method determinize the automata
        using BFS algorithm with a Queue
        """
        queue = Queue()
        transitions = dict()
        initial_state = tuple(self.__initial_states)
        queue.put(initial_state)
        print("Determinizing automaton... ")
        while not queue.empty():
            curr_state = queue.get()
            if curr_state not in transitions:
                transitions[curr_state] = dict()
                for symbol in self.__alphabet:
                    next_state = self.__get_next_state(curr_state, symbol)
                    if next_state == empty_set:
                        if empty_set not in transitions:
                            self.__add_empty_set(transitions)
                    transitions[curr_state][symbol] = [next_state]
                    queue.put(next_state)
        self.__states = set(transitions.keys())
        self.__initial_states = {initial_state}
        self.__final_states = set(
            filter(lambda state: self.__is_final_state(state), transitions.keys()))
        self.__transitions = transitions
        print("Automaton determinized! Press 'S' to see the changes\n")

    def read(self, word):
        """ Represents word reading
        """
        if not self.is_deterministic():
            print("\nThis automaton is non-deterministic")
            self.determinize()
        init_state = list(self.__initial_states)[0]
        print("Reading word...")
        self.__read(word, init_state)

    def minimize(self):
        if not self.is_deterministic():
            print("\nThis automaton is non-deterministic")
            self.determinize()
        # TODO: IMPLEMENT MINIMIZATION
        pass

    def show(self):
        print(f"    States => {self.__states}")
        print(f"    Initial states => {self.__initial_states}")
        print(f"    Final states => {self.__final_states}")
        print("\n    Transitions map => ")
        for state, transition in self.__transitions.items():
            print(f"        {state} =>")
            for symbol, dest in transition.items():
                print(f"            with {symbol} => {dest}")

    def is_deterministic(self):
        if len(self.__initial_states) > 1:
            return False
        for transition in self.__transitions.values():
            for states in transition.values():
                if len(states) != 1:
                    return False
        return True

    # -----------------------------------------------------
    # ----------------- PRIVATE METHODS -------------------
    # -----------------------------------------------------

    def __read(self, word, state):
        if len(word) < 1 or word == lmbda:
            if state in self.__final_states:
                print("WORD ACCEPTED")
            else:
                print("WORD NOT ACCEPTED")
            return
        symbol = word[0]
        if symbol not in self.__alphabet:
            print(f"SYMBOL {symbol} NOT RECOGNIZED => WORD NOT ACCEPTED")
            return
        next_state = self.__transitions[state][symbol][0]
        next_word = lmbda if len(word) <= 1 else word[1:]
        print(
            f"\t({state}, {word}) => ({next_state}, {next_word})")
        self.__read(next_word, next_state)

    def __get_next_state(self, curr_state, symbol):
        new_state = set()
        for state in curr_state:
            new_state.update(set(self.__transitions[state][symbol]))
        if len(new_state) == 0:
            return empty_set
        return tuple(new_state)

    def __add_empty_set(self, transitions):
        transitions[empty_set] = dict()
        for letter in self.__alphabet:
            transitions[empty_set][letter] = [empty_set]

    def __is_final_state(self, t):
        for elem in t:
            if elem in self.__final_states:
                return True
        return False

    # ------------ ASSERTS --------------
    def __assert_states(self, states):
        if not isinstance(states, dict):
            raise TypeError("Bad states type, has to be a map")
        has_initial = False
        has_final = False
        for value in states.values():
            if not isinstance(value, list):
                raise TypeError("Bad states value, has to be a list")
            if 'I' in value:
                has_initial = True
            if 'F' in value:
                has_final = True
        if not has_initial:
            raise ValueError("States map doesn't has an initial state")
        if not has_final:
            raise ValueError("States map does not has a final state")

    def __assert_alphabet(self, alphabet):
        if not isinstance(alphabet, list):
            raise TypeError("Bad alphabet type, has to be a list")

    def __assert_transitions(self, transitions, alphabet, states):
        if not isinstance(transitions, dict):
            raise TypeError("Bad transitions format, has to be a map")
        # Check if each state is defined in transitions map
        for s in states:
            if s not in transitions:
                raise ValueError(f"State {s} not defined on transitions table")
        # Check the transitions map format
        for state in transitions:
            # Check if each state is in the states map
            if state not in states:
                raise ValueError(
                    f"State {state} in transitions map not defined in states map")
            # Check the transition object type
            transition = transitions[state]
            if not isinstance(transition, dict):
                raise TypeError(
                    f"Transaction value {transition} has to be a symbol-states map")
            # Check if each state has defined a behaviour for each symbol in the alphabet
            for symbol in alphabet:
                if symbol not in transition.keys():
                    raise ValueError(
                        f"Symbol {symbol} behaviour not defined in state {state}, each symbol has to be defined even if its value is an empty list.")
            # Check the transition map content
            for symbol, dest in transition.items():
                # Check if each symbol is in the alphabet
                if symbol not in alphabet:
                    raise ValueError(
                        f"Symbol {symbol} in state {state} transition is not in the alphabet")
                # Check the destination states object type
                if not isinstance(dest, Iterable):
                    raise TypeError(
                        f"Value {dest} in transitions table has to be an Iterable")
                # Check if each state in destination list is in the states map
                for s in dest:
                    if s not in states:
                        raise ValueError(
                            f"State {s} in {dest} not in states map")
