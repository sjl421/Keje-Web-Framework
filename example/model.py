import database

def users():
    return database.get_users()

def user(id):
    return database.get_user(id)

def post_create_user(id, name):
    return database.add_user(id, name)

def post_delete_user(id):
    return database.delete_user(id)