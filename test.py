from const_lists import *


for (name, element), (_, role) in zip(character_elements.items(), character_roles.items()):
    if element == "A" and (role == "D" or ("D" in role and "SD" not in role)):
        print(f"{name} - {role}; ")
