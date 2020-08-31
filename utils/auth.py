import sqlite3
from datetime import datetime


def signUP(email, name, password):
    PATH_DB = 'db/todo.db'

    try :
        con = sqlite3.connect(PATH_DB)
        print('connected to database ')
    except :
        print('cant connect to database')

    #created = datetime.utcnow()
    cur = con.cursor()
    x = cur.execute("INSERT OR IGNORE INTO User (email,name,password) VALUES (?,?,?)",(email, name, password,))
    if x.rowcount == 1 :
        con.commit()
        cur.close()
        resp={'message':'account added'}
    else : resp={'message':'email already exist'}
    return resp

#signUP('k@aak.caoam','amine',"aha545")

def signIN(email):
    PATH_DB = 'db/todo.db'

    try :
        con = sqlite3.connect(PATH_DB)
        print('connected to database ')
    except :
        print('cant connect to database')
    cur = con.cursor()
    cur.execute("SELECT * FROM User WHERE email=?",(email,))
    rv = cur.fetchone()
    if rv : print('succef logged')
    cur.close()
    return rv
