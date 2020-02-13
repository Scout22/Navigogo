from collections import namedtuple
import mysql.connector
from os import getenv

navigo_db_config = {
    'host':getenv("MYSQL_SERVER", "localhost"),
    'user':getenv("MYSQL_USER"),
    'passwd':getenv("MYSQL_PASSWORD"),
    'database':"navigodb",
}

UserRecord = namedtuple("UserRecord", "first_name, last_name, email, navigo_id, navigo_token,user_id, organization_id")


def get_all_valid_users():
    navigo_db = mysql.connector.connect(**navigo_db_config)
    cursor = navigo_db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE functional=1")
    result = []
    for row in cursor.fetchall():
        result.append(
            UserRecord(row["first_name"], row["last_name"], row["email"], row["navigo_pass_id"], row["navigo_token"],
                       row["id"], row["organization_id"]))
    cursor.close()
    navigo_db.close()

    return result

def get_organization_email(organization_id:int):
    try:
        navigo_db = mysql.connector.connect(**navigo_db_config)
        cursor = navigo_db.cursor()
        cursor.execute(f"SELECT organization_email from organizations WHERE id = {organization_id};")
        return cursor.fetchone()[0]

    except Exception as e:
        print(f"Error in get_organization_email {e}")
        return ""


def add_attestation(user_id, error_msg=""):
    try:
        navigo_db = mysql.connector.connect(**navigo_db_config)
        cursor = navigo_db.cursor()

        cursor.execute("INSERT INTO sent_attestation (user_id, error_msg, status) "
                       "VALUES (%(user_id)s, %(error_msg)s, %(status)s);",
                       {'user_id': user_id, 'error_msg': error_msg, 'status': 1 if error_msg else 0})

        navigo_db.commit()
        cursor.close()
        navigo_db.close()

    except Exception as e:
        print(f"Error in add attestation {e}")
    return True


def report_non_functional_user(user_id):
    navigo_db = mysql.connector.connect(**navigo_db_config)
    cursor = navigo_db.cursor()

    cursor.execute("UPDATE users SET functional = 0 where id=%(user_id)s;",
                   {'user_id': user_id})
    navigo_db.commit()
    cursor.close()
    navigo_db.close()


def is_attestation_sent_for_month(user_id, month, year):
    navigo_db = mysql.connector.connect(**navigo_db_config)
    cursor = navigo_db.cursor(dictionary=True)
    cursor.execute("SELECT sent_at FROM sent_attestation WHERE user_id=%(user_id)s;", {'user_id': user_id})
    for row in cursor.fetchall():
        if row['sent_at'].month == month and row['sent_at'].year == year:
            return True;
    return False


def add_user(user: UserRecord):
    try:
        navigo_db = mysql.connector.connect(**navigo_db_config)
        cursor = navigo_db.cursor()

        cursor.execute("INSERT INTO users (first_name, last_name, email, navigo_token, navigo_pass_id) "
                       "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(navigo_token)s,%(navigo_pass_id)s);",
                       {'first_name': user.first_name, 'last_name': user.last_name,
                        'navigo_token': user.navigo_token, 'navigo_pass_id': user.navigo_id, 'email': user.email})

        navigo_db.commit()
        cursor.close()
        navigo_db.close()
    except Exception as e:
        print(f"Error in add User {e}")
        return False
    return True
