import pandas as pd

pd.set_option('max_columns', None)
pd.set_option('max_colwidth', 20)

def show():
    import sqlite3

    # Create a SQL connection to our SQLite database
    con = sqlite3.connect("data/jobstatus.db")

    # cur = con.cursor()
    # # The result of a "cursor.execute" can be iterated over by row
    # for row in cur.execute('SELECT * FROM jobs;'):
    #     print(row)

    df = pd.read_sql_query("select * from jobs;", con)
    print(df.tail())

    # Be sure to close the connection
    con.close()


if __name__ == '__main__':
    show()