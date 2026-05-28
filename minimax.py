import math

PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = '.'


class TicTacToe:

    def __init__(self):
        self.board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]

    def display(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def available_moves(self):
        moves = []

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    moves.append((i, j))

        return moves

    def make_move(self, move, player):
        i, j = move
        self.board[i][j] = player

    def undo_move(self, move):
        i, j = move
        self.board[i][j] = EMPTY

    def check_winner(self):

        # Rows
        for row in self.board:
            if row.count(PLAYER_X) == 3:
                return PLAYER_X
            if row.count(PLAYER_O) == 3:
                return PLAYER_O

        # Columns
        for col in range(3):

            column = []

            for row in range(3):
                column.append(self.board[row][col])

            if column.count(PLAYER_X) == 3:
                return PLAYER_X

            if column.count(PLAYER_O) == 3:
                return PLAYER_O

        # Diagonals
        diagonal1 = [self.board[i][i] for i in range(3)]
        diagonal2 = [self.board[i][2 - i] for i in range(3)]

        if diagonal1.count(PLAYER_X) == 3:
            return PLAYER_X

        if diagonal1.count(PLAYER_O) == 3:
            return PLAYER_O

        if diagonal2.count(PLAYER_X) == 3:
            return PLAYER_X

        if diagonal2.count(PLAYER_O) == 3:
            return PLAYER_O

        return None

    def is_terminal(self):
        return (
            self.check_winner() is not None or
            len(self.available_moves()) == 0
        )

    def evaluate(self):

        winner = self.check_winner()

        if winner == PLAYER_X:
            return 1

        elif winner == PLAYER_O:
            return -1

        else:
            return 0


# Minimax Algorithm
def minimax(game, maximizing_player):

    if game.is_terminal():
        return game.evaluate()

    # MAX player
    if maximizing_player:

        best_score = -math.inf

        for move in game.available_moves():

            game.make_move(move, PLAYER_X)

            score = minimax(game, False)

            game.undo_move(move)

            best_score = max(best_score, score)

        return best_score

    # MIN player
    else:

        best_score = math.inf

        for move in game.available_moves():

            game.make_move(move, PLAYER_O)

            score = minimax(game, True)

            game.undo_move(move)

            best_score = min(best_score, score)

        return best_score


# Find Best Move
def best_move(game):

    best_score = -math.inf
    move_selected = None

    for move in game.available_moves():

        game.make_move(move, PLAYER_X)

        score = minimax(game, False)

        game.undo_move(move)

        if score > best_score:
            best_score = score
            move_selected = move

    return move_selected


# Test Case
game = TicTacToe()

game.board = [
    ['X', 'X', '.'],
    ['O', 'O', '.'],
    ['.', '.', '.']
]

print("Current Board:")
game.display()

move = best_move(game)

print("Best Move:", move)
