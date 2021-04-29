import sqlite3, base64

def init_db():
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT, username TEXT, chat_id TEXT, addition BOOLEAN, regexp_addition BOOLEAN, regexp_deletion BOOLEAN, deletion BOOLEAN, add_link_flag BOOLEAN, add_regexp_flag BOOLEAN, temp_name TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS targets (name TEXT, link TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS ignores (name TEXT, regexp TEXT)")
    connection.close()

def user_exist(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT user_id from users WHERE user_id=" + str(update.effective_user.id)).fetchone()
    connection.close()

    if result:
        return True
    else:
        return False

def create_user(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, False, False, False, False, False, False, 'NULL')", (str(update.effective_user.id), str(update.effective_user.username), str(update.effective_chat.id)))
    connection.commit()
    connection.close()


def user_is_edit(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    regexp_addition = cursor.execute("SELECT regexp_addition from users WHERE user_id=" + str(update.effective_user.id)).fetchone()
    regexp_deletion = cursor.execute("SELECT regexp_deletion from users WHERE user_id=" + str(update.effective_user.id)).fetchone()
    addition = cursor.execute("SELECT addition from users WHERE user_id=" + str(update.effective_user.id)).fetchone()
    deletion = cursor.execute("SELECT deletion from users WHERE user_id=" + str(update.effective_user.id)).fetchone()
    connection.close()

    if deletion[0] == 1:
        return 'delete'
    if addition[0] == 1:
        return 'add'
    if regexp_addition[0] == 1:
        return 'add_regexp'
    if regexp_deletion[0] == 1:
        return 'delete_regexp'
    else:
        return 'no'

def user_reset(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET addition = False WHERE user_id =" + str(update.effective_user.id))
    cursor.execute("UPDATE users SET deletion = False WHERE user_id =" + str(update.effective_user.id))
    cursor.execute("UPDATE users SET add_link_flag = False WHERE user_id =" + str(update.effective_user.id))
    cursor.execute("UPDATE users SET temp_name = 'NULL' WHERE user_id =" + str(update.effective_user.id))
    cursor.execute("UPDATE users SET regexp_addition = False WHERE user_id =" + str(update.effective_user.id))
    cursor.execute("UPDATE users SET regexp_deletion = False WHERE user_id =" + str(update.effective_user.id))
    cursor.execute("UPDATE users SET add_regexp_flag = False WHERE user_id =" + str(update.effective_user.id))
    connection.commit()
    connection.close()


def user_delete(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET deletion = True WHERE user_id =" + str(update.effective_user.id))
    connection.commit()
    connection.close()

def regexp_delete(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET regexp_deletion = True WHERE user_id =" + str(update.effective_user.id))
    connection.commit()
    connection.close()

def user_add(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET addition = True WHERE user_id =" + str(update.effective_user.id))
    connection.commit()
    connection.close()

def regexp_add(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET regexp_addition = True WHERE user_id =" + str(update.effective_user.id))
    connection.commit()
    connection.close()

def check_link_flag(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    flag = cursor.execute("SELECT add_link_flag from users WHERE user_id=" + str(update.effective_user.id)).fetchone()
    connection.close()

    if flag[0] == 1:
        return True
    else:
        return False

def check_regexp_flag(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    flag = cursor.execute("SELECT add_regexp_flag from users WHERE user_id=" + str(update.effective_user.id)).fetchone()
    connection.close()

    if flag[0] == 1:
        return True
    else:
        return False


def link_flag_reset(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET add_link_flag = True WHERE user_id =" + str(update.effective_user.id))
    connection.commit()
    connection.close()

def regexp_flag_reset(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET add_regexp_flag = True WHERE user_id =" + str(update.effective_user.id))
    connection.commit()
    connection.close()

def set_temp_name(update, name):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET temp_name = '" + name +  "' WHERE user_id =" + str(update.effective_user.id))
    connection.commit()
    connection.close()

def target_name_exists(name):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT name from targets WHERE name='" + str(name) + "'").fetchone()
    connection.close()

    if result:
        return True
    else:
        return False


def regexp_name_exists(name):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT name from ignores WHERE name='" + str(name) + "'").fetchone()
    connection.close()

    if result:
        return True
    else:
        return False

def get_temp_name(update):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT temp_name FROM users WHERE user_id=" + str(update.effective_user.id)).fetchall()
    connection.close()
    return result[0][0]


def get_targets():
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT * from targets").fetchall()
    connection.close()
    return result

def get_ignores():
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT * from ignores").fetchall()
    connection.close()
    return result

def get_links():
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT link from targets").fetchall()
    connection.close()
    return result

def get_chats():
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT chat_id from users").fetchall()
    connection.close()
    return result

def add_target(name, link):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO targets VALUES (?, ?)",(name, link))
    connection.commit()
    connection.close()

def add_regexp(name, regexp):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO ignores VALUES (?, ?)",(name, base64.b64encode((str(regexp).encode("ascii"))).decode("ascii")))
    connection.commit()
    connection.close()

def delete_regexp(name):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ignores WHERE name='" + str(name).replace("'",'').replace("--","").replace(";","") + "'")
    connection.commit()
    connection.close()

def delete_target(name):
    connection = sqlite3.connect("pauchek.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM targets WHERE name='" + str(name).replace("'",'').replace("--","").replace(";","") + "'")
    connection.commit()
    connection.close()