from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv
import smtplib

from dotenv import load_dotenv

from errors import raise_error

load_dotenv()
class EmailService:
    @staticmethod
    async def send_email(
        recipient_email: str,
        subject: str,
        message: str
        ):
        """
        Sends an email to a user

        recipient_email (str) : Email of the recipient/receiver
        """
        try:
            smtp_server = getenv("SMTP_SERVER")
            smtp_port = getenv("SMTP_PORT")
            smtp_login = getenv("SMTP_USERNAME")
            smtp_password = getenv("SMTP_PASSWORD")

            msg = MIMEMultipart("alternative")
            msg['From'] = "support@jobstate.com"
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'html'))
            print(smtp_login)
            print(smtp_password)

            # Send email
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_login, smtp_password)
                server.sendmail("support@jobstate.com", recipient_email, msg.as_string())
        except Exception as exc:
            raise_error(exc)