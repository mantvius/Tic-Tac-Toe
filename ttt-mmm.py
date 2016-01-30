"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
# import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but do not change their names.
NTRIALS = 800        # Number of trials to run
SCORE_CURRENT = 2.0  # Score for squares played by the current player
SCORE_OTHER = 1.0    # Score for squares played by the other player
    

def mc_trial(board, player):
    """
    This function takes a current board and the next player to move.
    The function should play a game starting with the given player by making random moves, alternating between players.
    The function should return when the game is over. The modified board will contain the state of the game,
    so the function does not return anything. In other words, the function should modify the board input.
    """
    while board.check_win() is None:
        square = random.choice(board.get_empty_squares())
        board.move(square[0], square[1], player)
        player = provided.switch_player(player)
    return


def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the same dimensions as the Tic-Tac-Toe board,
    a board from a completed game, and which player the machine player is.
    The function should score the completed board and update the scores grid.
    As the function updates the scores grid directly, it does not return anything,
    """
    if board.check_win() == provided.DRAW:
        return
    elif board.check_win() == player:
        for dummy_row in range(board.get_dim()):
            for dummy_col in range(board.get_dim()):
                if board.square(dummy_row, dummy_col) == player:
                    scores[dummy_row][dummy_col] = SCORE_CURRENT
                elif board.square(dummy_row, dummy_col) == provided.switch_player(player):
                    scores[dummy_row][dummy_col] = -SCORE_OTHER
    elif board.check_win() == provided.switch_player(player):
        for dummy_row in range(board.get_dim()):
            for dummy_col in range(board.get_dim()):
                if board.square(dummy_row, dummy_col) == player:
                    scores[dummy_row][dummy_col] = -SCORE_CURRENT
                elif board.square(dummy_row, dummy_col) == provided.switch_player(player):
                    scores[dummy_row][dummy_col] = SCORE_OTHER


def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. The function should find all of the empty squares
    with the maximum score and randomly return one of them as a (row, column) tuple.
    It is an error to call this function with a board that has no empty squares (there is no possible next move),
    so your function may do whatever it wants in that case. The case where the board is full will not be tested.
    """
    max_score = -float("inf")
    list_empty_squares = board.get_empty_squares()
    list_max_scores = []
    for empty_square in list_empty_squares:
        if scores[empty_square[0]][empty_square[1]] > max_score:
            list_max_scores = [empty_square]
            max_score = scores[empty_square[0]][empty_square[1]]
        elif scores[empty_square[0]][empty_square[1]] == max_score:
            list_max_scores.append(empty_square)
    return random.choice(list_max_scores)


def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is, and the number of trials to run.
    The function should use the Monte Carlo simulation described above to return a move for the machine player
    in the form of a (row, column) tuple. Be sure to use the other functions you have written!
    """

    sum_scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    cur_board = board.clone()
    for dummy in range(trials):
        board = cur_board.clone()
        mc_trial(board, provided.PLAYERX)
        grid_scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
        mc_update_scores(grid_scores, board, player)

        for dummy_row in range(board.get_dim()):
            for dummy_col in range(board.get_dim()):
                sum_scores[dummy_row][dummy_col] += grid_scores[dummy_row][dummy_col]

    board = cur_board.clone()

    best_move = get_best_move(board,sum_scores)
    print "best move", best_move
    return best_move



# board = provided.TTTBoard(3, False)
# mc_move(board, provided.PLAYERX, NTRIALS)

provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)


# Test game with the console or the GUI. Uncomment whichever you prefer.
# Both should be commented out when you submit for testing to save time.


# The TTTBoard class uses four important constants from the provided code that you will use in your code.
# These constants are EMPTY, PLAYERX, PLAYERO, and DRAW.
# Included with the definition of these constants is a helper function switch_player(player)
# that returns PLAYERO on input PLAYERX and PLAYERX on input PLAYERO.

# Remember that you will need to add the module name as a prefix when accessing these constants.
# As the module is imported with the name provided, these constants can be referenced as
# provided.EMPTY, provided.PLAYERX, provided.PLAYERO, provided.DRAW.
# The function switch_player can be called as provided.switch_player(player).

# play_game(mc_move_function, ntrials, reverse) function
# that uses the mc_move_function you provide to play a game with two machine players on a 3 x 3 board.
# The play_game function will print the moves in the game to the console.
