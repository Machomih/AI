import itertools


class NumberScrabbleImproved:
    def __init__(self):
        self.board = [0] * 9
        self.player_a_moves = []
        self.player_b_moves = []

    def is_game_over(self):
        return self.check_win('A') or self.check_win('B') or all(num != 0 for num in self.board)

    def check_win(self, player):
        moves = self.player_a_moves if player == 'A' else self.player_b_moves
        if len(moves) < 3:
            return False

        for combo in itertools.combinations(moves, 3):
            if sum(combo) == 15:
                return True

        return False

    def is_valid_move(self, number):
        return 1 <= number <= 9 and self.board[number - 1] == 0

    def make_move(self, player, number):
        if not self.is_valid_move(number):
            return False

        self.board[number - 1] = number
        if player == 'A':
            self.player_a_moves.append(number)
        else:
            self.player_b_moves.append(number)
        return True

    def undo_move(self, player, number):
        self.board[number - 1] = 0
        if player == 'A':
            self.player_a_moves.remove(number)
        else:
            self.player_b_moves.remove(number)

    def min_max(self, depth, player, alpha=float('-inf'), beta=float('inf')):
        if player == 'B':
            best_value = float('-inf')
            best_move = None
        else:
            best_value = float('inf')
            best_move = None

        if depth == 0 or self.is_game_over():
            return self.calculate_heuristic(), None

        for number in range(1, 10):
            if self.is_valid_move(number):
                self.make_move(player, number)
                heuristic_value, _ = self.min_max(depth - 1, 'A' if player == 'B' else 'B', alpha, beta)
                self.undo_move(player, number)

                if player == 'B':
                    if heuristic_value > best_value:
                        best_value = heuristic_value
                        best_move = number
                    alpha = max(alpha, best_value)
                else:
                    if heuristic_value < best_value:
                        best_value = heuristic_value
                        best_move = number
                    beta = min(beta, best_value)

                # Alpha-Beta Pruning
                if beta <= alpha:
                    break

        return best_value, best_move

    def calculate_heuristic(self):
        # Check for immediate win
        if self.check_win('B'):
            return 100
        elif self.check_win('A'):
            return -100

        # Check for potential wins
        score = 0
        for combo in itertools.combinations(range(1, 10), 3):
            if sum(combo) == 15:
                b_count = sum(1 for num in combo if num in self.player_b_moves)
                a_count = sum(1 for num in combo if num in self.player_a_moves)
                if b_count == 2 and a_count == 0:
                    score += 10  # B is one move away from winning
                elif a_count == 2 and b_count == 0:
                    score -= 10  # A is one move away from winning
        return score

    def play_game(self):
        current_player = 'A'

        while not self.is_game_over():
            print(f"Current Board: {self.board}")
            if current_player == 'A':
                move = int(input(f"{current_player}, enter your move (1-9): "))
                if self.is_valid_move(move):
                    self.make_move(current_player, move)
                else:
                    print("Invalid move. Try again.")
            else:
                _, move = self.min_max(2, current_player)
                self.make_move(current_player, move)
                print(f"{current_player} chooses {move}")

            if self.check_win('A'):
                print("Player A wins!")
                break
            elif self.check_win('B'):
                print("Player B wins!")
                break
            current_player = 'B' if current_player == 'A' else 'A'

        if not self.check_win('A') and not self.check_win('B'):
            print("It's a draw.")


if __name__ == '__main__':
    game = NumberScrabbleImproved()
    game.play_game()
