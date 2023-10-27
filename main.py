import math
import time


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


def empty_cell_location(state):
    return state.index(0)


def validation_move(direction, state):
    empty_cell = empty_cell_location(state)

    if direction == "up":
        if empty_cell >= 3:
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
            result = depth_limit_search_rec(new_state, depth_limit, depth + 1, path + [direction], visited_states)
            if result is not None:
                return result

    visited_states.remove(tuple(state))


# EX:5 Inceput
def manhattan_distance(state):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            correct_row = (state[i] - 1) // 3
            correct_col = (state[i] - 1) % 3

            current_row = i // 3
            current_col = i % 3

            distance += abs(correct_row - current_row) + abs(correct_col - current_col)
    return distance


def hamming_distance(state):
    distance = 0
    for i in range(9):
        if state[i] != 0 and state[i] != i + 1:  # Verifică dacă fiecare piesă este la locul corect.
            distance += 1
    return distance


def euclidean_distance(state):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            correct_row = (state[i] - 1) // 3
            correct_col = (state[i] - 1) % 3

            current_row = i // 3
            current_col = i % 3

            distance += ((correct_row - current_row) ** 2 + (correct_col - current_col) ** 2) ** 0.5
    return distance


def greedy_search(state, heuristic):
    visited = set()
    queue = [(state, 0)]
    while queue:
        current_state, moves = queue.pop(0)
        if tuple(current_state) in visited:
            continue
        visited.add(tuple(current_state))
        if is_final_state(current_state):
            return moves
        neighbors = [move_up(current_state), move_down(current_state), move_left(current_state),
                     move_right(current_state)]
        neighbors = [n for n in neighbors if n != current_state]  # elimină stările care nu s-au schimbat
        neighbors.sort(key=lambda x: heuristic(x))
        for neighbor in neighbors:
            queue.append((neighbor, moves + 1))
    return -1


def main():
    instances = [
        [8, 6, 7, 2, 5, 4, 3, 0, 1],
        [2, 5, 3, 1, 0, 6, 4, 7, 8],
        [2, 7, 5, 0, 8, 4, 3, 1, 6]]

    for idx, instance in enumerate(instances):
        print(f"----- Instanța {idx + 1} -----")
        print("Stare inițială:", instance)

        # IDDFS
        print("\nStrategia IDDFS:")
        start_time = time.time()
        moves = iddfs(instance)
        end_time = time.time()
        if moves is not None:
            print(f"Soluția a fost găsită in {len(moves)} mutări.")
            print("Mutările:", moves)
        else:
            print("Nu s-a găsit soluție.")
        print(f"Durata execuției: {end_time - start_time:.4f} secunde.")

        # Greedy cu distanta Manhattan
        print("\nStrategia Greedy (Manhattan):")
        start_time = time.time()
        moves = greedy_search(instance, manhattan_distance)
        end_time = time.time()
        if moves != -1:
            print("Soluția a fost găsită in", {moves}, "mutări.")
        else:
            print("Nu s-a găsit soluție.")
        print(f"Durata execuției: {end_time - start_time:.4f} secunde.")

        # Greedy cu distanta Hamming
        print("\nStrategia Greedy (Hamming):")
        start_time = time.time()
        moves = greedy_search(instance, hamming_distance)
        end_time = time.time()
        if moves != -1:
            print("Soluția a fost găsită in", {moves}, "mutări.")
        else:
            print("Nu s-a găsit soluție.")
        print(f"Durata execuției: {end_time - start_time:.4f} secunde.")

        print("\nStrategia Greedy (Euclidiana):")
        start_time = time.time()
        moves = greedy_search(instance, euclidean_distance)
        end_time = time.time()
        if moves != -1:
            print("Soluția a fost găsită in", moves, "mutări.")
        else:
            print("Nu s-a găsit soluție.")
        print(f"Durata execuției: {end_time - start_time:.4f} secunde.")

        print("\n")


if __name__ == "__main__":
    main()
