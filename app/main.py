import sys
import argparse
import yaml
sys.path.insert(1,'../')


# PyWebIO imports
import pywebio
from pywebio.input import input, FLOAT, actions
from pywebio.output import put_text, put_buttons, put_markdown, put_link, put_html, put_table
from pywebio.output import use_scope, clear

from pywebio.session import run_js, hold

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

MAX_HIST_LEN = 5


def dict_to_str(dict, sep=" | "):
    return sep.join(f"{k}: {v}" for k,v in dict.items())

def rps():

    ## Initial values
    user_action = None
    user_hist = ["R"]*MAX_HIST_LEN
    
    
    count = {"User": 0,
             "Bot": 0,
             "Tie": 0}
    
    rps_bot = RPSBot(cursor)

    while True:

        depth = np.random.randint(5, size=1)[0]+1
        
        bot_action = rps_bot.make_choice(user_hist[-depth:])
        user_action = actions('Move', [('Rock', 'R'),
                                       ('Paper', 'P'),
                                       ('Scissors', 'S')])
        
        with use_scope('activity', clear=True):

            outcome = rules.RULES[(user_action, bot_action)]
            
            put_text(f'User: {user_action}')
            put_text(f'Bot: {bot_action}')
            put_text(f'{FORMATTED_OUTCOME[outcome]}')
            
            if outcome=="W":
                count["User"] = count["User"] + 1
            elif outcome=="L":
                count["Bot"] = count["Bot"] + 1
            elif outcome=="T":
                count["Tie"] = count["Tie"] + 1
            
            scoreboard = " | ".join(f"{k}: {v}" for k,v in count.items())
            put_text(f'Scoreboard: [{scoreboard}]')

            
        for d in range(1,min(MAX_HIST_LEN,len(user_hist))):
            
            #Update database with the last d moves
            rps_bot.update_database(user_hist[-d:], user_action)
            user_hist.append(user_action)
        
        rps_bot.update_statistics(depth, outcome)

def stats():

    statschecker = StatsChecker(cursor)

    put_markdown("**Bot & User statistics**")
    put_html(statschecker.report_plots())
    put_markdown("**Metrics about the algorithm**")
    put_markdown("Depth represents how many steps back does the bot look at (length of the user move history/sequence considered)")
    put_html(statschecker.stats_matrix_plot())

def about():
    with open('app/assets/about.md', 'r') as file:
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

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file',
                        type=str,
                        default='config_files/config.yml', required=False,
                        help='Path to configuration file')

    args = parser.parse_args()

    connection = connect_to_db(args.config_file)
    cursor = connection.cursor()


    pywebio.start_server([index, rps, stats, about], port=80, debug=True) 