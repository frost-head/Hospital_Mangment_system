def fetchall(mysql, query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

def fetchone(mysql, query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchone()
    cur.close()
    return data

def insert(mysql, query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()

def delete(mysql, query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()

def update(mysql, query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
