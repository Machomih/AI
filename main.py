# Ex 1: Pentru reprezentarea unei instante vom folosi un array unidimensional in care fiecare element reprezinta
#        o celula a matricii."
#        state = [1,2,3,4,5,6,7,8,0] -> fiecare element  reprezinta o celula a matricii, 0 fiind celula goala
#        Ordinea elementelor in array reprezinta si ordinea elementelor in matrice. Este mult mai usor sa prelucra,
#        datele problemei astfel pentru scrierea si rezolvarea algoritmului.

# Ex 2: Starea initiala este reprezentata de o asezare random a celulelor cu o celula goala. Pentru a obtine starea initiala,
#        trebuie sa punem intr-un mod aleatoriu numerele de la 1 la 8 intr o matrice, o celula fiind populata de 0, reprezentand
#        celula goala.
#       Starea finala este reprezentata de aranjamentul celulelor in ordine crescatoare, ignorand celula goala, cea populata de 0.

import random


# def initialize_puzzle():

# initializam lista si adaugam celula goala
#   numbers = list(range(1, 9))
#    numbers.append(0)

# amestecam elemente intr o ordine aleatorie pentru a obtine starea initiala a problemei
#    random.shuffle(numbers)

#    return numbers


def is_final_state(state):
    final_states = [[1, 2, 3, 4, 5, 6, 7, 8, 0],
                    [1, 2, 3, 4, 5, 6, 7, 0, 8],
                    [1, 2, 3, 4, 5, 6, 0, 7, 8],
                    [1, 2, 3, 4, 5, 0, 6, 7, 8],
                    [1, 2, 3, 4, 0, 5, 6, 7, 8],
                    [1, 2, 3, 0, 4, 5, 6, 7, 8],
                    [1, 2, 0, 3, 4, 5, 6, 7, 8],
                    [1, 0, 2, 3, 4, 5, 6, 7, 8],
                    [0, 1, 2, 3, 4, 5, 6, 7, 8]]

    for final_state in final_states:
        if state == final_state:
            return True
    return False


# initial_state = initialize_puzzle()

# print("The initial form of the puzzle is: ", initial_state)

# if is_final_state(initial_state):
#   print("The initial state is  the final state.")
# else:
#   print("The initial state is not the final state.")


# Ex 3 si 4: Vom defini 4 functii de miscare (move_up, move_down, move_left si move_right) dupa care vom defini o functie de control
#       ce ne va spune daca o miscare intr o anumita directie este valida


def empty_cell_location(state):
    return state.index(0)


# functia de control ce valideaza o miscare
def validation_move(direction, state):
    empty_cell = empty_cell_location(state)

    if direction == "up":
        if empty_cell >= 3:  # verificam daca celula goala nu  este in bottom line
            return True
        else:
            return False
    elif direction == "down":
        if empty_cell < 6:  # Verificam daca celula goala nu este in top line
            return True
        else:
            return False
    elif direction == "right":
        if empty_cell % 3 != 2:  # Verificam daca celula goala nu este in coloana cea mai din dreapta
            return True
        else:
            return False
    elif direction == "left":
        if empty_cell % 3 != 0:  # Verificam daca celula goala nu e in coloana cea mai din stanga
            return True
        else:
            return False

    else:
        return False


def move_up(state):
    if not validation_move("up", state):
        return state

    empty_cell = empty_cell_location(state)
    updated_state = state[:]
    # daca scriam updated_state = state, aveam doua variabile ce pointau spre aceeasi lista in memorie
    updated_state[empty_cell] = state[empty_cell - 3]  # schimbam celula goala cu cea de sub ea
    updated_state[empty_cell - 3] = 0

    return updated_state


def move_down(state):
    if not validation_move("down", state):
        return state

    empty_cell = empty_cell_location(state)
    updated_state = state[:]
    updated_state[empty_cell] = state[empty_cell + 3]
    updated_state[empty_cell + 3] = 0

    return updated_state


def move_right(state):
    if not validation_move("right", state):
        return state

    empty_cell = empty_cell_location(state)
    updated_state = state[:]
    updated_state[empty_cell] = state[empty_cell + 1]
    updated_state[empty_cell + 1] = 0

    return updated_state


