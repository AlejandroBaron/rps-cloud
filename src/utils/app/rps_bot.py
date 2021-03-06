import sys
sys.path.insert(1,'../')

import numpy as np
import itertools

from src.utils.game import rules


def initial_records(depth: int) -> dict:
    """Get transition matrix initial values for a given depth (equal probability for all transition states)

    Args:
        depth (int): pattern history depth

    Returns:
        list[dict]: list containing the records as dictionaries
    """
    
    initial_counts = np.array([1 for _ in rules.MOVES])
    
    if depth>1:
        possible_combinations = ["".join(combination) for combination in itertools.product(rules.MOVES,repeat=depth)]
    else:
        possible_combinations = rules.MOVES

    transition_matrix_records = {tuple(sequence):initial_counts for sequence in possible_combinations}

    return transition_matrix_records


class RPSBot:


    def __init__(self, cursor, past_weight=0.5, depth=2):
        
        self.cursor = cursor
        self.past_weight = past_weight
        self.depth = depth
        self.recent_matrix = initial_records(depth)

    def make_choice(self, user_hist: list) -> str:
        """Decides what move to make based on user history

        Args:
            user_hist (list): user past history

        Returns:
            str: next move to make
        """

        self.cursor.execute(f"SELECT R,P,S FROM transitionmatrix{len(user_hist)} WHERE Hist='{''.join(user_hist)}'")
        
        try:
            stored_outcomes = self.cursor.fetchall()[0]
        
            recent_outcomes = self.recent_matrix[tuple(user_hist)]
            
            n_stored_outcomes = sum(stored_outcomes)
            n_recent_outcomes = sum(recent_outcomes)

            next_move_stored_probs = np.array([po/n_stored_outcomes for po in stored_outcomes])
            next_move_recent_probs = np.array([po/n_recent_outcomes for po in recent_outcomes])

            next_move_probabilities = self.past_weight * next_move_stored_probs + (1-self.past_weight) * next_move_recent_probs
            player_prediction = np.random.choice(rules.MOVES, 1,  p=next_move_probabilities)[0]

        except:
            
            recent_outcomes = self.recent_matrix[tuple(user_hist)]
            n_recent_outcomes = sum(recent_outcomes)
            next_move_probabilities = np.array([po/n_recent_outcomes for po in recent_outcomes])
            player_prediction = np.random.choice(rules.MOVES, 1,  p=next_move_probabilities)[0]



        self.past_weight = min(self.past_weight*0.99,0.25)
        

        return rules.WINNING_MOVE[player_prediction]

    def update_database(self, user_hist: list, user_move: str):
        """
        Increments the database count for the pair (user_hist, user_move)
        """

        query = f"""UPDATE transitionmatrix{len(user_hist)}
                    SET {user_move} = {user_move} + 1
                    WHERE Hist='{''.join(user_hist)}' """
        
        self.cursor.execute(query)

    def update_recent_matrix(self, user_hist: list, user_move: str):
        """Updates the recent matrix database

        Args:
            user_hist (list): list containing user history
            user_move (str): next user_move
        """

        increase = {"R": np.array([1,0,0]),
                    "P": np.array([0,1,0]),
                    "S": np.array([0,0,1])}
        
        self.recent_matrix[tuple(user_hist)] =  self.recent_matrix[tuple(user_hist)] + increase[user_move]


    def update_statistics(self, depth, outcome):
        """
        Updates the statistic table
        """
        
        query = f"""UPDATE statistics
                    SET {outcome} = {outcome} + 1
                    WHERE Depth={depth} """

        
        self.cursor.execute(query)

    def save_round(self, game_id:str, user_move: list, bot_move: str, outcome: str, depth: int, platform: str):
        """Stores the following info about each round

        Args:
            game_id (str): unique id representing this round
            user_move (list): move selected by the user
            bot_move (str): move performed by the bot
            outcome (str): outcome of the round
            depth (int): history depth used by the bot
            platform (str): mobile or desktop
        """
        
        query = f"INSERT INTO rounds VALUES ('{game_id}','{user_move}','{bot_move}','{outcome}',{depth}, '{platform}')"
        
        self.cursor.execute(query)

