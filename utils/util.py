
import sqlite3


def run_sql():
    try :
        con = sqlite3.connect('db/todo.db')
        cur = con.cursor()
        print('connected to database ')
    except :print('cant connect to database')

    try:
        cur.executescript(
            '''
            CREATE TABLE IF NOT EXISTS User(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                email TEXT UNIQUE,
                name TEXT,
                password TEXT

            );
            
            CREATE TABLE IF NOT EXISTS Todo(
                id INTEGER NOT NULL UNIQUE,
                title TEXT,
                user_id INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            '''
        )
        con.commit()
        print('tables created')
        cur.close()
    except : print('error executing')
    return con





def addTask(user_email,task):
    
    con = run_sql()
    cur = con.cursor()
    cur.execute("SELECT id FROM User WHERE email=?",(user_email,))
    user_id = cur.fetchone()[0]
    print(user_id)
    cur.execute("INSERT INTO Todo (title,user_id) VALUES (?,?)",(task,user_id,))
    con.commit()
    cur.close()
    resp = {'email':user_email,"task":task}
    return resp
#addTask('c@c.com','do the shit')

def getTasks(user_email):
    con = run_sql()
    cur = con.cursor()
    cur.execute("SELECT id FROM User WHERE email=?",(user_email,))
    user_id = cur.fetchone()[0]
    cur.execute("SELECT title FROM Todo WHERE user_id=?",(user_id,))
    result = cur.fetchall()
    resp = {"email": user_email,'tasks':result}
    print(result)
    con.commit()
    cur.close()
    return resp

#getTasks('a@a.com')

def updateTask(user_email, taskTitle,task_id):
    con = run_sql()
    cur = con.cursor()
    cur.execute("SELECT id FROM User WHERE email=?",(user_email,))
    user_id = cur.fetchone()[0]
    x = cur.execute("UPDATE Todo SET title =? WHERE id = ? AND user_id=?",(taskTitle,task_id,user_id,))
    print(x.rowcount)
    if x.rowcount > 0:
        con.commit()
        result ='record updated'
    else : result ='process failed'
    cur.close()
    return {'message': result}



def deleteTask(user_email,task_id):
    con = run_sql()
    cur = con.cursor()
    try :
        cur.execute("SELECT id FROM User WHERE email=?",(user_email,))
        user_id = cur.fetchone()[0]
        x = cur.execute("DELETE FROM Todo where id =? AND user_id=?",(task_id,user_id,))
        if x.rowcount != 0 :
            con.commit()
            result = {'message': 'record delete'}
            cur.close()
        else : result = {'message': 'no record found'}
    except :
        result = {'message': 'error'}
    print('->',result)
    return {'message':result}
    



