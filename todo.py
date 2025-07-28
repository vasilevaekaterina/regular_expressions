import csv
import re
from pprint import pprint


def read_contacts(file_name):
    """Чтение данных из CSV файла."""
    with open(file_name, encoding='utf-8') as f:
        rows = csv.reader(f)
        contacts_list = list(rows)
        return contacts_list


def format_phone(phone):
    """Форматирование номера телефона в стандартный вид."""
    phone = re.sub(r'\D', '', phone)  # Удаляем все символы кроме цифр
    if len(phone) == 11 and phone.startswith('8'):
        phone = '7' + phone[1:]  # Заменяем 8 на 7
    formatted_phone = f"+7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]}"

    # Проверка на добавочный номер
    if len(phone) > 11:
        ext_number = phone[11:]
        formatted_phone += f" доб.{ext_number}"

    return formatted_phone


def process_contacts(contacts_list):
    """Удаление дубликатов и форматирования данных."""
    contacts_dict = {}

    for contact in contacts_list:
        name = ' '.join(contact[:3]).split(' ')
        lastname = name[0]
        firstname = name[1]
        surname = name[2]
        full_name = (lastname, firstname)
        phone_formatted = format_phone(contact[5])

        if full_name in contacts_dict:
            existing_contact = contacts_dict[full_name]
            existing_contact[3] = existing_contact[3] or contact[3]
            existing_contact[4] = existing_contact[4] or contact[4]
            # обновляем телефон
            existing_contact[5] = existing_contact[5] or phone_formatted
            existing_contact[6] = existing_contact[6] or contact[6]
        else:
            contacts_dict[full_name] = [
                lastname,
                firstname,
                contact[2] or surname,
                contact[3],
                contact[4],
                phone_formatted,
                contact[6]
                ]

    return list(contacts_dict.values())


def save_contacts(file_name, contacts):
    """Сохранение обработанных контактов в новый файл."""
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(contacts)


def main():
    raw_contacts_file = 'phonebook_raw.csv'
    processed_contacts_file = 'phonebook.csv'

    contacts_list = read_contacts(raw_contacts_file)
    processed_contacts = process_contacts(contacts_list)
    save_contacts(processed_contacts_file, processed_contacts)

    pprint(processed_contacts)


if __name__ == "__main__":
    main()
