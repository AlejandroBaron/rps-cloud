import sys 
import argparse
sys.path.insert(1,'../')

import psycopg2
import itertools
import numpy as np 
import argparse
import yaml

from src.utils.game import rules
from src.utils.sql.connections import connect_to_db
from src.utils.sql.queries import drop_table, check_for_table


if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file',
                        type=str,
                        default='config_files/config.yml', required=False,
                        help='Path to configuration file')


    args = parser.parse_args()

    try:
        
        connection = connect_to_db(args.config_file)
        cursor = connection.cursor()

        if not check_for_table(cursor, f"rounds"):
            raise ValueError("Table does not exist")

        drop_table(cursor, f"rounds")
        print("Success!")

    except (Exception, psycopg2.Error) as error:
        print("Error while dropping table: ", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")