import itertools


class NumberScrabble:
    def __init__(self):
        self.board = [0] * 9  # Represent the available numbers (1-9)
        self.player_a_moves = []
        self.player_b_moves = []

    def is_game_over(self):
        return self.check_win('A') or self.check_win('B') or len(self.player_a_moves) + len(self.player_b_moves) == 9

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
            self.player_a_moves.pop()
        else:
            self.player_b_moves.pop()

    def min_max(self, depth, player):
        if player == 'B':
            best_value = float('-inf')
            best_move = None
        else:
            best_value = float('inf')
            best_move = None

        if depth == 0 or self.is_game_over():
            return self.calculate_heuristic('B')

        for number in range(1, 10):
            if self.is_valid_move(number):
                self.make_move(player, number)
                current_value = self.min_max(depth - 1, 'A' if player == 'B' else 'B')
                self.undo_move(player, number)

                if player == 'B':
                    if current_value > best_value:
                        best_value = current_value
                        best_move = number
                else:
                    if current_value < best_value:
                        best_value = current_value
                        best_move = number

        if depth == 2:
            return best_move
        return best_value

    def calculate_heuristic(self, player):
        if player == 'A':
            player_moves = self.player_a_moves
        else:
            player_moves = self.player_b_moves

        if len(player_moves) < 3:
            return 0

        for combo in itertools.combinations(player_moves, 3):
            if sum(combo) == 15:
                return 1

        return 0

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
                move = self.min_max(2, current_player)
                self.make_move(current_player, move)
                print(f"{current_player} chooses {move}")

            current_player = 'B' if current_player == 'A' else 'A'

        if self.check_win('A'):
            print("Player A wins!")
        elif self.check_win('B'):
            print("Player B wins!")
        else:
            print("It's a draw.")


if __name__ == '__main__':
    game = NumberScrabble()
    game.play_game()

