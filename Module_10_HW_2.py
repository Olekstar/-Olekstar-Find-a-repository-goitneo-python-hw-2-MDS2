class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name}, phones: {', '.join(map(str, self.phones))}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command format."

    return inner

@input_error
def add_contact(args, address_book):
    if len(args) == 2:
        name, phone = args
        record = Record(name)
        record.add_phone(phone)
        address_book.add_record(record)
        return "Contact added."
    else:
        raise ValueError("Give me name and phone please.")

@input_error
def list_contacts(address_book):
    if not address_book.data:
        return "Contacts not found."
    else:
        return "\n".join(str(record) for record in address_book.data.values())

@input_error
def save_contacts(address_book, filename="contacts.txt"):
    with open(filename, "w") as file:
        for record in address_book.data.values():
            file.write(f"{record.name.value}:{';'.join(map(str, record.phones))}\n")

@input_error
def change_contact(args, address_book):
    if len(args) == 2:
        name, new_phone = args
        record = address_book.find(name)
        if record:
            record.edit_phone(record.phones[0].value, new_phone)
            return f"Phone number for {name} changed to {new_phone}."
        else:
            raise KeyError
    else:
        raise ValueError("Give me name and new phone please.")

@input_error
def load_contacts(address_book, filename="contacts.txt"):
    try:
        with open(filename, "r") as file:
            for line in file:
                name, phones_str = line.strip().split(":")
                phones = phones_str.split(";")
                record = Record(name)
                for phone in phones:
                    record.add_phone(phone)
                address_book.add_record(record)
    except FileNotFoundError:
        pass

def find_contact(args, address_book):
    if len(args) == 1:
        name = args[0]
        record = address_book.find(name)
        if record:
            return f"Phone number(s) for {name}: {', '.join(map(str, record.phones))}."
        else:
            return f"Contact '{name}' not found."
    else:
        raise ValueError("Give me a name to find.")
    
@input_error
def delete_contact(args, address_book):
    if len(args) == 1:
        name = args[0]
        address_book.delete(name)
        return f"Contact {name} deleted."
    else:
        raise ValueError("Give me a name to delete.")

def main():
    address_book = AddressBook()
    load_contacts(address_book)
    print('=' * 30 + '\nMain commands:\n'
                     'hello - greeting message\n'
                     'add - add new contact\\contact number\n'
                     'change - change contact number\n'
                     'find - number search by name\n'
                     'del - delete contact\\number\n'
                     'all - show all contacts\n' + '=' * 30)

    while True:
        user_input = input("Enter command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_contacts(address_book)
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "all":
            print(list_contacts(address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "find":
            print(find_contact(args, address_book))
        elif command == "del":
            print(delete_contact(args, address_book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()   
