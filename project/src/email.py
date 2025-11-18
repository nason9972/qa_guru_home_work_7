from dataclasses import dataclass
from typing import List, Optional

from project.src.email_address import EmailAddress
from project.src.status import Status
from project.src.utils import clean_text


@dataclass
class Email:
    subject: str
    body: str
    sender: EmailAddress
    recipients: List[EmailAddress] | EmailAddress
    date: Optional[str] = None
    short_body: Optional[str] = None
    status: Status = Status.DRAFT

    def __post_init__(self):
        if not isinstance(self.recipients, list):
            self.recipients = [self.recipients]

    def get_recipients_str(self) -> str:
        email_addresses = []
        for recipient in self.recipients:
            email_addresses.append(str(recipient))
        return ", ".join(email_addresses)

    def clean_data(self) -> "Email":
        self.subject = clean_text(self.subject)
        self.body = clean_text(self.body)
        return self

    def add_short_body(self, n=10) -> "Email":
        if not self.body:
            return self
        if len(self.body) > n:
            self.short_body = self.body[:n] + '...'
        else:
            self.short_body = self.body
        return self

    def is_valid_fields(self) -> bool:
        return (
            bool(self.body)
            and bool(self.subject)
            and bool(self.sender)
            and bool(self.recipients)
        )

    def prepare(self):
        cleaned_email = self.clean_data()
        self.subject = cleaned_email.subject
        self.body = cleaned_email.body
        if self.is_valid_fields():
            self.status = Status.READY
        else:
            self.status = Status.INVALID
        return self

    def __repr__(self):
        recipients_str = self.get_recipients_str()
        return (
            f"Status: {self.status}\n"
            f"Кому: {recipients_str}\n"
            f"От: {self.sender.masked}\n"
            f"Тема: {self.subject}, дата {self.date}\n"
            f"{self.short_body or self.body}"
        )