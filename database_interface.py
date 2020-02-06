from collections import namedtuple
import mysql.connector
from os import getenv

navigo_db = mysql.connector.connect(
    host=getenv("MYSQL_SERVER", "localhost"),
    user=getenv("MYSQL_USER"),
    passwd=getenv("MYSQL_PASSWORD"),
    database="navigodb",
)
UserRecord = namedtuple("UserRecord", "first_name, last_name, email, navigo_id, navigo_token,user_id")


def get_all_valid_users():
    cursor = navigo_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE functional=1")
    result = []
    for row in cursor.fetchall():
        result.append(
            UserRecord(row["first_name"], row["last_name"], row["email"], row["navigo_pass_id"], row["navigo_token"],
                       row["id"]))
    return result


def add_attestation(user_id, error_msg=""):
    try:
        cursor = navigo_db.cursor()

        cursor.execute("INSERT INTO sent_attestation (user_id, error_msg, status) "
                       "VALUES (%(user_id)s, %(error_msg)s, %(status)s);",
                       {'user_id': user_id, 'error_msg': error_msg, 'status': 1 if error_msg else 0})

        navigo_db.commit()
    except:
        return False
    return True


def report_non_functional_user(user_id):
    cursor = navigo_db.cursor()

    cursor.execute("UPDATE users SET functional = 0 where id=%(user_id)s;",
                   {'user_id': user_id})
    navigo_db.commit()


def is_attestation_sent_for_month(user_id, month, year):
    cursor = navigo_db.cursor(dictionary=True)
    cursor.execute("SELECT sent_at FROM sent_attestation WHERE user_id=%(user_id)s;", {'user_id': user_id})
    for row in cursor.fetchall():
        if row['sent_at'].month == month and row['sent_at'].year == year:
            return True;
    return False


def add_user(user: UserRecord):
    try:
        cursor = navigo_db.cursor()

        cursor.execute("INSERT INTO users (first_name, last_name, email, navigo_token, navigo_pass_id) "
                       "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(navigo_token)s,%(navigo_pass_id)s);",
                       {'first_name': user.first_name, 'last_name': user.last_name,
                        'navigo_token': user.navigo_token, 'navigo_pass_id': user.navigo_id, 'email': user.email})

        navigo_db.commit()
    except:
        return False
    return True