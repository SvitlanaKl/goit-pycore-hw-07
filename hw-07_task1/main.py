from collections import UserDict
from datetime import datetime, timedelta

# Базовий клас Field
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        # валідація номеру  перевірка на 10 цифр
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.") 
        # Виклик ініціалізації базового класу
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(self.value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        phone_to_remove = next((number for number in self.phones if number.value == phone), None)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def find_phone(self, phone):
        return next((number for number in self.phones if number.value == phone), None)

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            self.phones.remove(phone_to_edit)
            self.add_phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
   
    def __str__(self):
        phones = '; '.join(number.value for number in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday set"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name, None)
    
    def delete(self, name):
        removed_record = self.data.pop(name, None)
        if removed_record is None:
            print(f"Record with name '{name}' not found.")
        else:
            print(f"Record with name '{name}' has been deleted.")

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthdate = record.birthday.value.date()
                # якщо в цьому році вже минув день народження, змінити в даті рік на наступний
                if birthdate < today:  
                    birthdate = birthdate.replace(year=today.year + 1)
                days_to_birthday = (birthdate - today).days
                # якщо день народження потрапляє на вихідні, перенести привітання на наступний тиждень
                if days_to_birthday <= 7:
                    if birthdate.weekday() == 5:
                        birthdate += timedelta(days=2)
                    elif birthdate.weekday() == 6:
                        birthdate += timedelta(days=1)
                    upcoming_birthdays.append({"name": record.name.value, "congratulation_date": birthdate.strftime("%Y.%m.%d")})

        return upcoming_birthdays

if __name__ == '__main__':
    
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    # Видалення запису Jane
    users = [
    {"name": "John Doe", "birthday": "1985.05.24"},
    {"name": "Jane Smith", "birthday": "1990.05.22"}
    ]
    
    upcoming_birthdays = book.get_upcoming_birthdays()
    print("Upcoming birthdays:")
    for birthday in upcoming_birthdays:
        print(birthday)