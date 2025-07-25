from handlers import add_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, birthdays
from utils import parse_input
from models import AddressBook
from storage import save_data, load_data


def main():
    """Main loop for handling user commands."""
    
    book = load_data()
    print("Welcome to your assistant bot!")

    while True:
        user_input = input(">>> ")
        command, args = parse_input(user_input)

        if command in ("exit", "close"):
            print("Goodbye!")
            break
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        elif command == "hello":
            print("How can I help you?")
        else:
            print("Unknown command. Try again.")

    save_data(book)


if __name__ == "__main__":
    main()