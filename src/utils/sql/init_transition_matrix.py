import sys 
sys.path.insert(1,'../')

import psycopg2
import itertools
import numpy as np 
import argparse
import yaml

from src.utils.game import rules
from src.utils.sql.connections import connect_to_db
from src.utils.sql.queries import init_transition_table, check_for_table


def get_initial_records(depth: int) -> list[dict]:
    """Get transition matrix initial values for a given depth (equal probability for all transition states)

    Args:
        depth (int): pattern history depth

    Returns:
        list[dict]: list containing the records as dictionaries
    """
    
    initial_counts = {m:1 for m in rules.MOVES}
    
    if depth>1:
        possible_past_combinations = ["".join(combination) for combination in itertools.product(rules.MOVES,repeat=depth)]
    else:
        possible_past_combinations = rules.MOVES

    transition_matrix_records = [{**{"Hist":past_sequence}, **initial_counts} for past_sequence in possible_past_combinations]

    return transition_matrix_records




if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--depth',
                        type=int,
                        required=False,
                        help='Depth of history in transition matrix')

    args = parser.parse_args()

    if args.depth is None:
        args.depth = 2
    
    try:
        
        connection = connect_to_db()
        cursor = connection.cursor()


        if check_for_table(cursor, f"transitionmatrix{args.depth}"):
            raise ValueError("Table already exists")

        init_transition_table(cursor, args.depth, get_initial_records(args.depth))
        print("Success!")

    except (Exception, psycopg2.Error) as error:
        print("Error while initializing table: ", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")