import sqlite3

def load(df, db_name = "employee.db", table_name = "employees"):
    print("Loading data into SQLite3 database . . .")

    connected = sqlite3.connect(db_name) # initializes database for employees
    df.to_sql(table_name, connected, if_exists = "replace", index = False)   # transforms data --> SQL table

    connected.close()

    print(f"Data has been successfully loaded into {db_name} → table: {table_name}")