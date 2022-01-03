import sys
import os
sys.path.insert(1,'../')

import uuid

# PyWebIO imports
import pywebio
from pywebio.input import input, FLOAT, actions
from pywebio.output import put_text, put_buttons, put_markdown, put_link, put_html, put_table
from pywebio.output import use_scope, clear

from pywebio.session import run_js, hold, info

# Database imports
import psycopg2
import psycopg2.extras
from src.utils.sql.connections import connect_to_db

# Game imports
import numpy as np
from src.utils.game import rules

# App imports
from src.utils.app.rps_bot import RPSBot 
from src.utils.app.statschecker import StatsChecker

FORMATTED_OUTCOME = {"W": "User Wins!",
                     "T": "Tied Game",
                     "L": "Bot Wins!"}

FORMATTED_MOVE = {"R": "Rock",
                  "P": "Paper",
                  "S": "Scissors"}

OUTCOME_PALLETE = {"W": "green",
                   "T": "blue",
                   "L": "red"}

MAX_HIST_LEN = 4


def dict_to_str(dict, sep=" | "):
    return sep.join(f"{k}: {v}" for k,v in dict.items())

def rps():

    ## Initial values
    user_action = None
    user_hist = ["R"]*MAX_HIST_LEN
    
    
    count = {"User": 0,
             "Bot": 0,
             "Tie": 0}
    
    depth = np.random.randint(MAX_HIST_LEN, size=1)[0]+1

    rps_bot = RPSBot(cursor,
                     past_weight=0.67,
                     depth=depth)

    game_id = uuid.uuid4()

    while True:
        
        bot_action = rps_bot.make_choice(user_hist[-depth:])
        user_action = actions('Move', [('Rock', 'R'),
                                       ('Paper', 'P'),
                                       ('Scissors', 'S')])
        
        with use_scope('activity', clear=True):

            outcome = rules.RULES[(user_action, bot_action)]
            
            if outcome=="W":
                count["User"] = count["User"] + 1
            elif outcome=="L":
                count["Bot"] = count["Bot"] + 1
            elif outcome=="T":
                count["Tie"] = count["Tie"] + 1
            
            round_moves = f'You => {FORMATTED_MOVE[user_action]} | {FORMATTED_MOVE[bot_action]} <= Bot'
            scoreboard = " | ".join(f"{k}: {v}" for k,v in count.items())
            color = OUTCOME_PALLETE[outcome]

            
            put_markdown(f'<p align="center"><font size="5">{round_moves}</font></p>')
            put_markdown(f'<p align="center"><font size="4"; color="{color}">{FORMATTED_OUTCOME[outcome]}</font></p>')
            put_markdown(f'<p align="center"><font size="6">Scoreboard: [{scoreboard}]</font></p>')

            
        for d in range(1,min(MAX_HIST_LEN,len(user_hist))):
            
            #Update database with the last d moves
            rps_bot.update_database(user_hist[-d:], user_action)
            
        rps_bot.update_recent_matrix(user_hist[-depth:], user_action)
        rps_bot.update_statistics(depth, outcome)
        rps_bot.save_round(game_id=game_id, 
                            user_move=user_action,
                            bot_move=bot_action,
                            outcome=outcome,
                            depth=depth,
                            platform= "Mobile" if info.user_agent.is_touch_capable else "Desktop")

        user_hist.append(user_action)

def stats():

    statschecker = StatsChecker(cursor)

    put_markdown("**Bot & User statistics**")
    put_html(statschecker.report_plots(mobile=info.user_agent.is_touch_capable))
    put_markdown("**Metrics about the algorithm**")
    put_markdown("Depth represents how many steps back does the bot look at (length of the user move history/sequence considered)")
    put_html(statschecker.stats_matrix_plot())

def about():
    with open('src/app/assets/about.md', 'r') as file:
        about_str = file.read()
    put_markdown(about_str)

def index():

    put_markdown("- **Go play against the bot**... *if you dare*")
    put_link(name="Rock Paper Scissors bot \n",app="rps")
    put_markdown("&nbsp;&nbsp;")
    put_markdown(" - **Check some statistics about the game**. *Are we really random?*")
    put_link(name="Usage statistics ",app="stats")
    put_markdown("&nbsp;&nbsp;")
    put_markdown(" - **How was it developed?** *From the Tech Stack to the algorithm behind*")
    put_link(name="Learn about ",app="about")
        


if __name__ == '__main__':

    connection = connect_to_db()
    cursor = connection.cursor()

    port = os.environ['PORT']

    pywebio.start_server([index, rps, stats, about], port=port) 