def move_left(state):
    if not validation_move("left", state):
        return state

    empty_cell = empty_cell_location(state)
    updated_state = state[:]
    updated_state[empty_cell] = state[empty_cell - 1]
    updated_state[empty_cell - 1] = 0

    return updated_state


def iddfs(initial_state):
    max_depth = 1

    while True:
        visited_states = set()  # Initialize a set to keep track of visited states at each depth.
        result = depth_limit_search(initial_state, max_depth, visited_states)
        if result is not None:
            return result
        max_depth = max_depth + 1


def depth_limit_search(state, depth_limit, visited_states):
    return depth_limit_search_rec(state, depth_limit, 0, [], visited_states)


def depth_limit_search_rec(state, depth_limit, depth, path, visited_states):
    if depth == depth_limit:
        return None

    if is_final_state(state):
        return path

    visited_states.add(tuple(state))  # Convert the state to a tuple and add it to the visited states set.

    for direction in ["up", "left", "down", "right"]:
        if direction == "up":
            new_state = move_up(state)
        elif direction == "down":
            new_state = move_down(state)
        elif direction == "left":
            new_state = move_left(state)
        elif direction == "right":
            new_state = move_right(state)

        if new_state != state and tuple(new_state) not in visited_states:
            print(new_state)
            result = depth_limit_search_rec(new_state, depth_limit, depth + 1, path + [direction], visited_states)
            if result is not None:
                return result

    visited_states.remove(tuple(state))  # Remove the state from the visited states set when backtracking.



#EX:5 Inceput
def manhattan(stare, stare_finala):

    distanta = 0
    for val in stare:
        if val == 0:
            continue
        poz_curenta = stare.index(val)
        poz_finala = stare_finala.index(val)
        distanta += abs(poz_curenta // 3 - poz_finala // 3) + abs(poz_curenta % 3 - poz_finala % 3)

    return  distanta

def hamming(stare, stare_finala):
    gresite = 0
    for val, final in zip(stare, stare_finala):
        if val != final and val != 0:
            gresite += 1

    return  gresite
def piese_gresite(stare, stare_finala):
    gresite = 0
    for val, final in zip(stare, stare_finala):
        if val != final:
            gresite += 1

    return gresite
def greedy(stare, euristica, stare_finala):
    steps = 0
    while not is_final_state(stare):
        pos_moves = []
        for direction in ["up", "down", "left", "right"]:
            if direction == "up" and validation_move(direction,stare) is not False:
                euris_val = euristica(move_up(stare),stare_finala)
                pos_moves.append((direction,euris_val))
            elif direction == "down" and validation_move(direction,stare) is not False:
                euris_val = euristica(move_down(stare), stare_finala)
                pos_moves.append((direction, euris_val))
            elif direction == "left" and validation_move(direction,stare) is not False:
                euris_val = euristica(move_left(stare), stare_finala)
                pos_moves.append((direction, euris_val))
            elif direction == "right" and validation_move(direction,stare) is not False:
                euris_val = euristica(move_right(stare), stare_finala)
                pos_moves.append((direction, euris_val)) #pos_moves = [(direction, euris_val), (direction, euris_val)...]

        if not pos_moves:
            return None #ne am blocat, nu exista mutari posibile

        pos_moves.sort(key=lambda x: x[1]) #sortam dupa euris_val
        mutare, _ = pos_moves[0] # mutare primeste primul tuplu din pos_moves, mai exact doar functia de directie, ignorand a doua val din tuplu
        if mutare == "up":
            stare = move_up(stare)
        elif mutare == "down":
            stare = move_down(stare)
        elif mutare == "left":
            stare = move_left(stare)
        elif mutare == "right":
            stare = move_right(stare)

        steps += 1

euristici = [manhattan,hamming,piese_gresite]
initial_state = [2, 5, 3, 1, 0, 6, 4, 7, 8]
stare_finala = [1,2,3,4,5,6,7,8,0]

for euristica in euristici:
    result = greedy(initial_state, euristica, stare_finala)
    if result is not None:
        print(f"Euristica: {euristica.__name__}")
        print(f"Nr de pasi necesari: {result}")

    else:
        print(f"Euristica: {euristica.__name__}")
        print("No solution found")  #EX5 FINAL


#solution_path = iddfs(initial_state) #Linia asta si cu aia de jos, sunt apelul ca sa rezolvam cu iddfs pt ex 4.
#print(solution_path)