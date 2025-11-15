

class EmailAddress:
    def __init__(self, address: str):
        address = self.normalize_address(address)
        if self._check_correct_email(address):
            self._address = address
        else:
            raise ValueError(f"Неправильный email: {address}")

    @staticmethod
    def normalize_address(address):
        return address.lower().strip()

    def _check_correct_email(self, address):
        if "@" not in address:
            return False
        if address.endswith(".com"):
            return True
        if address.endswith(".ru"):
            return True
        if address.endswith(".net"):
            return True

    @property
    def masked(self):
        login = self._address.split("@")[0]
        domain = self._address.split("@")[-1]
        return login[:2] + "***@" + domain

    @property
    def address(self):
        return self._address