from flask_mail import Message
from flask import current_app


class EmailService:
        
    @staticmethod
    def send_email(subject, recipients, body,  html=None):
        """
        Sends an email to the specified recipients.

        :param subject: Subject of the email.
        :param recipients: List of recipient email addresses.
        :param body: Plain text body of the email.
        :param html: HTML content of the email (optional).
        :return: True if email sent successfully, False otherwise.
        """
        try:
            msg = Message(subject, recipients=recipients, body=body, html=html)
            mail = current_app.extensions.get('mail')
            if not mail:
                raise RuntimeError("Mail extension is not initialized in the app.")
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to send email: {e}")
            return False