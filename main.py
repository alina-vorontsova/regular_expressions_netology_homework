import re 
import csv


def format_name(contacts_list):
    '''Разделяем имена на Ф+И+О.'''
    for person in contacts_list:
        if len(person[0].split()) == 3: # обработка сценария ФИО
            surname_splitted = person[0].split()
            person[0], person[1], person[2] = person[0].split()[0], surname_splitted[1], surname_splitted[2]
        if len(person[1].split()) == 2: # обработка сценария Ф+ИО
            name_splitted = person[1].split()
            person[1], person[2] = name_splitted[0], name_splitted[1]
        if len(person[0].split()) == 2: # обработка сценария ФИ
            surname_splitted = person[0].split()
            person[0], person[1] = person[0].split()[0], surname_splitted[1]
    
    return contacts_list

def format_phone_numbers(contacts_list):
    '''Приводим номера телефонов к единому формату.'''
    pattern = r"(\+7|8)?\s?\(?(\d{3}?)\)?[-\s]?(\d{3})[-\s]?(\d{2})-?(\d{2})(\s?)\(?([доб.]{4})?\s?(\d{4})?\)?"
    substitution = r"+7(\2)\3-\4-\5\6\7\8"
    for person in contacts_list:
        person[5] = re.sub(pattern, substitution, person[5])
    
    return contacts_list

def delete_dubles(contacts_list):
    '''Объединяем дублирующиеся записи о человеке.'''
    for person in contacts_list:
        for another_person in contacts_list:
            if person[0] in another_person[0]:
                for i in range(7):
                    if person[i] == '': 
                        person[i] = another_person[i]

    formatted_contacts_list = []
    for person in contacts_list: 
        if len(person) != 7: # Избавляемся от персонажа, длина списка которого отличается от длины списков других людей (у всех 7, а у него 8)
            del person[7:]
        if person not in formatted_contacts_list:
            formatted_contacts_list.append(person)

    return formatted_contacts_list


if __name__ == "__main__":

    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    format_name(contacts_list)
    format_phone_numbers(contacts_list)
    formatted_contacts_list = delete_dubles(contacts_list)

    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(formatted_contacts_list)