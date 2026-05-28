import math
import random
import copy

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


# MCTS Node
class MCTSNode:

    def __init__(self, game, parent=None, move=None):

        self.game = copy.deepcopy(game)

        self.parent = parent
        self.move = move

        self.children = []

        self.wins = 0
        self.visits = 0

        self.untried_moves = game.available_moves()

    # UCT selection
    def select_child(self):

        return max(
            self.children,
            key=lambda child:
            (
                child.wins / child.visits
                +
                math.sqrt(
                    2 * math.log(self.visits)
                    / child.visits
                )
            )
        )


# Random Simulation
def random_playout(game, current_player):

    while not game.is_terminal():

        move = random.choice(game.available_moves())

        game.make_move(move, current_player)

        current_player = (
            PLAYER_O
            if current_player == PLAYER_X
            else PLAYER_X
        )

    return game.evaluate()


# Monte-Carlo Tree Search
def monte_carlo_tree_search(root_game, iterations=1000):

    root = MCTSNode(root_game)

    for _ in range(iterations):

        node = root

        game = copy.deepcopy(root_game)

        current_player = PLAYER_X

        # Selection
        while (
            node.untried_moves == []
            and node.children != []
        ):

            node = node.select_child()

            game.make_move(node.move, current_player)

            current_player = (
                PLAYER_O
                if current_player == PLAYER_X
                else PLAYER_X
            )

        # Expansion
        if node.untried_moves:

            move = random.choice(node.untried_moves)

            node.untried_moves.remove(move)

            game.make_move(move, current_player)

            child = MCTSNode(game, node, move)

            node.children.append(child)

            node = child

            current_player = (
                PLAYER_O
                if current_player == PLAYER_X
                else PLAYER_X
            )

        # Simulation
        result = random_playout(game, current_player)

        # Backpropagation
        while node is not None:

            node.visits += 1

            if result == 1:
                node.wins += 1

            node = node.parent

    best_child = max(
        root.children,
        key=lambda child: child.visits
    )

    return best_child.move


# Test Case
game = TicTacToe()

game.board = [
    ['X', '.', '.'],
    ['.', 'O', '.'],
    ['.', '.', '.']
]

print("Current Board:")
game.display()

best = monte_carlo_tree_search(
    game,
    iterations=2000
)

print("Best Move:", best)
