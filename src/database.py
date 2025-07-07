
def fetchall(mysql, querry):
    # cur =mysql.connect.cursor()
    cur = mysql.get_db().cursor()
    cur.execute("{}".format(querry))
    data = cur.fetchall()
    cur.close()
    return data


def fetchone(mysql, querry):
    cur = mysql.get_db().cursor()
    # cur =mysql.connect.cursor()
    cur.execute("{}".format(querry))
    data = cur.fetchone()
    cur.close()
    return data


def insert(mysql, querry):
    cur = mysql.get_db().cursor()
    # cur =mysql.connect.cursor()
    cur.execute("{}".format(querry))
    # mysql.connect.commit()
    cur.close()
    return

def delete(mysql, querry):
    cur = mysql.get_db().cursor()
    # cur =mysql.connect.cursor()
    cur.execute("{}".format(querry))
    # mysql.connect.commit()
    cur.close()
    return

def update(mysql, querry):
    cur = mysql.get_db().cursor()
    # cur =mysql.connect.cursor()
    cur.execute("{}".format(querry))
    # mysql.connect.commit()
    cur.close()
    return
