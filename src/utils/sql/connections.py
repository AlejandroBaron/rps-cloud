import psycopg2
import yaml

def connect_to_db(config_file: str) -> psycopg2.extensions.connection:
    """Returns a psycopg2 connection object to a POSTGRESQL database

    Args:
        config_file (str): path to the config.yml file containing the necessary credentials and routes

    Returns:
        psycopg2.Connection: connection to the database
    """



    with open(config_file) as file:
        configuration = yaml.full_load(file)

    user = configuration["credentials"]["user"]
    password = configuration["credentials"]["password"]

    database = configuration["connection"]["db"]
    host = configuration["connection"]["host"]
    port = configuration["connection"]["port"]

    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)

    connection.autocommit = True
    
    
    return connection

