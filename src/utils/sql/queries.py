import psycopg2.extensions

def check_for_table(cursor: psycopg2.extensions.cursor, table_name: str) -> bool:
    """Checks if table exists in the database to which cursor is pointing

    Args:
        cursor (psycopg2.cursor): cursor obtained from connection to the database
        table_name (str): table name

    Returns:
        bool: Whether table exists or not
    """
    
    cursor.execute("select exists(select * from information_schema.tables where table_name=%s)", (table_name,))
    return cursor.fetchone()[0]

def drop_table(cursor: psycopg2.extensions.cursor, name: str):
    """Drops the transition matrix for the specified depth

    Args:
        cursor (psycopg2.extensions.cursor): cursor pointing to the database
        name (str): table name
    """

    # First, create the transition matrix table for the specified depth
    query = f'''DROP TABLE {name}'''
    cursor.execute(query)

def init_transition_table(cursor: psycopg2.extensions.cursor, depth: int, initial_records: list[dict]):
    """Inits and populates the transition matrix for the desired table

    Args:
        cursor (psycopg2.extensions.cursor): cursor pointing to the database
        depth (int): transition matrix depth
        initial_records (list[dict]): list of dicts representing the initial table values
    """

    # First, create the transition matrix table for the specified depth
    query = f'''CREATE TABLE IF NOT EXISTS transitionmatrix{depth} (
                                                                    Hist VARCHAR NOT NULL UNIQUE,
                                                                    R FLOAT NOT NULL,
                                                                    P FLOAT NOT NULL,
                                                                    S FLOAT NOT NULL
                                                                    )'''
    cursor.execute(query)

    # Now, populate the tabl
    query = f"INSERT INTO transitionmatrix{depth}"+ " VALUES (%(Hist)s, %(R)s, %(P)s, %(S)s)"
    cursor.executemany(query, initial_records)

def init_stats_table(cursor: psycopg2.extensions.cursor, initial_records: list[dict]):
    """Inits and populates the transition matrix for the desired table

    Args:
        cursor (psycopg2.extensions.cursor): cursor pointing to the database
    """

    # First, create the transition matrix table for the specified depth
    query = f'''CREATE TABLE IF NOT EXISTS statistics (Depth INTEGER NOT NULL UNIQUE,
                                                              W INTEGER NOT NULL,
                                                              T INTEGER NOT NULL,
                                                              L INTEGER NOT NULL
                                                             )'''
    cursor.execute(query)

    # Now, populate the tabl
    query = f"INSERT INTO statistics"+ " VALUES (%(Depth)s, %(W)s, %(T)s, %(L)s)"
    cursor.executemany(query, initial_records)
