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
            smtp_server = getenv("SMTP_HOST")
            smtp_port = 465
            smtp_login = getenv("SMTP_USERNAME")
            smtp_password = getenv("SMTP_PASSWORD")

            print([smtp_server, smtp_port, smtp_login, smtp_password])
            if not all([smtp_server, smtp_port, smtp_login, smtp_password]):
                raise ValueError("SMTP configuration is incomplete. Check environment variables.")


            msg = MIMEMultipart("alternative")
            msg['From'] = "support@jobstate.com"
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'html'))


            # Send email
            if smtp_port == 465:
                    # SSL connection
                    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                        server.login(smtp_login, smtp_password)
                        server.sendmail(smtp_login, recipient_email, msg.as_string())
            elif smtp_port == 587:
                    # STARTTLS connection
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(smtp_login, smtp_password)
                        server.sendmail(smtp_login, recipient_email, msg.as_string())
            else:
                    raise ValueError(f"Unsupported SMTP port: {smtp_port}")
        except Exception as exc:
            raise_error(exc)


    