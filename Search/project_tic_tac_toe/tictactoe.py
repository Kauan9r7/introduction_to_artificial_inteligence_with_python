"""
Tic Tac Toe Player
"""
import copy

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
    X_count = sum(row.count("X") for row in board)
    O_count = sum(row.count("O") for row in board)
    if X_count > O_count:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    board_size = len(board)
    possible_actions = set()
    for row in range(board_size ):
        for collum in range(board_size):
            if board[row][collum] == EMPTY:
                possible_actions.add((row,collum))
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row = action[0]
    collum = action[1]
    new_board = copy.deepcopy(board)
    new_board[row][collum] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Verifica se há ganhador na horizontal
    for row in board:
        if len(set(row)) == 1 and row[0] != EMPTY:
            return row[0]

    #Vertical
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col]

    #Diagonal
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    points = winner(board)
    if points == X:
        return 1
    elif points == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    print(f"\n--- IA ({current_player}) calculando jogada ---")

    if current_player == X:
        best_val = -float("inf")
        best_action = None
        alpha = -float("inf")
        beta = float("inf")

        for action in actions(board):
            val = min_value(result(board, action), alpha, beta)
            print(f"Ação {action} -> Pontuação avaliada: {val}") # Imprime cada opção testada
            if val > best_val:
                best_val = val
                best_action = action
            alpha = max(alpha, best_val)
            
        print(f"👉 IA escolheu a ação {best_action} com valor {best_val}\n")
        return best_action

    else:
        best_val = float("inf")
        best_action = None
        alpha = -float("inf")
        beta = float("inf")

        for action in actions(board):
            val = max_value(result(board, action), alpha, beta)
            print(f"Ação {action} -> Pontuação avaliada: {val}") # Imprime cada opção testada
            if val < best_val:
                best_val = val
                best_action = action
            beta = min(beta, best_val)
            
        print(f"👉 IA escolheu a ação {best_action} com valor {best_val}\n")
        return best_action

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = -float("inf")
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v