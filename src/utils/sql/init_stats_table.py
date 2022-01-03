import sys 
sys.path.insert(1,'../')

import psycopg2
import itertools
import numpy as np 
import argparse
import yaml

from src.utils.game import rules
from src.utils.sql.connections import connect_to_db
from src.utils.sql.queries import init_stats_table, check_for_table


def get_initial_records() -> list[dict]:
    """Get transition matrix initial values for a given depth (equal probability for all transition states)

    Returns:
        list[dict]: list containing the records as dictionaries
    """
    
    initial_counts = {m:0 for m in rules.OUTCOMES}
    
    transition_matrix_records = [{**{"Depth":d}, **initial_counts} for d in range(1,5)]

    return transition_matrix_records




if __name__=="__main__":

    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    
    try:
        
        connection = connect_to_db()
        cursor = connection.cursor()


        if check_for_table(cursor, "statistics"):
            raise ValueError("Table already exists")

        init_stats_table(cursor, get_initial_records())
        print("Success!")

    except (Exception, psycopg2.Error) as error:
        print("Error while initializing table: ", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")