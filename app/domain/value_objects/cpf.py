import re


class CPF:
    def __init__(self, value: str):
        cleaned = re.sub(r'\D', '', value)
        if not re.match(r'^\d{11}$', cleaned):
            raise ValueError("Invalid CPF format")
        self.value = cleaned

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return isinstance(other, CPF) and self.value == other.value

    def __hash__(self):
        return hash(self.value)
