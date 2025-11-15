from datetime import datetime
from typing import List
from project.src.email import Email
from project.src.status import Status


class EmailService:
    def __init__(self):
        self.sent_emails: List[Email] = []

    def add_send_date(self) -> str:
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        return formatted_date

    def send_email(self, email: Email) -> List[Email]:
        sent_emails_list = []
        prepared_email = email.prepare()

        if prepared_email.status == Status.INVALID:
            prepared_email.status = Status.FAILED
            self.sent_emails.append(prepared_email)
            return [prepared_email]


        for recipient in prepared_email.recipients:
            email_copy = Email(
                subject=prepared_email.subject,
                body=prepared_email.body,
                sender=prepared_email.sender,
                recipients=[recipient],
                date=self.add_send_date(),
                short_body=prepared_email.short_body,
                status=Status.SENT if prepared_email.status == Status.READY else Status.FAILED
            )

            sent_emails_list.append(email_copy)
            self.sent_emails.append(email_copy)

        return sent_emails_list


class LoggingEmailService(EmailService):
    def __init__(self, log_path="send.log"):
        super().__init__()
        self.log_path = log_path

    def send_email(self, email: Email) -> List[Email]:
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
