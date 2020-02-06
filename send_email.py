import smtplib
import os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, to: [str], cc: [str] = [], bcc: [str] = [], filename=""):
    # Set identification
    sender_email = os.getenv("JUSTIFICATIF_EMAIL_ID")
    password = os.getenv("JUSTIFICATIF_EMAIL_PASSWORD")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ",".join(to)
    message["CC"] = ",".join(cc)
    message["Subject"] = subject  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # If an attachement is present include it in the email
    if filename:
        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            'content-disposition', 'attachment',
            filename=('utf-8', '', os.path.basename(filename))
        )

        # Add attachment to message
        message.attach(part)
    # Convert message to string
    text = message.as_string()

    # Log in to server using secure context and send email
    server = smtplib.SMTP("smtp.laposte.net:587")
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, to + cc + bcc + [sender_email], text)
