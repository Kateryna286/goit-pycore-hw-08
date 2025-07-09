from utils import input_error
from models import AddressBook, Record, Birthday

book = AddressBook()

@input_error
def add_contact(args, book: AddressBook):
    """Adds a new contact or updates existing one with a phone number."""
    
    if len(args) < 2:
        raise ValueError()
    
    name, phone, *_ = args

    if not name.isalpha():
        return "Name must contain only letters."
    if not phone.isdigit():
        return "Phone number must contain only digits."
    
    try:
        record = book.find(name)
        record.add_phone(phone)
        return f"Phone {phone} added to existing contact {name.capitalize()}."
    except ValueError as e:
        if "not found" in str(e):
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            return f"Contact {name.capitalize()} added with phone {phone}."
        else:
            return str(e)

@input_error
def change_contact(args, book: AddressBook):
    """Changes an existing contact's phone number."""
    
    if len(args) != 3:
        raise ValueError("You must provide a name, old phone, and new phone.")
    
    name, old_phone, new_phone = args

    if not name.isalpha():
        return "Name must contain only letters."
    if not old_phone.isdigit() or not new_phone.isdigit():
        return "Phone number must contain only digits."
    
    record = book.find(name)

    if not record.phones:
        raise ValueError(f"No phones found for {name.capitalize()} to change.")
    
    record.edit_phone(old_phone, new_phone)
    return f"Phone number for {name.capitalize()} changed from {old_phone} to {new_phone}."
 
@input_error
def show_phone(args, book: AddressBook):
    """Shows the phone number for a given contact."""
    
    if len(args) != 1:
        raise IndexError()
    
    name = args[0]

    if not name.isalpha():
        return "Name must contain only letters."
    
    record = book.find(name)
    
    if not record.phones:
        return f"No phone numbers found for {name.capitalize()}."

    phones_str = ", ".join(p.value for p in record.phones)
    return f"Phone(s) for {name.capitalize()}: {phones_str}"

def show_all(book: AddressBook):
    """Shows all stored contacts."""
    if not book.data:
        return "No contacts saved yet."
    
    result = []
    for record in book.data.values():
        phones = ", ".join(p.value for p in record.phones) if record.phones else "N/A"
        birthday = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "N/A"
        
        contact_info = (f"{{name: {record.name.value}, phones: {phones}, birthday: {birthday}}}")
        result.append(contact_info)    
    return "\n".join(result)

@input_error
def add_birthday(args, book):
    """Adds a birthday for a given contact."""

    if len(args) < 2:
        raise ValueError("Please provide a name and a birthday in the format DD.MM.YYYY.")
    name, birthday_str = args[0], args[1]

    if not name.isalpha():
        return "Name must contain only letters."
    
    birthday = Birthday(birthday_str)

    try:
        record = book.find(name)
    except ValueError:
        record = Record(name)
        book.add_record(record)

    record.birthday = birthday

    return f"Birthday {birthday.value.strftime('%d.%m.%Y')} added for contact {name.capitalize()}."

@input_error
def show_birthday(args, book: AddressBook):
    """Shows the birthday for a given contact."""

    if len(args) != 1:
       raise IndexError()
   
    name = args[0]
   
    if not name.isalpha():
        return "Name must contain only letters."

    record = book.find(name)
    
    if not record.birthday:
        return f"No birthday found for {name.capitalize()}."  

    birthday_str = record.birthday.value.strftime("%d.%m.%Y")
    return f"Birthday for {name.capitalize()}: {birthday_str}."  

@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays found."
    
    return upcoming