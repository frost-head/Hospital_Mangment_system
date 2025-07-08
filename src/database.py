def fetchall(mysql, query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params or ())
    data = cur.fetchall()
    cur.close()
    return data

def fetchone(mysql, query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params or ())
    data = cur.fetchone()
    cur.close()
    return data

def insert(mysql, query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params or ())
    mysql.connection.commit()
    cur.close()

def update(mysql, query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params or ())
    mysql.connection.commit()
    cur.close()

def delete(mysql, query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params or ())
    mysql.connection.commit()
    cur.close()

