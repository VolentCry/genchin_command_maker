"""
Docstring for start
"""
from const_lists import *
import random

your_character_list = ["Качина", "Сетос", "Ка Мин", "Шеврёз", "Шарлотта", "Нёвиллет", "Фремине",
                       "Линетт", "Кирара", "Кавех", "Мика", "Яо Яо", "Фарузан", "Лайла", "Кандакия",
                       "Тигнари", "Коллеи", "Хэйдзо", "Синобу", "Юнь Цзинь", "Горо", "Тома",
                       "Сара", "Саю", "Аяка", "Кадзуха", "Янь Фэй", "Розария", "Сяо", "Гань Юй", 
                       "Синь Янь", "Тарталья", "Диона", "Кли", "Мона", "Ци Ци", "Дилюк", "Джинн",
                       "Сахароза", "Чун Юнь", "Ноэлль", "Беннет", "Фишль", "Нин Гуан", "Син Цю",
                       "Бэй Доу", "Сян Лин", "Рэйзор", "Барбара", "Лиза", "Кэйа", "Эмбер"]


pattern_1 = "D.SD.S.S"

damaggers_list = []
subdamaggers_list = []
supports_list = []
                

def get_rank_for_role(character: str, role: str) -> int:
    """
    Возвращает числовой ранг персонажа для конкретной роли
    0 - S+, 1 - S, 2 - A, 3 - B, 4 - C, 5 - D
    Если персонаж не имеет указанной роли, возвращает 6 (худший ранг)
    """
    # Словарь для преобразования ранга в число
    rangs = {"S+": 0, "S": 1, "A": 2, "B": 3, "C": 4, "D": 5}
    
    # Получаем роли персонажа
    char_roles = character_roles[character]
    char_rangs = character_rang[character]
    
    # Если у персонажа одна роль
    if isinstance(char_roles, str):
        if char_roles == role:
            # Если ранг - строка
            if isinstance(char_rangs, str):
                return rangs[char_rangs]
            # Если ранг - список (должно быть одно значение)
            else:
                return rangs[char_rangs[0]]
        else:
            # Персонаж не имеет этой роли
            return 6
    
    # Если у персонажа несколько ролей
    else:
        # Ищем индекс нужной роли
        try:
            role_index = char_roles.index(role)
        except ValueError:
            # Персонаж не имеет этой роли
            return 6
        
        # Получаем ранг для этой роли
        if isinstance(char_rangs, list):
            rank_str = char_rangs[role_index]
        else:
            # Если ранг - строка, но ролей несколько (не должно быть, но на всякий случай)
            rank_str = char_rangs
        
        return rangs[rank_str]

def progressive_sort(character_list: list, role: str) -> list:
    """
    Сортирует список персонажей по рангу для указанной роли
    Сначала идут персонажи с лучшим рангом (S+), затем с худшим (D)
    """
    # Сортируем по рангу для указанной роли, а при одинаковом ранге - по имени
    return sorted(character_list, key=lambda char: (get_rank_for_role(char, role), char))

# Формируем списки персонажей по ролям
for i in your_character_list:
    role = character_roles[i]
    if type(role) == str:  # Одна роль
        if role == "D":
            damaggers_list.append(i)
        elif role == "SD":
            subdamaggers_list.append(i)
        else:
            supports_list.append(i)
    else:  # Две или более роли
        for j in role:
            if j == "D":
                damaggers_list.append(i)
            elif j == "SD":
                subdamaggers_list.append(i)
            else:
                supports_list.append(i)

# Убираем дубликаты (если персонаж имеет несколько ролей)
damaggers_list = list(set(damaggers_list))
subdamaggers_list = list(set(subdamaggers_list))
supports_list = list(set(supports_list))

# СОРТИРУЕМ списки по рангу для каждой роли
damaggers_list = progressive_sort(damaggers_list, "D")
subdamaggers_list = progressive_sort(subdamaggers_list, "SD")
supports_list = progressive_sort(supports_list, "S")

def make_command(mode: int, pattern: str):
    """
    """
    command = []

    if mode == 0:
        for position in pattern.split("."):
            if position == "D":
                command.append(random.choice(damaggers_list))
            elif position == "SD":
                command.append(random.choice(subdamaggers_list))
            else:
                command.append(random.choice(supports_list))
    elif mode == 1:
        D = 0; SD = 0; S = 0
        for position in pattern.split("."):
            if position == "D":
                command.append(damaggers_list[D:][0]); D += 1
            elif position == "SD":
                command.append(subdamaggers_list[SD:][0]); SD += 1
            else:
                command.append(supports_list[S:][0]); S += 1
    else:
        raise ValueError("Неверное значение режима")

    
    return command

print("Выберите мод генерации команды (0 - случайный, 1 - лучший из лучших):  ")
make_mode = int(input())


print(make_command(make_mode, pattern_1))