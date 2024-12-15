from flask_mail import Message

class EmailService:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
            
    def init_app(self, app):
        self.app = app
        
    def send_email(self, subject, recipients, body, html=None):
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
            mail = self.app.extensions.get('mail')
            if not mail:
                raise RuntimeError("Mail extension is not initialized in the app.")
            mail.send(msg)
            return True
        except Exception as e:
            self.app.logger.error(f"Failed to send email: {e}")
            return False
