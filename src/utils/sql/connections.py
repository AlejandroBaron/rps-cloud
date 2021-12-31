import psycopg2
import urllib.parse as urlparse
import os



def connect_to_db() -> psycopg2.extensions.connection:
    """Returns a psycopg2 connection object to a POSTGRESQL database

    Returns:
        psycopg2.Connection: connection to the database
    """

    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
                )

    connection.autocommit = True
    
    
    return connection

