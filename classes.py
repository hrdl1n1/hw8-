import pickle
from datetime import datetime, timedelta, date
from collections import UserDict

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self._validate_phone(value):
            raise ValueError("Номер телефону має містити 10 цифр")
        super().__init__(value)

    def _validate_phone(self, value):
        return isinstance(value, str) and len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not self._validate_date(new_value):
            raise ValueError("Невірний формат дати. Використовуйте ДД.ММ.РРРР")
        self._value = new_value

    def _validate_date(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    def get_date_object(self):
        return datetime.strptime(self._value, "%d.%m.%Y").date()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.change_history = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if not self.find_phone(old_phone):
            raise ValueError("Номер телефону для редагування не існує")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        if self.birthday:
            raise ValueError("Дата народження вже існує для цього контакту")
        self.birthday = Birthday(birthday)

    def add_change(self, change_description):
        self.change_history.append((datetime.now(), change_description))

    def show_change_history(self):
        if self.change_history:
            for change_time, change_description in self.change_history:
                print(f"{change_time}: {change_description}")
        else:
            print("Історія змін порожня.")

    def revert_to_previous_state(self):
        if len(self.change_history) > 1:
            self.change_history.pop()
            _, previous_state_description = self.change_history[-1]
            return previous_state_description
        else:
            return "Немає попередніх станів для відновлення."

    def __str__(self):
        phones = ', '.join(str(phone) for phone in self.phones)
        birthday = str(self.birthday) if self.birthday else "Немає інформації про день народження"
        return f"Ім'я: {self.name}, Телефони: {phones}, День народження: {birthday}"

class Group:
    def __init__(self, name):
        self.name = name
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def remove_contact(self, contact):
        if contact in self.contacts:
            self.contacts.remove(contact)

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.groups = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_bdays = []

        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.get_date_object()
                bday_this_year = bday.replace(year=today.year)

                if bday_this_year < today:
                    bday = bday.replace(year=today.year + 1)
                else:
                    bday = bday_this_year

                days_until_bday = (bday - today).days

                if 0 <= days_until_bday <= 7:
                    if bday.weekday() >= 5:
                        days_until_monday = (7 - bday.weekday())
                        bday += timedelta(days_until_monday)

                    upcoming_bdays.append({
                        "name": record.name.value,
                        "congratulation_date": bday.strftime("%Y.%m.%d")
                    })

        return upcoming_bdays
    def search_by_partial_name(self, partial_name):
        matching_contacts = [record for record in self.data.values() if partial_name in record.name.value]
        return matching_contacts

    def check_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()
        for record in self.data.values():
            if record.birthday:
                bday_this_year = record.birthday.get_date_object().replace(year=today.year)
                if bday_this_year >= today:
                    days_until_bday = (bday_this_year - today).days
                    if 0 < days_until_bday <= 7:
                        upcoming_birthdays.append((record.name.value, record.birthday.value))
        return upcoming_birthdays

    def sort_contacts(self, field):
        if field == "Name":
            return sorted(self.data.values(), key=lambda x: x.name.value)
        elif field == "Phone":
            return sorted(self.data.values(), key=lambda x: x.phones[0].value if x.phones else '')
        elif field == "Birthday":
            return sorted(self.data.values(), key=lambda x: x.birthday.value if x.birthday else '')
        else:
            raise ValueError("Непідтримуване поле для сортування.")

    def add_group(self, group_name):
        if group_name not in self.groups:
            self.groups[group_name] = Group(group_name)
        else:
            print("Група з такою назвою вже існує.")

    def remove_group(self, group_name):
        if group_name in self.groups:
            del self.groups[group_name]
        else:
            print("Група з такою назвою не існує.")

    def add_contact_to_group(self, contact, group_name):
        if group_name in self.groups:
            self.groups[group_name].add_contact(contact)
        else:
            print("Група з такою назвою не існує.")

    def remove_contact_from_group(self, contact, group_name):
        if group_name in self.groups:
            self.groups[group_name].remove_contact(contact)
        else:
            print("Група з такою назвою не існує.")

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
