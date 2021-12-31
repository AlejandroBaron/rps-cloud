import sys
sys.path.insert(1,'../')

import numpy as np

from src.utils.game import rules


class RPSBot:


    def __init__(self, cursor):
        
        self.cursor = cursor

    def make_choice(self, user_hist):

        self.cursor.execute(f"SELECT R,P,S FROM transitionmatrix{len(user_hist)} WHERE Hist='{''.join(user_hist)}'")
        
        past_outcomes = self.cursor.fetchall()[0]
        sum_outcomes = sum(past_outcomes)
        
        next_move_probabilities = [po/sum_outcomes for po in past_outcomes]

        player_prediction = np.random.choice(rules.MOVES, 1,  p=next_move_probabilities)[0]

        return rules.WINNING_MOVE[player_prediction]

    def update_database(self, user_hist, user_move):
        
        query = f"""UPDATE transitionmatrix{len(user_hist)}
                    SET {user_move} = {user_move} + 1
                    WHERE Hist='{''.join(user_hist)}' """
        
        self.cursor.execute(query)

    def update_statistics(self, depth, outcome):
        
        query = f"""UPDATE statistics
                    SET {outcome} = {outcome} + 1
                    WHERE Depth={depth} """

        
        self.cursor.execute(query)