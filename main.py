from classes import AddressBook, Record, load_data, save_data
from datetime import datetime
from colorama import init, Fore

init()

def input_error(func):
    """Декоратор, який обробляє помилки введення для функцій."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Контакт не знайдено."
        except IndexError:
            return "Недійсна кількість аргументів для цієї команди."
    return inner

def parse_input(user_input):
    """Розбирає введену користувачем команду на команду та аргументи."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(user_input, book: AddressBook):
    """Додає новий контакт або оновлює існуючий."""
    args = user_input.split()[1:]
    if len(args) < 2:
        raise ValueError("Введіть ім'я та номер телефону, будь ласка.")
    name, phone = args[:2]
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Недійсний номер телефону. Введіть 10 цифр без роздільників.")
    record = book.find(name)
    message = "Контакт оновлено."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано."
    record.add_phone(phone)
    return message

@input_error
def change_contact(user_input, book: AddressBook):
    """Змінює номер телефону контакту."""
    args = user_input.split()[1:]
    if len(args) < 2:
        raise ValueError("Введіть ім'я та новий номер телефону.")
    name, new_phone = args[:2]
    if not new_phone.isdigit() or len(new_phone) != 10:
        raise ValueError("Недійсний номер телефону. Введіть 10 цифр без роздільників.")
    if book.find(name):
        book.find(name).add_phone(new_phone)
        return "Контакт оновлено."
    else:
        return "Контакт не знайдено."

@input_error
def phone(user_input, book: AddressBook):
    """Повертає номер телефону за ім'ям контакту."""
    name = user_input.split()[1]
    record = book.find(name)
    if record:
        return record  # Зміна тут
    else:
        return "Контакт не знайдено."

input_error
def all_contacts(user_input, book: AddressBook):
    """Повертає всі контакти."""
    if book.data:
        contacts_info = "\n".join(str(record) for record in book.data.values())
        return contacts_info
    else:
        return "Немає контактів у книзі."

@input_error
def add_birthday(user_input, book: AddressBook):
    """Додає день народження для контакту."""
    args = user_input.split()[1:]
    if len(args) < 2:
        raise ValueError("Введіть ім'я контакту та дату народження у форматі DD.MM.YYYY.")
    name, birthday = args[:2]
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"День народження додано для {name}."
    else:
        return "Контакт не знайдено."

@input_error
def show_birthday(user_input, book: AddressBook):
    """Показує день народження за ім'ям контакту."""
    name = user_input.split()[1]
    record = book.find(name)
    if record and record.birthday:
        return f"День народження {name}: {record.birthday}"
    else:
        return "День народження не знайдено."

@input_error
def birthdays(user_input, book: AddressBook):
    """Повертає всі наближені дні народження."""
    return book.get_upcoming_birthdays()

@input_error
def search_name(user_input, book: AddressBook):
    """Пошук контактів за частковим іменем."""
    partial_name = user_input.split()[1]
    matching_contacts = book.search_by_partial_name(partial_name)
    if matching_contacts:
        result = "\n".join(str(contact) for contact in matching_contacts)
        return result
    else:
        return "Контакти за вказаним ім'ям не знайдені."

@input_error
def sort_contacts(user_input, book: AddressBook):
    """Сортування контактів за різними полями."""
    field = user_input.split()[1].capitalize()
    try:
        sorted_contacts = book.sort_contacts(field)
        if sorted_contacts:
            result = "\n".join(str(contact) for contact in sorted_contacts)
            return result
        else:
            return "Немає контактів для сортування."
    except ValueError as e:
        return str(e)

@input_error
def add_group(user_input, book: AddressBook):
    """Додавання нової групи."""
    group_name = user_input.split()[1]
    book.add_group(group_name)
    return f"Групу '{group_name}' успішно додано."

@input_error
def remove_group(user_input, book: AddressBook):
    """Видалення існуючої групи."""
    group_name = user_input.split()[1]
    book.remove_group(group_name)
    return f"Групу '{group_name}' успішно видалено."

@input_error
def add_to_group(user_input, book: AddressBook):
    """Додавання контакту до групи."""
    group_name, contact_name = user_input.split()[1:]
    contact = book.find(contact_name)
    if contact:
        book.add_contact_to_group(contact, group_name)
        return f"Контакт '{contact_name}' успішно додано до групи '{group_name}'."
    else:
        return f"Контакт '{contact_name}' не знайдено."

