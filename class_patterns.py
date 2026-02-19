import json
from const_lists import *

class Character:
    """ Объект персонажа """
    def __init__(self, name, roles_and_ranks, element, element_code, weapon_type, special_codes, persons_pluses):
        self.name = name
        self.roles_and_ranks = roles_and_ranks
        self.element = element
        self.element_code = element_code
        self.weapon_type = weapon_type
        self.special_codes = special_codes
        self.persons_pluses = persons_pluses # Сюда просто вписывает плюсы персонажа, чтобы потом указать их в общих плюсах пачки

    def __repr__(self):
        return f"{self.name} - {self.element}({self.element_code})"


def make_character_classes(name):
    """ Из многочисленных consts_lists собирает под каждого персонажа цельный класс со всеми необходимыми данными """
    roles_and_ranks = {}
    for role, rang in zip(character_roles[name], character_rang[name]):
        roles_and_ranks[role] = rang
    return Character(name, roles_and_ranks, character_elements_name[name], character_elements[name], "weopone none", "-", "+")

def make_character_json():
    """ Эта функция собирает данные и записывает их в json файл """
    character_data_list = []

    for char_name in your_character_list:
        character_obj = make_character_classes(char_name)
        
        character_dict = {
            "name": character_obj.name,
            "roles_and_ranks": character_obj.roles_and_ranks,
            "element": character_obj.element,
            "element_code": character_obj.element_code,
            "weapon_type": character_obj.weapon_type,
            "special_codes": character_obj.special_codes,
            "persons_pluses": character_obj.persons_pluses
        }
        
        character_data_list.append(character_dict)
    
    with open("user_characters_data.json", "w", encoding="utf-8") as file:
        json.dump(character_data_list, file, indent=4, ensure_ascii=False)

make_character_json()