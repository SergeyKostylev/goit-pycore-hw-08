import re
from collections import UserDict
from datetime import datetime, date, timedelta

DATE_FORMAT = "%d-%m-%Y"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def validate(self, value):
        if not re.fullmatch(r'^\d{10}$', value):
            raise ValueError(f"Invalid phone number: {value}")


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            raise ValueError(f"Invalid date format. Use {DATE_FORMAT}")

        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        br_day = self.get_birthday()

        return f"Contact name: {self.name.value}, {br_day}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, birthday_as_string):
        if self.birthday is not None:
            raise ValueError(f"Birthday already set")
        self.birthday = Birthday(birthday_as_string)

    def add_phone(self, param):
        self.phones.append(
            Phone(param)
        )

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def remove_phone(self, phone_number):
        for index, phone in enumerate(self.phones):
            if phone.value == phone_number:
                self.phones.pop(index)

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def get_birthday(self):
        br_day = self.birthday
        br_string = "Birthday: "
        br_string = br_string + ("not set " if br_day is None else br_day.value)

        return br_string


class AddressBook(UserDict):
    def add_record(self, record: Record):
        name = record.name.value
        if name in self.data:
            raise ValueError(f"Record name {name} already set")

        self.data[name] = record

    def find(self, name) -> Record:
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)

    def get_all(self) -> dict[Record, Record]:
        return self.data.values()

    def get_upcoming_birthdays(self):
        today = date.today()
        result = {}

        for name in self.data:
            record = self.data[name]
            if record.birthday is None:
                continue
            birthday = datetime.strptime(record.birthday.value, DATE_FORMAT).date()
            congratulation_date = date(today.year, birthday.month, birthday.day)
            count_days_to_congratulation = (congratulation_date - today).days
            if count_days_to_congratulation < 0 or count_days_to_congratulation > 7:
                continue

            weekday = congratulation_date.weekday()

            if weekday in [5, 6]:
                addDays = 2 if weekday == 5 else 1
                congratulation_date = congratulation_date + timedelta(days=addDays)

            if congratulation_date in result:
                result[congratulation_date].append(record)
            else:
                result[congratulation_date] = [record]

        return result
