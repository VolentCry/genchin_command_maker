from const_lists import *
from helpful_funcs import *
import random

# Допустимые паттерны создания команд 
pattern_1 = "D.SD.S.S"
pattern_1 = "D.SD.SD.S"


# Желаемая стихия даммагера
desired_element = "-"

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
    return sorted(character_list, key = lambda char: (get_rank_for_role(char["name"], role), char["name"]))


damaggers_list, subdamaggers_list, supports_list = read_characters_from_json("user_characters_data.json")


# СОРТИРУЕМ списки по рангу для каждой роли
damaggers_list = progressive_sort(damaggers_list, "D")
subdamaggers_list = progressive_sort(subdamaggers_list, "SD")
supports_list = progressive_sort(supports_list, "S")



def make_command(mode: int, pattern: str) -> list:
    """
    Это основная функция, которая создаёт для вас граммотную команду персонажей на основе ваших запросов
    В ней подразумеваются такие режимы: 
    • 0 - случайный подбор команды
    • 1 - сборка пачки из самых лучших персонажей вашего аккаунта
    • 2 - сборка пачки посредством сложных алгоритмов для достижения лучшего результата
    • 3 - сборка моноэлементальной пачик 
    """
    command, command_elements = [], []
    Max_D = pattern.split(".").count("D"); Max_SD = pattern.split(".").count("SD"); Max_S = pattern.split(".").count("S")
    D = 0; SD = 0; S = 0

    if len(your_character_list) < 4: 
        raise ValueError("Невозможно составить команду, у вас меньше 4-ёх персонажей")


    # --------------------- 0. Режим рандомизации --------------------- 
    if mode == 0:
        for position in pattern.split("."):
            if position == "D":
                command.append(random.choice(damaggers_list))
            elif position == "SD":
                command.append(random.choice(subdamaggers_list))
            else:
                command.append(random.choice(supports_list))


    # --------------------- 1. Подборка лучший из лучших --------------------- 
    elif mode == 1:
        for position in pattern.split("."):
            # Поиск дамаггера
            if position == "D" and D < Max_D:
                command.append(damaggers_list[D:][0]); D += 1
            # Поиск сабдамаггера
            elif position == "SD" and SD < Max_SD:
                command.append(subdamaggers_list[SD:][0]); SD += 1
            # Поиск саппорта
            elif position == "S" and S < Max_S:
                command.append(supports_list[S:][0]); S += 1


    # --------------------- 2. Класисческий режим генерации --------------------- 
    elif mode == 2:
        for position in pattern.split("."):
            # Поиск дамаггера

            if desired_element == "-":
                if position == "D" and D < Max_D:
                    damagger = damaggers_list[D:][0]
                    command.append(damagger); D += 1

                    # Дамаггер пиро
                    if character_elements[damagger] == "P": 
                        gydro_or_kryo_subdd = None
                        for char in subdamaggers_list: # Ищем СабДД Крио или Гидро
                            if character_elements[char] == "G" or character_elements[char] == "K":
                                gydro_or_kryo_subdd = char
                                break
                        if gydro_or_kryo_subdd != None: command.append(gydro_or_kryo_subdd); SD += 1

                    # Дамаггер крио/гидро
                    elif character_elements[damagger] == "G" or character_elements[damagger] == "K":
                        pyro_subdd = None
                        for char in subdamaggers_list: # Ищем СабДД Пиро
                            if character_elements[char] == "P":
                                pyro_subdd = char
                                break
                        if pyro_subdd != None: command.append(pyro_subdd); SD += 1

                    # Дамаггер гео
                    elif character_elements[damagger] == "Ge":
                        # Сборка Гео даммагера непосредственно в его урон

                        # Сначала проверка на Цзы Бай
                        if character_fraction[damagger] == "Нод-Край":
                            # Это Цзы Бай
                            required_geo_nord_karai_person = False
                            required_gidro_nord_karai_person = False
                            suitable_characters = [] # Подходящие под Цзы Бай персонажи
                            for char in your_character_list:
                                if char != damagger and character_fraction[char] == "Нод-Край" and (character_elements[char] == "Ge" or character_elements[char] == "G"):
                                    suitable_characters.append(char)
                            if len(suitable_characters) != 0:
                                for char in suitable_characters:
                                    if "Коломбина" in suitable_characters: # Проверка, есть ли Коломбина
                                        command.append("Коломбина")
                                        suitable_characters.remove("Коломбина")
                                        required_gidro_nord_karai_person = True; SD += 1
                                        if "Иллуги" in suitable_characters: # Проверка, есть ли Иллуги, при учёте наличия Коломбины
                                            command.append("Иллуги")
                                            suitable_characters.remove("Иллуги")
                                            required_geo_nord_karai_person = True; S += 1
                                            break
                                    else:
                                        if "Иллуги" in suitable_characters: # Проверка, есть ли Иллуги, при учёте отсутствия Коломбины
                                            command.append("Иллуги")
                                            suitable_characters.remove("Иллуги")
                                            required_geo_nord_karai_person = True; S += 1
                                        if "Айно" in suitable_characters:
                                            command.append("Айно")
                                            suitable_characters.remove("Айно")
                                            required_gidro_nord_karai_person = True; SD += 1
                                        break
                                    
                            if required_geo_nord_karai_person and required_gidro_nord_karai_person:
                                if SD < Max_SD:
                                    if "Коломбина" in command: subdamaggers_list.remove("Коломбина")
                                    elif "Айно" in command: subdamaggers_list.remove("Айно")
                                    command.append(subdamaggers_list[0]); SD += 1
                                elif S < Max_S:
                                    supports_list.remove("Иллуги")
                                    command.append(supports_list[0]); S += 1
                                
                            else: # Случай, если у человека нет ни одного Гео/Гидро Нод-Край персонажа
                                suitable_characters = [] # Подходящие под Цзы Бай персонажи, а именно Нин Гуан, Тиори, Альбедо
                                if "Нин Гуан" in your_character_list:
                                    supports_list.append("Нин Гуан")
                                if "Тиори" in your_character_list:
                                    supports_list.append("Тиори")
                                if "Альбедо" in your_character_list:
                                    supports_list.append("Альбедо") 
                                if len(suitable_characters) == 0:
                                    while (SD < Max_SD and S < Max_S):
                                        if SD < Max_SD:
                                            command.append(subdamaggers_list[SD:][0]); SD += 1
                                        if S < Max_S:
                                            command.append(supports_list[S:][0]); S += 1
                                            
                        elif damagger == "Итто": # Теперь обрабатываем Итто
                            tiori, albedo = False, False # флаги для описка АЛьбедо и Тиори
                            for char_sub_dd_for_itto in subdamaggers_list:
                                if char_sub_dd_for_itto == "Тиори": tiori = True
                                elif char_sub_dd_for_itto == "Альбедо": albedo = True
                            if tiori and albedo:
                                command.append(random.choice(["Тиори", "Альбедо"]))
                                command_elements.append("Ge")
                            elif tiori or albedo:
                                command.append("Тиори" if tiori else "Альбедо")
                                command_elements.append("Ge")
                                
                        elif damagger == "Навия": # Теперь обрабатываем Навию
                            pass

                    # Главный дамаггер анемо стихии
                    elif character_elements[damagger] == "A":
                        command_elements.append("A")
                        if character_fraction[damagger] == "-":
                            pass
                        else:
                            # Поиск сабдамаггера из такой же фракции электро, гидро, крио или пиро стихии
                            for i in Max_SD:
                                fraction_subdamagger, fraction_subdamagger_element = None, None
                                for (name, element), (_, fraction) in zip(character_elements.items(), character_fraction.items()):
                                    if element in ["E", "G", "P", "K"] and fraction == character_fraction[damagger] and (name in subdamaggers_list):
                                        fraction_subdamagger = name
                                        SD += 1
                                        fraction_subdamagger_element = element
                                if fraction_subdamagger == None: break
                                else: 
                                    command.append(fraction_subdamagger)
                                    command_elements.append(fraction_subdamagger_element)

                            for j in Max_S:
                                fraction_support, fraction_support_element = None, None
                                for (name, element), (_, fraction) in zip(character_elements.items(), character_fraction.items()):
                                    if element in ["E", "G", "P", "K"] and fraction == character_fraction[damagger] and (name in supports_list):
                                        fraction_support = name
                                        S += 1
                                        fraction_support_element = element
                                if fraction_support == None: break
                                else: 
                                    command.append(fraction_support)
                                    command_elements.append(fraction_support_element)

                    # Главный дамаггер электро стихии
                    elif character_elements[damagger] == "E": 
                        
                        # Дамаггер из Нод-Края, значит это Флинс, под него в первую очередь СОбираем Инеффу и Коломбину,
                        # если нет их двоих, то пихаем Айно, чтобы закрыть синергию нодкраевцев до второго уровня,
                        # если и она отсутствует, то собираем просто хороших гидро и электро сабдд и саппортов
                        if character_fraction[damagger] == "Нод-Край":
                            if "Коломбина" in your_character_list and "Инеффа" in your_character_list:
                                command += "Коломбина", "Инеффа"
                                command_elements += "G", "E"
                                if Max_SD < 2: SD -= 1; S -= 1
                                else: SD -= 2
                            elif "Коломбина" in your_character_list:
                                command.append("Коломбина")
                                command_elements.append("G")
                                SD -= 1
                            elif "Инеффа" in your_character_list:
                                command.append("Инеффа")
                                command_elements.append("E")
                                SD -= 1
                            elif "Айно" in your_character_list:
                                command.append("Айно")
                                command_elements.append("G")
                                SD -= 1
                            
                            # Не нашлось ни одного подходящего персонажа из Нод-Края
                            else:
                                now_SD, now_S, new_members, element_of_members = electro_and_gydor_subdd_or_support(Max_SD, subdamaggers_list, supports_list)
                                if len(element_of_members) == 0 and (now_SD != 0 or now_S != 0):
                                    command += new_members
                                    command_elements += ["G", "E"]
                                elif len(element_of_members) == 1:
                                    command += new_members
                                    command_elements += element_of_members
                                    Max_SD -= now_SD; Max_S -= now_S
                                
                        # Электро дамаггер не из Нод-края, значит приоритетно собираем команду в реакцию заряжен, а потом же в перегрузку,
                        # ещё ниже по приоритету стоят реакции Вегетация/Стимуляция, Разрастание, Обострение
                        else:
                            now_SD, now_S, new_members, element_of_members = electro_and_gydor_subdd_or_support(Max_SD, subdamaggers_list, supports_list)
                            command += new_members
                            command_elements += element_of_members
                            Max_SD -= now_SD; Max_S -= now_S

                    # Главный дамаггер дендро стихии
                    elif character_elements[damagger] == "D": 
                        pass

            # Поиск сабдамаггера
            elif position == "SD" and SD < Max_SD:
                command.append(subdamaggers_list[SD:][0]); SD += 1

            # Поиск саппорта
            elif position == "S" and S < Max_S:
                command.append(supports_list[S:][0]); S += 1


    # --------------------- 3. Моноэлементная пачка --------------------- 
    elif mode == 3:
            for position in pattern.split("."):
                # Поиск дамаггера
                if position == "D" and D < Max_D:
                    for character in damaggers_list:
                        if character["element_code"] == desired_element and character not in command:
                            command.append(character)
                            D += 1
                            break

                # Поиск сабдамаггера
                elif position == "SD" and SD < Max_SD:
                    for character in subdamaggers_list:
                        if character["element_code"] == desired_element and character not in command:
                            command.append(character)
                            SD += 1
                            break
                
                # Поиск саппорта
                elif position == "S" and S < Max_S:
                    for character in supports_list:
                        if character["element_code"] == desired_element and character not in command:
                            command.append(character)
                            S += 1
                            break

    # Пользователь указывает невероное (не существующее) значение режима
    else:
        raise ValueError("Неверное значение режима.")

    return command

print("Выберите способ генерации команды (0 - случайный, 1 - лучший из лучших, 2 - сложный алгоритм составления(дольше), 3 - моноэлементальные пачик):  ", end=" ")

make_mode = int(input())
if make_mode == 3:
    print("Введите элемент вашей будущей команды:\n\t1. - Пиро\n\t2. - Гидро\n\t3. - Электро\n\t4. - Крио\n\t5. - Дендро\n\t6. - Гео\n\t7. - Анемо\nВведите нужный элемент: ", end="")
    desired_element = element_codes[input()]
    if element_characters_counter(your_character_list)[desired_element] < 4:
        raise ValueError("У вас недостаточно персонажей данной стихии.")
elif make_mode == 2 and len(your_character_list) <= 15:
    print("У вас слишком мало персонажей для данного алгоритма подбора, скорее всего он не сможет подобрать грамотный отряд")


my_command = make_command(make_mode, pattern_1)
print(" --- Ваш билд ---")
for i in my_command:
    print(f"{i["name"]} - {i["element"]}")