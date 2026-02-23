import customtkinter as ctk
from helpful_funcs import read_characters_from_json, make_character_json, element_characters_counter
from start import make_command
from const_lists import element_codes, list_of_resonance
import json
from collections import Counter
# from PIL import Image



def my_custom_generation_function(selected_characters, mode, target_element) -> tuple:
    """
    Сюда будет передаваться список имён выбранных персонажей.
    
    Заглушка
    """
    print(f"[LOG] Персонажи: {selected_characters}")
    print(f"[LOG] Режим: {mode}")
    print(f"[LOG] Целевой элемент: {target_element}")

    # Формируем новый JSON-файл с персонажами пользователя
    make_character_json("user_characters_data.json", selected_characters)
    print("[LOG] Новый JSON-файл создан")

    pattern_1 = "D.SD.S.S"
    pattern_2 = "D.SD.SD.S"

    # Определяем режим составления команды
    match mode:
        case "Случайный": make_mode = 0
        case "Лучший из лучших": make_mode = 1
        case "Профи": make_mode = 2
        case "Моноэлемент": make_mode = 3
    print(f"[LOG] Режиму генерации присвоен номер {make_mode}")

    # Определяем желаемый элемент дамаггера
    desired_element = "-"

    if target_element != "Любой":
        desired_element = element_codes[target_element]
        if element_characters_counter(selected_characters)[desired_element] < 4:
            raise ValueError("У вас недостаточно персонажей данной стихии.")
    
    print(f"[LOG] Выбран целевой элемент {desired_element}")

    # Формируем команду пользователя
    user_command, user_command_elements = make_command(make_mode, pattern_2, desired_element)
    user_resonance = []
    print(user_command_elements)

    if len(Counter(user_command_elements)) != 4:
        for key, value in Counter(user_command_elements).items():
            if value >= 2:
                user_resonance.append(list_of_resonance[key])
    else: 
        user_resonance.append("Элементальное сопротивление +15%, физ. сопротивление +15%.")

    print("[LOG] Команда сгенерированна")
    
    return user_command, user_resonance


