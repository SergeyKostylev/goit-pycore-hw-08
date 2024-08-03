from models.main_models import *


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"

    return inner


@input_error
def add_contact(args, book: AddressBook):
    try:
        name, phone = args
    except ValueError:
        raise ValueError("Give me name and phone please.")

    record = book.find(name)

    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
        record.add_phone(phone)

    return message


@input_error
def add_birthday(args, book: AddressBook):
    try:
        name, dr_day = args
    except ValueError:
        raise ValueError("Give me name and birthday please.")

    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} does not exist.")

    record.add_birthday(dr_day)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    try:
        name, = args
    except ValueError:
        raise ValueError("Give me name and birthday please.")

    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} does not exist.")

    return record.get_birthday()


@input_error
def change_username_phone(args, book: AddressBook):
    try:
        name, phone_old, phone_new = args
    except ValueError:
        raise ValueError("Give me name and phone please.")

    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} does not exist.")

    record.edit_phone(phone_old, phone_new)


@input_error
def render_contacts(book: AddressBook):
    records = book.get_all()
    if not records:
        return "Address book is empty."

    for record in records:
        print(record)
    return


@input_error
def phone_username(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return f"Unknown contact {name}."

    return str(record)


@input_error
def get_week_birthdays(book: AddressBook):
    records = book.get_upcoming_birthdays()
    if not records:
        return "There are not birthday people this week."

    res = ""
    for day, records in records.items():
        res += f"{day}:\n"
        for record in records:
            res += f"\t{record.name}\n"

    return res


def main():
    book = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        output = ''

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            output = add_contact(args, book)
        elif command == "change":
            output = change_username_phone(args, book)
        elif command == "phone":
            output = phone_username(args, book)
        elif command == "all":
            render_contacts(book)
        elif command == "add-birthday":
            output = add_birthday(args, book)
        elif command == "show-birthday":
            output = show_birthday(args, book)
        elif command == "bi":
            output = get_week_birthdays(book)
        else:
            print("Invalid command.")

        print(output)


if __name__ == "__main__":
    main()
