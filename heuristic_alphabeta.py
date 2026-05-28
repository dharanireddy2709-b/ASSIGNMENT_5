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


# Heuristic Evaluation Function
def heuristic(game):

    score = 0

    lines = []

    # Rows
    lines.extend(game.board)

    # Columns
    for col in range(3):
        lines.append(
            [game.board[row][col] for row in range(3)]
        )

    # Diagonals
    lines.append([game.board[i][i] for i in range(3)])
    lines.append([game.board[i][2 - i] for i in range(3)])

    for line in lines:

        x_count = line.count(PLAYER_X)
        o_count = line.count(PLAYER_O)

        # Favor X positions
        if x_count > 0 and o_count == 0:
            score += x_count

        # Favor O positions
        elif o_count > 0 and x_count == 0:
            score -= o_count

    return score


# Heuristic Alpha-Beta Algorithm
def heuristic_alpha_beta(
    game,
    depth,
    alpha,
    beta,
    maximizing_player
):

    if game.check_winner() == PLAYER_X:
        return 100

    if game.check_winner() == PLAYER_O:
        return -100

    if len(game.available_moves()) == 0:
        return 0

    # Depth limit reached
    if depth == 0:
        return heuristic(game)

    # MAX player
    if maximizing_player:

        value = -math.inf

        for move in game.available_moves():

            game.make_move(move, PLAYER_X)

            value = max(
                value,
                heuristic_alpha_beta(
                    game,
                    depth - 1,
                    alpha,
                    beta,
                    False
                )
            )

            game.undo_move(move)

            alpha = max(alpha, value)

            # Pruning
            if beta <= alpha:
                break

        return value

    # MIN player
    else:

        value = math.inf

        for move in game.available_moves():

            game.make_move(move, PLAYER_O)

            value = min(
                value,
                heuristic_alpha_beta(
                    game,
                    depth - 1,
                    alpha,
                    beta,
                    True
                )
            )

            game.undo_move(move)

            beta = min(beta, value)

            # Pruning
            if beta <= alpha:
                break

        return value


# Best Move Function
def best_move(game):

    best_score = -math.inf
    selected_move = None

    for move in game.available_moves():

        game.make_move(move, PLAYER_X)

        score = heuristic_alpha_beta(
            game,
            depth=3,
            alpha=-math.inf,
            beta=math.inf,
            maximizing_player=False
        )

        game.undo_move(move)

        if score > best_score:
            best_score = score
            selected_move = move

    return selected_move


# Test Case
game = TicTacToe()

game.board = [
    ['X', '.', '.'],
    ['.', 'O', '.'],
    ['.', '.', '.']
]

print("Current Board:")
game.display()

move = best_move(game)

print("Best Move:", move)