class TeamBuilderApp(ctk.CTk):
    def __init__(self, characters_list, owned_characters):
        super().__init__()

        self.title("Сборщик команд")
        self.geometry("900x850") # Увеличил высоту для новых кнопок
        
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("green") 

        self.characters_list = characters_list
        self.owned_characters = owned_characters
        self.checkbox_vars = {}
        self.current_generated_team = [] # Для хранения данных последнего отряда

        # # Путь к иконкам
        # self.icons_path = os.path.join(CURRENT_DIR, "assets")
        # self.profile_image = self.load_icon("profile_icon.png", (20, 20))
        # self.magic_image = self.load_icon("magic_icon.png", (24, 24))

        self.setup_ui()

    # def load_icon(self, filename, size):
    #     path = os.path.join(self.icons_path, filename)
    #     if os.path.exists(path):
    #         return ctk.CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=size)
    #     return None

    def open_info(self):
        """Окно с инструкцией"""
        info_window = ctk.CTkToplevel(self)
        info_window.title("Инструкция")
        info_window.geometry("400x300")
        info_window.attributes("-topmost", True)
        
        label = ctk.CTkLabel(info_window, text="Как пользоваться программой", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=15)
        
        text_area = ctk.CTkTextbox(info_window, width=350, height=180)
        text_area.pack(padx=20, pady=10)
        text_area.insert("0.0", "Здесь будет ваша инструкция...\n\n1. Выберите персонажей.\n2. Выберите режим.\n3. Нажмите генерацию.\n4. Сохраните понравившийся отряд.")
        text_area.configure(state="disabled")

    def open_profile(self):
        profile_window = ctk.CTkToplevel(self)
        profile_window.title("Мой профиль")
        profile_window.geometry("300x200")
        profile_window.attributes("-topmost", True)
        
        ctk.CTkLabel(profile_window, text="Профиль пользователя", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        ctk.CTkLabel(profile_window, text=f"Всего персонажей: {len(self.characters_list)}\nУ вас в наличии: {len(self.owned_characters)}").pack(pady=10)

    def setup_ui(self):
        # Верхняя панель
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=30, pady=(20, 10))
        
        # Инфо-кнопка (слева)
        self.info_btn = ctk.CTkButton(
            self.top_bar, text="?", width=40, height=40, 
            corner_radius=10, command=self.open_info, font=ctk.CTkFont(size=18, weight="bold")
        )
        self.info_btn.pack(side="left")

        self.title_label = ctk.CTkLabel(
            self.top_bar, text="Сборщик команд", 
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.title_label.pack(side="left", expand=True)

        # Кнопка профиля (справа)
        self.profile_btn = ctk.CTkButton(
            self.top_bar, text="Мой профиль",
            compound="left", width=140, height=40, command=self.open_profile, font=ctk.CTkFont(size=14, weight="bold")
        )
        self.profile_btn.pack(side="right")

        self.subtitle_label = ctk.CTkLabel(self, text="Выберите персонажей, которые у вас есть:", text_color="gray")
        self.subtitle_label.pack(anchor="w", padx=35, pady=(0, 10))

        # Блок персонажей
        self.scroll_container = ctk.CTkScrollableFrame(self, height=250, fg_color="transparent")
        self.scroll_container.pack(fill="x", padx=30)
        
        self.grid_frame = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.grid_frame.pack(expand=True)

        columns = 4
        for index, char_name in enumerate(self.characters_list):
            # Устанавливаем "on", если персонаж есть в файле user_characters_data
            initial_state = "on" if char_name in self.owned_characters else "off"
            var = ctk.StringVar(value=initial_state)
            self.checkbox_vars[char_name] = var
            
            # Создаем "блок" для персонажа (как на концепте)
            char_card = ctk.CTkFrame(self.grid_frame, corner_radius=8, border_width=1, border_color="#D1D1D1")
            char_card.grid(row=index // columns, column=index % columns, padx=8, pady=8, sticky="nsew")
            
            cb = ctk.CTkCheckBox(
                char_card, text=char_name, variable=var, 
                onvalue="on", offvalue="off", font=ctk.CTkFont(size=13)
            )
            cb.pack(padx=15, pady=10)

        # Настройки
        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(self.settings_frame, text="Режим:").grid(row=0, column=0, padx=5)
        self.mode_menu = ctk.CTkOptionMenu(self.settings_frame, values=["Случайный", "Лучший из лучших", "Профи", "Моноэлемент"])
        self.mode_menu.grid(row=0, column=1, padx=(0, 20))

        ctk.CTkLabel(self.settings_frame, text="Элемент:").grid(row=0, column=2, padx=5)
        self.element_menu = ctk.CTkOptionMenu(self.settings_frame, values=["Любой", "Пиро", "Крио", "Гидро", "Электро", "Дендро", "Гео", "Анемо"])
        self.element_menu.grid(row=0, column=3)

        # Генерация
        self.generate_btn = ctk.CTkButton(
            self, text="Начать генерацию", compound="left",
            font=ctk.CTkFont(size=16, weight="bold"), height=45, command=self.on_generate_click
        )
        self.generate_btn.pack(pady=10)

        # Результат
        ctk.CTkLabel(self, text="Результат:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))

        self.result_textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(size=14), corner_radius=10, height=150)
        self.result_textbox.pack(fill="x", padx=30, pady=(0, 10))
        self.result_textbox.configure(state="disabled")

        # Кнопка сохранения (внизу)
        self.save_btn = ctk.CTkButton(
            self, text="Сохранить отряд", width=200, height=40, text_color="white",
            command=self.on_save_team_click, font=ctk.CTkFont(size=16, weight="bold")
        )
        self.save_btn.pack(anchor="w", padx=30, pady=(0, 20))

    def on_generate_click(self):
        selected_chars = [char for char, var in self.checkbox_vars.items() if var.get() == "on"]
        current_mode = self.mode_menu.get()
        current_element = self.element_menu.get()

        # Сохраняем результат в переменную класса для последующего сохранения в файл
        self.current_generated_team, self.resonance_of_current_generated_team = my_custom_generation_function(selected_chars, current_mode, current_element)

        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("1.0", "end")

        if not self.current_generated_team:
            self.result_textbox.insert("end", "Команда не найдена.")
        else:
            for char in self.current_generated_team:
                line = f"⚔️ {char.get('name')} | {char.get('element')} | {char.get('weapon_type')}\n"
                self.result_textbox.insert("end", line)

        self.result_textbox.insert("end", "- "*50 + "\n")
        for resonance in self.resonance_of_current_generated_team:
            line = f"* {resonance}\n"
            self.result_textbox.insert("end", line)

        self.result_textbox.configure(state="disabled")

    def on_save_team_click(self):
        """Функция сохранения текущего отряда в JSON"""
        # 1. Получаем текст из результата
        result_text = self.result_textbox.get("1.0", "end-1c").strip()
        
        if not result_text or "Команда не найдена" in result_text:
            print("[LOG] Нечего сохранять")
            return

        # Путь к файлу сохранений
        save_path = "user_app_data.json"
        
        # Подготавливаем данные для сохранения
        new_entry = {
            "timestamp": "2024-05-20 12:00", # Тут можно добавить реальное время
            "mode": self.mode_menu.get(),
            "element": self.element_menu.get(),
            "team_raw": result_text,
            "team_data": self.current_generated_team # Сохраняем структурированные данные
        }

        # 2. Читаем существующие данные
        data = []
        try:
            with open(save_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except: data = []

        # 3. Добавляем и записываем
        data.append(new_entry)
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"[LOG] Отряд успешно сохранен в {save_path}")
            # Здесь можно добавить уведомление пользователю в UI
        except Exception as e:
            print(f"[LOG] Ошибка сохранения: {e}")


if __name__ == "__main__":
    name_list = []
    for x in read_characters_from_json("all_characters_data.json"):
        for y in x:
            name_list.append(y["name"])
    name_list = list(set(name_list))
    name_list.sort()
    
    owned_names = []
    try:
        with open("user_characters_data.json", "r", encoding="utf-8") as f:
            user_data = json.load(f)
            owned_names = [char["name"] for char in user_data]
    except Exception as e:
        print(f"Ошибка чтения данных пользователя: {e}")

    app = TeamBuilderApp(characters_list=name_list, owned_characters=owned_names)
    app.mainloop()