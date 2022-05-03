
def fetchall(mysql, querry):
    cur = mysql.connection.cursor()
    cur.execute("{}".format(querry))
    data = cur.fetchall()
    cur.close()
    return data


def fetchone(mysql, querry):
    cur = mysql.connection.cursor()
    cur.execute("{}".format(querry))
    data = cur.fetchone()
    cur.close()
    return data


def insert(mysql, querry):
    cur = mysql.connection.cursor()
    cur.execute("{}".format(querry))
    mysql.connection.commit()
    cur.close()
    return

def delete(mysql, querry):
    cur = mysql.connection.cursor()
    cur.execute("{}".format(querry))
    mysql.connection.commit()
    cur.close()
    return

def update(mysql, querry):
    cur = mysql.connection.cursor()
    cur.execute("{}".format(querry))
    mysql.connection.commit()
    cur.close()
    return
