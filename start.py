from const_lists import *
from helpful_funcs import *
import random

# Допустимые паттерны создания команд 
pattern_1 = "D.SD.S.S"
pattern_1 = "D.SD.SD.S"


# Желаемая стихия даммагера
desired_element = "-"

damaggers_list, subdamaggers_list, supports_list = read_characters_from_json("user_characters_data.json")


# ------------------------- Необходимые функции -------------------------
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
# -----------------------------------------------------------------------------------------------------



# ------------------------- Функции непосредственно с поиском персонажей -------------------------

def find_gydro_kryo_subdd(our_command: list) -> None|dict:
    """ 
    Функция для поиска гидро или крио. 
    В случаи успешной "находки" возвращает словарь с данными персонажа, в ином случаи None
    """
    gydro_or_kryo_subdd = None
    for char in subdamaggers_list:
        if char["element_code"] in ["G", "K"] and char not in our_command:
            gydro_or_kryo_subdd = char
            break
    return gydro_or_kryo_subdd

def find_element_subdd_or_sup(our_command: list, element_code: str, role: str) -> None|dict:
    """ 
    Функция для поиска сабдд или саппорта одной определеённой стихии. 
    В случаи успешной "находки" возвращает словарь с данным персонажем, в ином случаи None
    """
    necessary_person = None
    if role == "SD":
        for char in subdamaggers_list:
            if char["element_code"] == element_code and char not in our_command:
                necessary_person = char
                break
    elif role == "S":
        for char in supports_list:
            if char["element_code"] == element_code and char not in our_command:
                necessary_person = char
                break
    return necessary_person

def find_remaining_supports(our_command: list, cnt_of_S: int) -> list[dict]:
    """ 
    Функция находит недостающих персонажей на позиции саппортов 
    На вход принимает уже имеющуюся команду, а также количество персонажей, которые нужно найти
    """
    remaining_supports = []
    temp_cnt = 0 
    for char in supports_list:
        if char not in our_command and temp_cnt < cnt_of_S:
            remaining_supports.append(char); temp_cnt += 1
    return remaining_supports

def find_remaining_sudamaggers(our_command: list, cnt_of_SD: int) -> list[dict]:
    """ 
    Функция находит недостающих персонажей на позиции сабдамаггеров 
    На вход принимает уже имеющуюся команду, а также количество персонажей, которые нужно найти
    """
    remaining_subdamaggers = []
    temp_cnt = 0 
    for char in subdamaggers_list:
        if char not in our_command and temp_cnt < cnt_of_SD:
            remaining_subdamaggers.append(char); temp_cnt += 1
    return remaining_subdamaggers

# -----------------------------------------------------------------------------------------------------



# СОРТИРУЕМ списки по рангу для каждой роли
damaggers_list = progressive_sort(damaggers_list, "D")
subdamaggers_list = progressive_sort(subdamaggers_list, "SD")
supports_list = progressive_sort(supports_list, "S")




