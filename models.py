from collections import UserDict
from datetime import datetime, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name is required")
        super().__init__(value)

    def __str__(self):
        return f"Name: {self.value}"

class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must be a 10-digit number")
        super().__init__(value)

    def __str__(self):
        return f"Phone: {self.value}"
    
class Birthday(Field):
    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Birthday must be a string in format DD.MM.YYYY")
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(parsed_date)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Check if phone is an object of Phone class or a string and return string
    def _get_phone_value(self, phone):
        return phone.value if isinstance(phone, Phone) else phone

    def add_phone(self, phone):
        phone_value = self._get_phone_value(phone)

        for p in self.phones:
            if p.value == phone_value:
                raise ValueError(f"Phone {phone_value} already exists for this contact.")

        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_value = self._get_phone_value(phone)

        for p in self.phones:
            if p.value == phone_value:
                print(f"Phone {phone_value} removed from contact {self.name.value}")
                self.phones.remove(p)
                return

        raise ValueError(f"Phone {phone_value} not found in record") 
    
    def edit_phone(self, old_phone, new_phone):
        old_phone_value = self._get_phone_value(old_phone)
        new_phone_value = self._get_phone_value(new_phone)

        if old_phone_value == new_phone_value:
            raise ValueError("New phone number must be different from the old one")  

        for i, p in enumerate(self.phones):
            if p.value == old_phone_value:
                print(f"Phone {old_phone_value} changed to {new_phone_value} in contact {self.name.value}") 
                self.phones[i] = Phone(new_phone_value)
                return

        raise ValueError(f"Phone {old_phone_value} not found in record")
    
    def find_phone(self, phone):
        phone_value = self._get_phone_value(phone)

        for p in self.phones:
            if p.value == phone_value:
                print(f"Phone found: {p.value}")
                return p

        raise ValueError(f"Phone {phone_value} not found in record")
    
    def add_birthday(self, birthday):
        birthday_value = birthday.value if isinstance(birthday, Birthday) else birthday

        if self.birthday is not None and self.birthday.value == birthday_value:
            raise ValueError(f"Birthday already exists for this contact.")

        self.birthday = Birthday(birthday_value)
        print(f"Birthday {birthday_value} added to contact {self.name.value}")

class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise ValueError(f"Record with name {name} not found")

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
            print(f"Record for '{name}' deleted from address book.") 
        else:
            raise ValueError(f"Record with name {name} not found")
        
    def get_upcoming_birthdays(self):
        today = datetime.now().date()

        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday = record.birthday.value

            # Set birthday to this year
            birthday_this_year = birthday.replace(year=today.year)

            # If birthday has already passed this year, set it to next year
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            # Calculate the difference in days
            days_until_birthday = (birthday_this_year - today).days

            # Check if the birthday is within the next 7 days
            if 0 <= days_until_birthday <= 7:
                congratulation_date = birthday_this_year

                # Check if the congratulation date falls on a weekend
                if congratulation_date.weekday() >= 5:

                    # If it's Saturday (5) or Sunday (6), move to the next Monday
                    congratulation_date += timedelta(days=(7 - congratulation_date.weekday()))

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })            

        upcoming_birthdays.sort(key=lambda x: x["congratulation_date"])
        
        return upcoming_birthdays    
    
    def save_data(book, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(book, f)

    def load_data(filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()