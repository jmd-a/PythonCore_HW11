from collections import UserDict
from datetime import datetime, timedelta

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input."
        except IndexError:
            return "Invalid input."
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def update(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass

class Birthday:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

    def update(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            self.value = value
        except ValueError:
            raise ValueError

class Record:
    def __init__(self, name_value, birthday_value=None):
        self.name = Name(name_value)
        self.birthday = Birthday(birthday_value)
        self.phones = []

    def add_phone(self, phone_number):
        self.phones.append(phone_number)

    def remove_phone(self, index):
        if 0 <= index < len(self.phones):
            del self.phones[index]

    def edit_phone(self, index, new_number):
        if 0 <= index < len(self.phones):
            self.phones[index].update(new_number)

    def days_to_birthday(self):
        if not self.birthday.value:
            return "Birthday not set."
        today = datetime.today()
        next_birthday = datetime(today.year, int(self.birthday.value[5:7]), int(self.birthday.value[8:10]))
        if next_birthday < today:
            next_birthday = datetime(today.year + 1, int(self.birthday.value[5:7]), int(self.birthday.value[8:10]))
        days = (next_birthday - today).days
        return f"Days until next birthday: {days}"
    
    def __str__(self):
        phone_str = ", ".join(str(phone) for phone in self.phones)
        return f"Name: {self.name}, Phones: {phone_str}, Birthday: {self.birthday}"

class AddressBook(UserDict):
    def __iter__(self):
        return self.iterator()

    def iterator(self, N=10):
        records = list(self.data.values())
        for i in range(0, len(records), N):
            yield records[i:i + N]

    def add_record(self, record):
        self.data[record.name.value] = record

    def search(self, query):
        results = []
        for record in self.data.values():
            if query in record.name.value:
                results.append(record)
            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
                    break
        return results

contacts = AddressBook()

@input_error
def add_contact(name, phone, birthday=None):
    record = Record(name, birthday)
    record.add_phone(phone)
    contacts.add_record(record)
    return f"Contact {name} added with phone number {phone}."

@input_error
def change_contact(name, phone):
    if name in contacts.data:
        record = contacts.data[name]
        record.edit_phone(0, phone)
        return f"Phone number for {name} updated to {phone}."
    else:
        raise KeyError

@input_error
def get_phone(name):
    return f"The phone number for {name} is {contacts.data[name].phones[0]}."

def show_all_contacts():
    if contacts.data:
        return "\n".join([str(record) for record in contacts.data.values()])
    else:
        return "No contacts found."

def main():
    while True:
        user_input = input("Enter a command: ").lower().split(" ", 2)
        command = user_input[0]

        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            try:
                name = user_input[1]
                phone = user_input[2]
                record = Record(Name(name))
                record.add_phone(Phone(phone))
                if len(user_input) > 3:
                    birthday = user_input[3]
                    response = add_contact(name, phone, birthday)
                else:
                    response = add_contact(name, phone)
                print(response)
            except IndexError:
                print("Give me name and phone please.")
        elif command == "change":
            try:
                name = user_input[1]
                phone = user_input[2]
                response = change_contact(name, phone)
                print(response)
            except IndexError:
                print("Give me name and phone please.")
        elif command == "phone":
            try:
                name = user_input[1]
                response = get_phone(name)
                print(response)
            except IndexError:
                print("Enter user name.")
        elif command == "birthday":
            try:
                name = user_input[1]
                record = contacts.data[name]
                print(record.days_to_birthday())
            except KeyError:
                print("Contact not found.")
            except IndexError:
                print("Enter user name.")
        elif command == "show":
            if user_input[1] == "all":
                print(show_all_contacts())
        elif command in ["good", "bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()