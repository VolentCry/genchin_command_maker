"""
Файл со всеми вспомогательными функциями для работы алгоритма, а также здесь вынесены большие цепочки из основной программы, которые дуплируются в разных частях кода
"""
from const_lists import character_elements

def electro_and_gydor_subdd_or_support(Max_SD: int, subdamaggers_list: list, supports_list: list) -> list:
    """
    """
    new_command_members = [] # Персонажи добавляются обязательно в порядке сначало гидро, потом электро
    elements_of_new_command_members = []
    SD, S = 0, 0

    if Max_SD == 2:
        # Поиск подходящего гидро СабДД и электро СабДД, а после единственный слот саппорта заполнится лучшим из имеющихся саппортов
        gydro_subdamagger = None; electro_subdamagger = None
        for name in subdamaggers_list:
            if character_elements[name] == "G" and gydro_subdamagger == None:
                gydro_subdamagger = name; SD += 1
            elif character_elements[name] == "E" and electro_subdamagger == None:
                electro_subdamagger = name; SD += 1
        
        # Не нашлось ни гидро, ни электро СабДД, поэтому ищем саппортов этой стихии
        if gydro_subdamagger == None and electro_subdamagger == None:
            electro_suport = None; gydro_suport = None
            for name in supports_list:
                if character_elements[name] == "G" and gydro_suport == None:
                    gydro_suport = name; S += 1
                elif character_elements[name] == "E" and electro_suport == None:
                    electro_suport = name; S += 1

        # Не нашлось гидро СабДД, поэтому ищем саппорта этой стихии
        elif gydro_subdamagger == None:
            gydro_suport = None
            for name in supports_list:
                if character_elements[name] == "G" and gydro_suport == None:
                    gydro_suport = name; S += 1

        # Не нашлось электро СабДД, поэтому ищем саппорта этой стихии
        elif electro_subdamagger == None:
            electro_suport = None
            for name in supports_list:
                if character_elements[name] == "E" and electro_suport == None:
                    electro_suport = name; S += 1

        # Финальная проверка и вывод результатов
        if gydro_subdamagger and electro_subdamagger:
            new_command_members = [gydro_subdamagger, electro_subdamagger]
            return SD, S, new_command_members, elements_of_new_command_members
        elif gydro_subdamagger and (electro_subdamagger == None and electro_suport):
            new_command_members = [gydro_subdamagger, electro_suport]
            return SD, S, new_command_members, elements_of_new_command_members
        elif electro_subdamagger and (gydro_subdamagger == None and gydro_suport):
            new_command_members = [gydro_suport, electro_subdamagger]
            return SD, S, new_command_members, elements_of_new_command_members
        elif (electro_subdamagger == None and electro_suport) and (gydro_subdamagger == None and gydro_suport):
            new_command_members = [gydro_suport, electro_suport]
            return SD, S, new_command_members, elements_of_new_command_members
        elif (electro_subdamagger == None and electro_suport == None) and (gydro_subdamagger == None and gydro_suport):
            new_command_members = [gydro_suport]
            elements_of_new_command_members = ["E"]
            return SD, S, new_command_members, elements_of_new_command_members
        elif (electro_subdamagger == None and electro_suport) and (gydro_subdamagger == None and gydro_suport == None):
            new_command_members = [electro_suport]
            elements_of_new_command_members = ["E"]
            return SD, S, new_command_members, elements_of_new_command_members
        elif (electro_subdamagger == None and electro_suport == None) and (gydro_subdamagger == None and gydro_suport == None):
            return SD, S, new_command_members, elements_of_new_command_members

    # Поиск подходящего гидро СабДД и электро саппорта, а после последний слот саппорта заполнится лучшим из имеющихся саппортов
    elif Max_SD == 1:
        gydro_subdamagger = None; electro_suport = None
        for name in subdamaggers_list:
            if character_elements[name] == "G" and gydro_subdamagger == None:
                gydro_subdamagger = name; SD += 1
        for name in supports_list:
            if character_elements[name] == "E" and electro_suport == None:
                electro_suport = name; S += 1

        # Не удалось найти ни гидро СабДД, ни электро саппорта, поэтому ищем электро СабДД и гидро саппорта
        if gydro_subdamagger == None and electro_suport == None:
            electro_subdamagger = None; gydro_suport = None
            for name in subdamaggers_list:
                if character_elements[name] == "E" and electro_subdamagger == None:
                    electro_subdamagger = name; SD += 1
                elif electro_subdamagger: break
            for name in supports_list:
                if character_elements[name] == "G" and gydro_suport == None:
                    gydro_suport = name; S += 1
                elif gydro_suport: break
    
        # Не удалось найти гидро сабДД, поэтому ищем электро СабДД
        elif gydro_subdamagger == None:
            electro_subdamagger = None
            for name in subdamaggers_list:
                if character_elements[name] == "E" and electro_subdamagger == None:
                    electro_subdamagger = name; SD += 1
                elif electro_subdamagger: break

        # Не удалось найти электро саппорта, поэтому ищем гидро саппорта
        elif electro_suport == None:
            gydro_suport = None
            for name in supports_list:
                if character_elements[name] == "G" and gydro_suport == None:
                    gydro_suport = name; S += 1
                elif gydro_suport: break

        if gydro_subdamagger and electro_suport:
            new_command_members = [gydro_subdamagger, electro_suport]
            elements_of_new_command_members = ["G", "E"]
            return SD, S, new_command_members, elements_of_new_command_members
        elif gydro_subdamagger and (electro_suport == None and gydro_suport):
            new_command_members = [gydro_subdamagger, gydro_suport]
            elements_of_new_command_members = ["G", "G"]
            return SD, S, new_command_members, elements_of_new_command_members
        elif (gydro_subdamagger == None and electro_subdamagger) and electro_suport:
            new_command_members = [electro_subdamagger, electro_suport]
            elements_of_new_command_members = ["E", "E"]
            return SD, S, new_command_members, elements_of_new_command_members
        

def element_characters_counter(your_characters: list) -> dict:
    """Это счётчик количество элементов у вас, то есть сколько персонажей каждого элемента есть у вас в наличии, не считая ГГ"""
    element_counts = {
    "P": 0,
    "K": 0,
    "G": 0,
    "A": 0,
    "Ge": 0,
    "E": 0,
    "D": 0
    }

    for char in your_characters:
        element_counts[character_elements[char]] += 1

    return element_counts
