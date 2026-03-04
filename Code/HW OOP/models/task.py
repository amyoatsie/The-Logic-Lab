from dataclasses import dataclass
import datetime


@dataclass #doesn't do anything!
class Task: #a model of data, identifies each of the columns, defines what the data would look like
    id: int #type hints, for the programmer rather than the computer
    subject: str
    description: str
    due_date: str
    status: str


def is_valid_date(date_text): #helper function, outside of class but used in relation
    try:
        datetime.date.fromisoformat(date_text)
        return True
    except ValueError:
        return False


def to_date(date_text):
    return datetime.date.fromisoformat(date_text)