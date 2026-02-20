import json
from const_lists import *

class Character:
    """ Объект персонажа """
    def __init__(self, name, roles_and_ranks, element, element_code, weapon_type, special_codes, persons_pluses, fraction):
        self.name = name
        self.roles_and_ranks = roles_and_ranks
        self.element = element
        self.element_code = element_code
        self.weapon_type = weapon_type
        self.special_codes = special_codes
        self.persons_pluses = persons_pluses # Сюда просто вписывает плюсы персонажа, чтобы потом указать их в общих плюсах пачки
        self.fraction = fraction

    def __repr__(self):
        return f"{self.name} - {self.element}({self.element_code})"



