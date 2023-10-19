#Ex 1: Pentru reprezentarea unei instante vom folosi un array unidimensional in care fiecare element reprezinta
#        o celula a matricii."
#        state = [1,2,3,4,5,6,7,8,0] -> fiecare element  reprezinta o celula a matricii, 0 fiind celula goala
#        Ordinea elementelor in array reprezinta si ordinea elementelor in matrice. Este mult mai usor sa prelucra,
#        datele problemei astfel pentru scrierea si rezolvarea algoritmului.

#Ex 2: Starea initiala este reprezentata de o asezare random a celulelor cu o celula goala. Pentru a obtine starea initiala,
#        trebuie sa punem intr-un mod aleatoriu numerele de la 1 la 8 intr o matrice, o celula fiind populata de 0, reprezentand
#        celula goala.
#       Starea finala este reprezentata de aranjamentul celulelor in ordine crescatoare, ignorand celula goala, cea populata de 0.

import random
#def initialize_puzzle():

    #initializam lista si adaugam celula goala
 #   numbers = list(range(1, 9))
#    numbers.append(0)

    #amestecam elemente intr o ordine aleatorie pentru a obtine starea initiala a problemei
#    random.shuffle(numbers)

#    return numbers


def is_final_state(state):

    #initializam starea finala
    final_state = list(range(1, 9))
    final_state.append(0)
    #final state ul e de forma [1,2,3,4,5,6,7,8,0]

    if(final_state == state):
        return True
    else:
        return False


#initial_state = initialize_puzzle()

#print("The initial form of the puzzle is: ", initial_state)

#if is_final_state(initial_state):
 #   print("The initial state is  the final state.")
#else:
 #   print("The initial state is not the final state.")


# Ex 3 si 4: Vom defini 4 functii de miscare (move_up, move_down, move_left si move_right) dupa care vom defini o functie de control
#       ce ne va spune daca o miscare intr o anumita directie este valida


def empty_cell_location(state):
    return state.index(0)


#functia de control ce valideaza o miscare
def validation_move(direction, state):

        empty_cell = empty_cell_location(state)

        if direction == "up":
            if empty_cell >= 3: #verificam daca celula goala nu  este in top line
                return True
            else: return False
        elif direction == "down":
            if empty_cell < 6: #Verificam daca celula goala nu este in bottom row
                return True
            else: return  False
        elif direction == "right":
            if empty_cell % 3 != 2: #Verificam daca celula goala nu este in coloana cea mai din dreapta
                return True
            else: return False
        elif direction == "left":
            if empty_cell % 3 != 0: #Verificam daca celula goala nu e in coloana cea mai din stanga
                return True
            else: return False

        else: return False
def move_up(state):
    if not validation_move("up", state):
        return state

    empty_cell = empty_cell_location(state)
    updated_state = state[:] #daca scriam updated_state = state, aveam doua variabile ce pointau spre aceeasi lista in memorie
    updated_state[empty_cell] = state[empty_cell - 3] #schimbam celula goala cu cea de sub ea
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


def move_left(state):
    if not validation_move("left", state):
        return state

    empty_cell = empty_cell_location(state)
    updated_state = state[:]
    updated_state[empty_cell] = state[empty_cell - 1]
    updated_state[empty_cell - 1] = 0

    return updated_state


def move_right(state):
    if not validation_move("right", state):
        return state

    empty_cell = empty_cell_location(state)
    updated_state = state[:]
    updated_state[empty_cell] = state[empty_cell + 1]
    updated_state[empty_cell + 1] = 0
    return updated_state

def iddfs(initial_state):
    max_depth = 1

    while True:
        result = depth_limit_search(initial_state, max_depth)
        if result is not None:
            return result
        max_depth = max_depth + 1

def depth_limit_search(state, depth_limit):
    return depth_limit_search_rec(state, depth_limit, 0, [])

def depth_limit_search_rec(state, depth_limit, depth, path):
        if depth == depth_limit:
            return None

        if is_final_state(state):
            return path

        for direction in ["up", "down", "left", "right"]:
            if direction == "up":
                new_state = move_up(state)
            elif direction == "down":
                new_state = move_down(state)
            elif direction == "left":
                new_state = move_left(state)
            elif direction == "right":
                new_state = move_right(state)
            if new_state != state:
                print(new_state)
                result = depth_limit_search_rec(new_state, depth_limit, depth + 1, path + [direction])
                if result is not None:
                    return  result

initial_state =  [8, 6, 7, 2, 5, 4, 0, 3, 1]
solution_path = iddfs(initial_state)
print(solution_path)