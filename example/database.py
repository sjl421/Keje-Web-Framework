import MySQLdb

db = MySQLdb.connect(host="localhost", user="", passwd="", db="")

cur = db.cursor()

def add_user(id, name):
    query = 'INSERT INTO users (id, name) VALUES ("{id}", "{name}");'.format(id=id, name=name)
    cur.execute(query)
    db.commit()

def remove_all():
    query = 'truncate users'
    cur.execute(query)
    db.commit()

def get_users():
    cur.execute("select * from users")
    users = []
    for row in cur.fetchall():
        _user = { 'id': row[0], 'name': row[1]}
        users.append(_user)
    return users

def get_user(id):
    query = 'select id,name from users where id={id};'.format(id=id)
    cur.execute(query)
    users = []
    for row in cur.fetchall():
        _user = { 'id': row[0], 'name': row[1]}
        users.append(_user)
    if(len(users) == 0):
        return {}
    else:
        return users[0]

def delete_user(id):
    query = 'DELETE FROM users WHERE id={id};'.format(id=id)
    cur.execute(query)
    db.commit()
