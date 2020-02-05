import text_generator
import download_attestation
import send_email
from datetime import date
import os.path
import database_interface


def handle_exception(user, exception_msg):
    database_interface.report_non_functional_user(user.user_id)
    body, subject = text_generator.get_email_text_invalid_token()
    send_email.send_email(subject, body, user.email)
    return exception_msg


def handle_valid_user(user):
    year = date.today().year
    month = date.today().month

    if not database_interface.is_attestation_sent_for_month(user.user_id, month, year):
        error_msg = ""
        try:
            body, subject = text_generator.get_email_text(user.first_name, user.last_name, year, month)
            filename = f"{user.first_name.upper()}_{user.last_name.upper()}_{month}_{year}_attestation_navigo.pdf"
            filename = os.path.join["downloaded_attestation", filename]
            download_attestation.download_attestation(user.navigo_id, user.navigo_token, filename, month, year)
            send_email.send_email(subject, body, [user.email], filename)
        except Exception as e:
            error_msg = handle_exception(user, str(e))
        database_interface.add_attestation(user_id=user.user_id, error_msg=str(error_msg))


def main():
    for user in database_interface.get_all_valid_users():
        handle_valid_user(user)


if __name__== "__main__":
    main()