import sqlite3
import argparse
from performance_summary.db_commands import Users

def create_db(conn):
    pp = conn.cursor()
    pp.executescript('drop table if exists users;')

    try:
        pp.executescript("begin")
        pp.executescript("""
        CREATE TABLE users
            (id INTEGER PRIMARY KEY, username varchar(20), admin INTEGER,  UNIQUE(username));
        """)
        pp.executescript("commit")
        return True
    except conn.Error as e:
        pp.executescript("rollback")
        print(e.args[0])
        return False

def main():
    parser = argparse.ArgumentParser(description='creates db tables required for PanelPal program')
    parser.add_argument('--db')
    parser.add_argument('--users', default='dnamdp,cytng,gencph,genes,dnanhc')
    args = parser.parse_args()


    db = args.db
    print(db)

    conn_main = sqlite3.connect(db)
    complete = create_db(conn_main)
    u = Users()
    if not complete:
        print "Database creation failed. Exiting."
        exit()
    if args.users is not None:
        users = args.users.split(',')
        for user in users:
            complete = u.add_user(user, 1)
            if complete == -1:
                print user + " not added to database"


if __name__ == '__main__':
    main()