@input_error
def remove_from_group(user_input, book: AddressBook):
    """Видалення контакту з групи."""
    group_name, contact_name = user_input.split()[1:]
    contact = book.find(contact_name)
    if contact:
        book.remove_contact_from_group(contact, group_name)
        return f"Контакт '{contact_name}' успішно видалено з групи '{group_name}'."
    else:
        return f"Контакт '{contact_name}' не знайдено."

def main():
    """Основна функція програми."""
    book = load_data()  # Відновлення даних

    print("Ласкаво просимо до помічника!")
    print(f"{Fore.BLUE}Список доступних команд: {Fore.RESET}\n"
    f"{Fore.GREEN}add{Fore.RESET}\n"
    f"{Fore.YELLOW}change{Fore.RESET}\n"
    f"{Fore.BLUE}phone{Fore.RESET}\n"
    f"{Fore.MAGENTA}all{Fore.RESET}\n"
    f"{Fore.CYAN}add-birthday{Fore.RESET}\n"
    f"{Fore.RED}show-birthday{Fore.RESET}\n"
    f"{Fore.GREEN}birthdays{Fore.RESET}\n"
    f"{Fore.YELLOW}sort{Fore.RESET}\n"
    f"{Fore.BLUE}add-group{Fore.RESET}\n"
    f"{Fore.MAGENTA}remove-group{Fore.RESET}\n"
    f"{Fore.CYAN}add-to-group{Fore.RESET}\n"
    f"{Fore.RED}remove-from-group{Fore.RESET}\n"
    f"{Fore.GREEN}hello{Fore.RESET}\n"
    f"{Fore.RED}notify-birthdays{Fore.RESET}\n"
    f"{Fore.YELLOW}search-name{Fore.RESET}"
    f"{Fore.YELLOW}close{Fore.RESET} або {Fore.YELLOW}exit{Fore.RESET}\n"
    
)
    while True:
        user_input = input("Введіть команду: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)  # Збереження даних перед виходом
            print("До побачення!")
            break

        elif command == "hello":
            print("Як я можу допомогти?")

        elif command == "add":
            result = add_contact(user_input, book)
            print(result)

        elif command == "change":
            result = change_contact(user_input, book)
            print(result)

        elif command == "phone":
            result = phone(user_input, book)
            print(result)

        elif command == "all":
            result = all_contacts(user_input, book)
            print(result)

        elif command == "add-birthday":
            result = add_birthday(user_input, book)
            print(result)

        elif command == "show-birthday":
            result = show_birthday(user_input, book)
            print(result)

        elif command == "birthdays":
            result = birthdays(user_input, book)
            print(result)

        elif command == "sort":
            field = input("Введіть поле для сортування (ім'я, телефон або дата народження): ")
            sorted_contacts = book.sort_contacts(field)
            if sorted_contacts:
                print("Відсортовані контакти:")
                for contact in sorted_contacts:
                    print(contact)
            else:
                print("Немає контактів для сортування.")

        elif command == "add-group":
            group_name = input("Введіть назву групи: ")
            book.add_group(group_name)

        elif command == "remove-group":
            group_name = input("Введіть назву групи, яку потрібно видалити: ")
            book.remove_group(group_name)

        elif command == "add-to-group":
            group_name, contact_name = args
            contact = book.data.get(contact_name)
            if contact:
                book.add_contact_to_group(contact, group_name)
            else:
                print("Контакт не знайдено.")

        elif command == "remove-from-group":
            group_name, contact_name = args
            contact = book.data.get(contact_name)
            if contact:
                book.remove_contact_from_group(contact, group_name)
            else:
                print("Контакт не знайдено.")

        elif command == "search-name":
            search_name = args[0]
            results = book.search_name(search_name)
            if results:
                print("Результати пошуку:")
                for contact in results:
                    print(contact)
            else:
                print("Контакти за вказаним ім'ям не знайдені.")

        elif command == "notify-birthdays":
            notifications = book.notify_birthdays()
            if notifications:
                print("Наближені дні народження:")
                for notification in notifications:
                    print(notification)
            else:
                print("Немає наближених днів народження.")

        else:
            print("Невірна команда.")

if __name__ == "__main__":
    main()