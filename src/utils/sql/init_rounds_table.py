import sys 
sys.path.insert(1,'../')

import psycopg2
import itertools
import numpy as np 
import argparse
import yaml

from src.utils.game import rules
from src.utils.sql.connections import connect_to_db
from src.utils.sql.queries import init_rounds_table, check_for_table



if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file',
                        type=str,
                        default='config_files/config.yml', required=False,
                        help='Path to configuration file')
    parser.add_argument('-d', '--depth',
                        type=int,
                        required=False,
                        help='Depth of history in transition matrix')

    args = parser.parse_args()

    if args.depth is None:
        with open(args.config_file) as file:
            args.depth = yaml.full_load(file)["bot"]["depth"]
    
    try:
        
        connection = connect_to_db(args.config_file)
        cursor = connection.cursor()


        if check_for_table(cursor, f"rounds"):
            raise ValueError("Table already exists")

        init_rounds_table(cursor)
        print("Success!")

    except (Exception, psycopg2.Error) as error:
        print("Error while initializing table: ", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")