import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
import sys

def extract_data(filepath):
    print(f"Loading data from path: {filepath}")
    df = pd.read_csv(filepath)

    print(f"Loaded {filepath} and has {df.shape[0]} rows")
    return df

def create_db_conn(dbname, user, password, host='localhost', port=5432):
    print("Connecting to DB...")
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connected to DB!")
        return conn
    except Exception as e:
        print(f"Error connecting to DB: {e}", file=sys.stderr)
        return None

def create_table(conn, table_name):
    print("Creating table...")

    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
          id SERIAL PRIMARY KEY, 
          rank INT,
          name VARCHAR(255),  
          platform VARCHAR(100), 
          year INT,
          genre VARCHAR(100),
          publisher VARCHAR(255), 
          na_sales FLOAT,
          eu_sales FLOAT,
          jp_sales FLOAT,
          other_sales FLOAT,
          global_sales FLOAT 
        );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        print(f"Table '{table_name}' is ready")
    except Exception as e:
        print(f"Error creating table: {e}", file=sys.stderr)
    print("Creating table...")

    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
          id SERIAL PRIMARY KEY, 
          rank INT,
          name VARCHAR(50),
          platform VARCHAR(100),
          year INT,
          genre VARCHAR(100),
          publisher VARCHAR(100),
          na_sales FLOAT,
          eu_sales FLOAT,
          jp_sales FLOAT,
          other_sales FLOAT,
          global_sales FLOAT 
        );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        print(f"Table '{table_name}' is ready")
    except Exception as e:
        print(f"Error creating table: {e}", file=sys.stderr)

def insert_data(conn, df, table_name):
    print("Inserting data...")

    COLUMNS_ORDER = [
        'rank', 'name', 'platform', 'year', 'genre', 'publisher', 
        'na_sales', 'eu_sales', 'jp_sales', 'other_sales', 'global_sales'
    ]

    df_reordered = df[COLUMNS_ORDER]
    
    if df_reordered is not None:
        df_reordered = df_reordered.where(pd.notnull(df_reordered), None)

    records = [tuple(x) for x in df_reordered.to_numpy()]

    columns_to_insert = ', '.join(df_reordered.columns) 
    
    sql_query = f"""INSERT INTO "{table_name}" ({columns_to_insert}) VALUES %s"""

    try:
        cursor = conn.cursor()
        execute_values(cursor, sql_query, records)
        conn.commit()
        print(f"Successfully inserted {len(records)} rows into '{table_name}'.")
        cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}", file=sys.stderr)


def get_data(conn, table_name):
    print("Getting Data...")
    try:
        cur = conn.cursor()
        cur.execute(f""" SELECT * FROM "{table_name}" LIMIT 10 """)
        colnames = [desc[0] for desc in cur.description]
        print("Columns: ", colnames)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
    except Exception as e:
        print(f"Error getting data: {e}", file=sys.stderr)


def main():
    filepath = r'C:\Users\genti\Desktop\Learning Python\DataCleaningExercises\Video Games Sales\cleaned_videogames_sales.csv' 
    
    db_config = {
        'dbname': 'Videogame Sales',
        'user': 'postgres',
        'password': 'admini',
        'host': 'localhost',
        'port': 5432
    }

    TABLENAME = 'videogame_sales'

    df = extract_data(filepath)

    conn = create_db_conn(
        dbname=db_config["dbname"], 
        host=db_config["host"], 
        password=db_config["password"], 
        user=db_config['user'], 
        port=db_config['port']
    )
    
    if conn is None:
        return

    try:
        create_table(conn, TABLENAME)
        insert_data(conn, df, TABLENAME)
        get_data(conn, TABLENAME)
    except Exception as e:
        print(f"Main Error: {e}", file=sys.stderr)
    finally:
        conn.close()
        print("DB Connection is closed")

main()