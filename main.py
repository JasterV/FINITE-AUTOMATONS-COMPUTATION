from automaton import FA
from os import system, name
import json


def clear():
    # for windows
    if name == 'nt':
        system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        system('clear')


def show_options():
    print("D => Determinize automat")
    print("M => Minimize automat")
    print("read => Read a word")
    print("show => Show automat")
    print("clear => Clear screen")
    print("help => Show commands")
    print("quit => Close program")


if __name__ == '__main__':
    try:
        filename = input("Enter the automaton json filepath: ")
        fp = open(filename, 'r')
        automaton_json = json.load(fp)
        automat = FA(automaton_json)
        show_options()
        while True:
            option = input(">> ").lower()
            if option == 'd':
                if automat.is_deterministic():
                    print("This automaton is already determinized")
                    continue
                automat.determinize()
            elif option == 'm':
                automat.minimize()
            elif option == 'read':
                word = input("Enter the word you want to read: ")
                automat.read(word)
            elif option == 'show':
                automat.show()
            elif option == 'clear':
                clear()
            elif option == 'help':
                show_options()
            elif option == 'quit':
                print("Bye!")
                break
            else:
                print("Command not recognized")
    except OSError as err:
        print("OSError:", err)
    except ValueError as err:
        print("ValueError:", err)
    except TypeError as err:
        print("TypeError:", err)
