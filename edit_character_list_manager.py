"""
Здесь расположены вспомогательные функции для быстрого обновления актуального
спсика персонажей
"""

import json
from const_lists import element_codes

with open("all_characters_data.json", 'r', encoding='utf-8') as file:
    raw_data = json.load(file)


def found_person(target_name: str) -> bool:
    """
    Провека на наличие персонажа в списке всех персонажей
    """
    for i in range(len(raw_data)):
        if raw_data[i]['name'] == target_name:
            return True
    return False


def add_new_person():
    """
    """

    target_name = input("Введите имя персонажа: ").capitalize()

    if found_person(target_name):
        raise ValueError("Такой персонаж уже есть в спсике")

    raruity = int(input("Введите редкость персонажа: "))
    element = input("Введите элемент персонажа(словом, на русском, "
                    "с большой буквы): ").capitalize()
    weapon_type = input("Введите тип оружия персонажа(словом, на русском, "
                        "с большой буквы): ").capitalize()
    fraction = input("Введите название фракции персонажа (Допустимые варианты:"
                     " Нод-Край, Шабаш): ").capitalize()
    rols_cnt = int(input("Сколько ролей у персонажа: "))

    # Словарь с ролями персонажа в формате "роль":"оценка"
    roles = {}

    for i in range(rols_cnt):
        role_type = input(f"Роль {i+1}. Введите тип роли (D, SD, S): ")

        while role_type not in ["D", "SD", "S"]:
            print("Такой роли нет в списке.")
            role_type = input(f"Роль {i+1}. Введите тип роли (D, SD, S): ")

        role_grade = input(f"Роль {i+1}. Ввепдите оценку роли (D-S+): ")

        while role_grade not in ["S+", "S", "A", "B", "C", "D"]:
            print("Такой оценки не существует.")
            role_grade = input(f"Роль {i+1}. Ввепдите оценку роли (D-S+): ")

        roles[role_type] = role_grade

    new_person = {
        'name': target_name,
        "roles_and_ranks": roles,
        "rarity": raruity,
        "element": element,
        "element_code": element_codes[element],
        "weapon_type": weapon_type,
        "special_codes": "-",
        "persons_pluses": "+",
        "fraction": fraction
    }

    for i in range(len(raw_data)-1):
        if raw_data[i]['name'] < target_name < raw_data[i+1]['name']:
            print(f"Новая последовательность: {raw_data[i]['name']}"
                  f"{target_name} {raw_data[i+1]['name']}")
            raw_data.insert(i + 1, new_person)
            break  # Прерывает цикл после успешной вставки

    print("\nВот итоговый вариант. Пожалуйста проверьте всё очень внимательно")
    print(new_person)
    answer = input("\nПодтверждаете запись? (yes/no):\t")

    if answer in "yes":
        with open("all_characters_data.json", "w", encoding="utf-8") as file:
            json.dump(raw_data, file, indent=4, ensure_ascii=False)
    else:
        return


add_new_person()
