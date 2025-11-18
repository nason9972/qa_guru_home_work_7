from datetime import datetime
from typing import List
from project.src.email import Email
from project.src.status import Status
from copy import deepcopy

class EmailService:

    def __init__(self, email: Email):
        self.email = email

    @staticmethod
    def add_send_date() -> str:
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        return formatted_date

    def send_email(self):
        emails = []
        for recipient in self.email.recipients:
            email_copy = deepcopy(self.email)
            email_copy.date = self.add_send_date()
            email_copy.recipients = [recipient]
            if email_copy.status == Status.READY:
                email_copy.status = Status.SENT
            else:
                email_copy.status = Status.FAILED
            emails.append(email_copy)
        return emails


class LoggingEmailService(EmailService):
    def __init__(self,email: Email, log_path="send.log"):
        super().__init__(email)
        self.log_path = log_path

    def send_email(self) -> List[Email]:
        result = super().send_email(email)

        with open(self.log_path, "a", encoding="utf-8") as f:
            for sent_email in result:
                f.write(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                    f"Status: {sent_email.status}, "
                    f"From: {sent_email.sender.address}, "
                    f"To: {sent_email.get_recipients_str()}, "
                    f"Subject: {sent_email.subject}\n"
                )

        return result
