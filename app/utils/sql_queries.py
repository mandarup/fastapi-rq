import pandas as pd
import sqlite3

pd.set_option('max_columns', None)
pd.set_option('max_colwidth', 50)


def get_all_records():

    # Create a SQL connection to our SQLite database
    # con = sqlite3.connect("data/jobstatus.db")

    # cur = con.cursor()
    # # The result of a "cursor.execute" can be iterated over by row
    # for row in cur.execute('SELECT * FROM jobs;'):
    #     print(row)

    # df = pd.read_sql_query("select * from jobs;", con)
    # print(df)

    # Be sure to close the connection
    # con.close()

    with sqlite3.connect("data/jobstatus.db") as con:
        df = pd.read_sql_query("select * from jobs;", con)
    return df#.to_dict(orient='records')



def delete_old_records(days='7'):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    con = sqlite3.connect("data/jobstatus.db")
    sql = "DELETE FROM jobs WHERE finishedat <= date('now','-{days} day')"
    cur = con.cursor()
    cur.execute(sql)
    con.close()



if __name__ == '__main__':
    # print(get_all_records())
    delete_old_records(-1)
    print(get_all_records())