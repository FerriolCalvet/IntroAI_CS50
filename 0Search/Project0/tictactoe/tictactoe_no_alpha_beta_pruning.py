"""
Tic Tac Toe Player
"""

import math, copy

from collections import Counter

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # returns a dict with the elements as keys and the appearanecs as value
    moves_counter = Counter(x for sublist in board for x in sublist)
    x_moves = moves_counter[X]
    o_moves = moves_counter[O]

    if o_moves < x_moves:
        return O
    return X

# print(player(initial_state()))



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_of_actions = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                set_of_actions.add((row, col))
    return set_of_actions

# print(actions(initial_state()))




def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise NameError("Invalid action")

    new_board = copy.deepcopy(board)
    which_player = player(board)

    new_board[action[0]][action[1]] = which_player

    return new_board

# board1 = initial_state()
# print(actions(board1))
# board1 = result(board1, (1,1))
# print(actions(board1))
# board1 = result(board1, (1,2))
# print(actions(board1))
# board1 = result(board1, (0,1))
# print(board1)



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        row = set(board[i])
        if row == {X}:
            return X
        if row == {O}:
            return O

    for i in range(3):
        column = {board[0][i], board[1][i], board[2][i]}
        if column == {X}:
            return X
        if column == {O}:
            return O

    diag1 = {board[0][0], board[1][1], board[2][2]}
    if diag1 == {X}:
        return X
    if diag1 == {O}:
        return O

    diag2 = {board[2][0], board[1][1], board[0][2]}
    if diag2 == {X}:
        return X
    if diag2 == {O}:
        return O

    return None


# print(winner([[None, X, None], [None, X, O], [None, X, None]]))
# print(winner([[O, X, None], [None, O, O], [X, X, O]]))




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if there are no empty cells in the board
    cell_counter = Counter(x for sublist in board for x in sublist)
    if None not in cell_counter:
        return True
    # if there is a winner
    if winner(board):
        return True

    return False




def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    whos_won = winner(board)
    if whos_won == X:
        return 1
    if whos_won == O:
        return -1

    return 0



def max_value(board):
    """
    Returns maximum possible value
    Choose the action leading to a higher result
    """
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    """
    Returns minimum possible value
    Choose the action leading to a lower result
    """
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    who_plays = player(board)

    playing_board = copy.deepcopy(board)

    if who_plays == X:
        v = -math.inf
        best_action = None
        for action in actions(playing_board):
            action_result = min_value(result(playing_board, action))
            if action_result > v:
                v = action_result
                best_action = action

    else:
        v = math.inf
        best_action = None
        for action in actions(playing_board):
            action_result = max_value(result(playing_board, action))
            if action_result < v:
                v = action_result
                best_action = action


    # print(best_action)

    # if best_action != None:
    #     board = result(board, best_action)


    # return minimax(board)
    return best_action

# print(minimax([['O', 'X', None], ['X', None, None], [X, None, 'O']]))
