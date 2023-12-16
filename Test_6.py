from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        while not isinstance(value, str) or not value.isdigit() or len(value) != 10:
            print("Invalid phone number format. Please enter a 10-digit phone number.")
            value = input("Enter the contact number: ")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name}, phones: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

# Створення нової адресної книги
book = AddressBook()

def load_contacts(address_book):
    # Функція завантаження контактів може бути реалізована за необхідністю
    pass

def main():
    address_book = AddressBook()
    load_contacts(address_book)
    print('=' * 30 + '\nMain commands:\n'
                     'hello - greeting message\n'
                     'add - add new contact\\contact number\n'
                     'find - number search by name\n'
                     'change - change contact number\n'
                     'del - delete contact\\number\n'
                     'all - show all contacts\n'
                     'exit - finish work\n' + '=' * 30)

    while True:
        command = input("Enter a command: ").lower()

        if command == 'hello':
            print("Hello! I am your address book assistant. Enter a command you want to perform.")
        elif command == 'add':
            name = input("Enter the contact name: ")
            phone = input("Enter the contact number: ")
            record = address_book.find(name)
            if not record:
                record = Record(name)
                address_book.add_record(record)
            record.add_phone(phone)
            print(f"Contact {name} added successfully.")
        elif command == 'change':
            name = input("Enter the contact name: ")
            record = address_book.find(name)
            if record:
                print(f"Current contact numbers: {', '.join(str(p) for p in record.phones)}")
                old_phone = input("Enter the contact number to change: ")
                new_phone = input("Enter the new contact number: ")
                record.edit_phone(old_phone, new_phone)
                print(f"Contact number for {name} changed successfully.")
            else:
                print(f"Contact {name} not found.")
        elif command == 'find':
            name = input("Enter the contact name: ")
            record = address_book.find(name)
            if record:
                print(f"Contact {name} numbers: {', '.join(str(p) for p in record.phones)}")
            else:
                print(f"Contact {name} not found.")
        elif command == 'del':
            name = input("Enter the contact name: ")
            delete = address_book.delete(name)
            if delete:
                print(f"Contact {name} deleted successfully.")
            else:
                print(f"Contact {name} not found.")
        elif command == 'all':
            if not address_book.data:
                print("Address book is empty.")
            else:
                for name, record in address_book.data.items():
                    print(record)
        elif command == 'exit':
            print("Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