def make_command(mode: int, pattern: str) -> list[dict]:
    """
    Это основная функция программы, которая создаёт для вас граммотную команду персонажей на основе ваших запросов
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

                    # ********* Дамаггер - ПИРО *********
                    if damagger["element_code"] == "P":
                        new_member = find_gydro_kryo_subdd(command)
                        if new_member != None: 
                            command.append(new_member)
                            command_elements.append(new_member["element_code"])
                            SD += 1


                    # ********* Дамаггер - КРИО/ГИДРО *********
                    elif damagger["element_code"] in ["G", "K"]:
                        new_member = find_element_subdd_or_sup(command, "P", "SD")
                        if new_member != None: 
                            command.append(new_member)
                            command_elements.append(new_member["element_code"])
                            SD += 1


                    # ********* Дамаггер - ГЕО *********
                    elif damagger["element_code"] == "Ge":
                        # Сборка Гео даммагера непосредственно в его урон

                        # Сначала проверка на Цзы Бай
                        if character_fraction[damagger] == "Нод-Край": 
                            # Это Цзы Бай
                            required_geo_nord_karai_person = False # Прочерка на наличие гео персонажей из Нод-Края
                            required_gidro_nord_karai_person = False # Прочерка на наличие гидро персонажей из Нод-Края
                            suitable_characters = [] # Список для подходящих под Цзы Бай персонажей
                            suitable_characters_only_names = [] # Список для подходящих под Цзы Бай персонажей (только имена)
                            for char in your_character_list:
                                if char != damagger and char["fraction"] == "Нод-Край" and char["element_code"] in ["Ge", "G"]:
                                    suitable_characters.append(char)
                                    suitable_characters_only_names.append(char["name"])
                            if len(suitable_characters) != 0:
                                for char in suitable_characters:
                                    if "Коломбина" in suitable_characters_only_names: # Проверка, есть ли Коломбина
                                        command.append(suitable_characters[suitable_characters_only_names.index("Коломбина")])
                                        suitable_characters.pop(suitable_characters_only_names.index("Коломбина"))
                                        required_gidro_nord_karai_person = True; SD += 1
                                        if "Иллуги" in suitable_characters_only_names: # Проверка, есть ли Иллуги, при учёте наличия Коломбины
                                            command.append(suitable_characters[suitable_characters_only_names.index("Иллуги")])
                                            suitable_characters.pop(suitable_characters_only_names.index("Иллуги"))
                                            required_geo_nord_karai_person = True; S += 1
                                            break
                                    else:
                                        if "Иллуги" in suitable_characters_only_names: # Проверка, есть ли Иллуги, при учёте отсутствия Коломбины
                                            command.append(suitable_characters[suitable_characters_only_names.index("Иллуги")])
                                            suitable_characters.pop(suitable_characters_only_names.index("Иллуги"))
                                            required_geo_nord_karai_person = True; S += 1
                                        if "Айно" in suitable_characters_only_names:
                                            command.append(suitable_characters[suitable_characters_only_names.index("Айно")])
                                            suitable_characters.pop(suitable_characters_only_names.index("Айно"))
                                            required_gidro_nord_karai_person = True; SD += 1
                                        break
                                    
                            if required_geo_nord_karai_person and required_gidro_nord_karai_person:
                                if SD < Max_SD:
                                    for char in subdamaggers_list:
                                        if char not in command:
                                            command.append(char); SD += 1
                                elif S < Max_S:
                                    for char in supports_list:
                                        if char not in command:
                                            command.append(char); S += 1
                                
                            else: # Случай, если у человека нет ни одного Гео/Гидро Нод-Край персонажа
                                suitable_characters = [] # Подходящие под Цзы Бай персонажи, кроме Нодкраевцев, а именно Нин Гуан, Тиори, Альбедо
                                if "Нин Гуан" in your_character_list:
                                    suitable_characters.append("Нин Гуан")
                                if "Тиори" in your_character_list:
                                    suitable_characters.append("Тиори")
                                if "Альбедо" in your_character_list:
                                    suitable_characters.append("Альбедо") 
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

                    # ********* Дамаггер - АНЕМО *********
                    elif damagger["element_code"] == "A":
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

                    # ********* Дамаггер - ЭЛЕКТРО *********
                    elif damagger["element_code"] == "E": 
                        
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

                    # ********* Дамаггер - ДЕНДРО *********
                    elif damagger["element_code"] == "D": 
                        pass

                # Поиск сабдамаггера
                if position == "SD" and SD < Max_SD:
                    new_subdamaggers = find_remaining_sudamaggers(command, Max_SD - SD)
                    command += new_subdamaggers
                    for i in new_subdamaggers:
                        command_elements.append(i["element_code"])

                # Поиск саппорта
                if position == "S" and S < Max_S:
                    new_supports = find_remaining_supports(command, Max_S - S)
                    command += new_supports
                    for i in new_supports:
                        command_elements.append(i["element_code"])


            # ********** Желаемый элемент дамаггера ПИРО **********
            elif desired_element == "P" and D < Max_D:
                for char in damaggers_list:
                    pyro_damagger = None
                    if char["element_code"] == 'P':
                        pyro_damagger = char; D += 1
                        command.append(char); command_elements.append("P")
                        break
                if pyro_damagger == None:
                    raise TypeError("У вас отсутствует пиро персонаж подходящий на роль дамаггера")
                
                for i in range(Max_SD):
                    new_member = find_gydro_kryo_subdd(command)
                    if new_member != None:
                        command.append(new_member)
                        command_elements.append(new_member["element_code"])
                        SD += 1

                # Поиск сабдамаггеров, если они нужны
                if SD < Max_SD:
                    new_subdamaggers = find_remaining_sudamaggers(command, Max_SD - SD)
                    command += new_subdamaggers
                    for i in new_subdamaggers:
                        command_elements.append(i["element_code"])

                # Поиск саппорта
                if S < Max_S:
                    new_supports = find_remaining_supports(command, Max_S - S)
                    command += new_supports
                    for i in new_supports:
                        command_elements.append(i["element_code"])
            
            # ********** Желаемый элемент дамаггера ГИДРО **********
            elif desired_element == "G":
                new_member = find_element_subdd_or_sup(command, "P", "SD")
                if new_member != None: 
                    command.append(new_member)
                    command_elements.append(new_member["element_code"])
                    SD += 1

            # ********** Желаемый элемент дамаггера КРИО **********
            elif desired_element == "K":
                new_member = find_element_subdd_or_sup(command, "P", "SD")
                if new_member != None: 
                    command.append(new_member)
                    command_elements.append(new_member["element_code"])
                    SD += 1

            # ********** Желаемый элемент дамаггера ЭЛЕКТРО **********
            elif desired_element == "E":
                pass

            # ********** Желаемый элемент дамаггера ДЕНДРО **********
            elif desired_element == "D":
                pass

            # ********** Желаемый элемент дамаггера ГЕО **********
            elif desired_element == "Ge":
                pass

            # ********** Желаемый элемент дамаггера АНЕМО **********
            elif desired_element == "A":
                pass
                        

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
if make_mode == 3 or (make_mode == 2 and len(your_character_list) >= 15):
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