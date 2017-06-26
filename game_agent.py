"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
#import logging
#logging.basicConfig(level=logging.DEBUG,filename="my_log.log")

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    #if the player's legal moves remaining is greater than opponents move use this
    #heuristic to chase after the opponent..
    num_my_moves = len(game.get_legal_moves(player))
    num_opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    if(num_my_moves > num_opp_moves):
        return float(num_my_moves - (2 * num_opp_moves))
    else:
        return float(num_my_moves)



def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    #raise NotImplementedError
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    num_my_moves = len(game.get_legal_moves(player))
    num_opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(num_my_moves - (2 * num_opp_moves))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=50.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            # logging.debug("search depth is: "+str(self.search_depth))
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
             pass  #Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def max_val(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if(depth == 0):
            return self.score(game, self)
        node_value = float("-inf")
        for a in game.get_legal_moves():
            node_value = max(node_value, self.min_val(game.forecast_move(a), depth - 1))
        return node_value

    def min_val(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if(depth == 0):
            return self.score(game, self)
        node_value = float("+inf")
        for a in game.get_legal_moves():
            node_value = min(node_value, self.max_val(game.forecast_move(a), depth - 1))
        return node_value

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        best_possible_move = (-1, -1)
        maximum = float("-inf")
        for a in game.get_legal_moves():
            current_val = self.min_val(game.forecast_move(a), depth - 1)
            if current_val >= maximum:
                maximum = current_val
                best_possible_move = a
        return best_possible_move
        # # TODO: finish this function!
        # possible_actions = {}
        # for a in game.get_legal_moves(self):
        #     possible_actions[a] = self.min_value(game.forecast_move(a), depth - 1)
        # maximum = float("-inf")
        # best_possible_move = ()
        # for key, value in possible_actions.items():
        #     if(value >= maximum):
        #         maximum = value
        #         best_possible_move = key
        # return best_possible_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        best_move = (-1, -1)
        recent_best = best_move
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            s_depth = 1

            while True:
                #logging.debug("The value of depth is: {}".format(s_depth))
                curr_move = self.alphabeta(game, s_depth)
                if curr_move != (-1, -1):
                    best_move = curr_move
                    recent_best = curr_move
                else:
                    best_move = recent_best
                    break
                s_depth += 1

        except SearchTimeout:
             return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def max_val(self, game, depth , alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if(depth == 0):
            return self.score(game, self)
        node_value = float("-inf")
        for a in game.get_legal_moves():
            node_value = max(node_value, self.min_val(game.forecast_move(a), depth - 1, alpha, beta))
            if(node_value >= beta):
                return node_value
            alpha = max(alpha, node_value)
        return node_value

    def min_val(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if(depth == 0):
            return self.score(game, self)
        node_value = float("inf")
        for a in game.get_legal_moves():
            node_value = min(node_value, self.max_val(game.forecast_move(a), depth - 1, alpha, beta))
            if(node_value <= alpha):
                return node_value
            beta = min(beta, node_value)
        return node_value

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        best_possible_move = (-1, -1)
        maximum = float("-inf")
        for a in game.get_legal_moves():
            current_val = self.min_val(game.forecast_move(a), depth - 1, alpha, beta)
            alpha = max(alpha, current_val)
            if current_val >= maximum:
                maximum = current_val
                best_possible_move = a
                #alpha = maximum
        return best_possible_move