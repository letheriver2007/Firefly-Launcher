import os
import re
import shutil

def handleResDevide():
    start_flag_avatar = False
    start_flag_lightcone = False
    start_flag_item = False
    start_flag_food = False
    start_flag_head = False
    start_flag_monster = False
    start_flag_stage = False
    start_flag_scene = False
    start_flag_relic = False

    avatar_lines = []
    lightcone_lines = []
    item_lines = []
    food_lines = []
    head_lines = []
    monster_lines = []
    stage_lines = []
    scene_lines = []
    relic_lines = []

    config_100000 = {'CHS': "100000 : 荣", 'EN': "100000 : Star", 'CHT': "100000 : 榮"}
    config_400004 = {'CHS': "400004 : 果", 'EN': "400004 : Comfort", 'CHT': "400004 : 果"}
    config_1001 = {'CHS': "1001 : 三", 'EN': "1001 : March", 'CHT': "1001 : 三"}
    try:
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            lines = input_file.readlines()
            for line in lines:
                if line.startswith("# Avatars"):
                    start_flag_avatar = True
                if line.startswith("20000 :"):
                    start_flag_lightcone = True
                if line.startswith(("# Items", "11001 :", config_100000[LANGUAGE], "210001 :")):
                    start_flag_item = True
                if line.startswith((config_400004[LANGUAGE])):
                    start_flag_food = True
                if line.startswith("200001 :"):
                    start_flag_head = True
                if line.startswith("# NPC"):
                    start_flag_monster = True
                if line.startswith("# Battle"):
                    start_flag_stage = True
                if line.startswith("# Mazes"):
                    start_flag_scene = True
                if line.startswith("61011 :"):
                    start_flag_relic = True

                if start_flag_avatar and not line.startswith(("# Avatars", "# Items")):
                    avatar_lines.append(line)
                elif start_flag_lightcone and not line.startswith("31011 :"):
                    lightcone_lines.append(line)
                elif start_flag_item and not line.startswith(
                        ("# Items", config_1001[LANGUAGE], "20000 :", "200001 :", config_400004[LANGUAGE])):
                    item_lines.append(line)
                elif start_flag_food and not line.startswith("# Props"):
                    food_lines.append(line)
                elif start_flag_head and not line.startswith("210001 :"):
                    head_lines.append(line)
                elif start_flag_monster and not line.startswith(("# NPC", "# Battle")):
                    monster_lines.append(line)
                elif start_flag_stage and not line.startswith(("# Battle", "# Mazes")):
                    stage_lines.append(line)
                elif start_flag_scene and not line.startswith("# Mazes"):
                    scene_lines.append(line)
                elif start_flag_relic and not line.startswith("71000 :"):
                    relic_lines.append(line)

                if start_flag_avatar and line.startswith("# Items"):
                    start_flag_avatar = False
                elif start_flag_lightcone and line.startswith("31011 :"):
                    start_flag_lightcone = False
                elif start_flag_item and line.startswith(
                        (config_1001[LANGUAGE], "20000 :", "200001 :", config_400004[LANGUAGE])):
                    start_flag_item = False
                elif start_flag_food and line.startswith("# Props"):
                    start_flag_food = False
                elif start_flag_head and line.startswith("210001 :"):
                    start_flag_head = False
                elif start_flag_monster and line.startswith("# Battle"):
                    start_flag_monster = False
                elif start_flag_stage and line.startswith("# Mazes"):
                    start_flag_stage = False
                elif start_flag_scene and line.startswith("THE END"):
                    start_flag_scene = False
                elif start_flag_relic and line.startswith("71000 :"):
                    start_flag_relic = False
    except FileNotFoundError:
        input("文件不存在, 请确认文件名是否正确.")

    config_1 = {'CHS': '头部', 'EN': 'Head', 'CHT': '頭部'}
    config_2 = {'CHS': '手部', 'EN': 'Hand', 'CHT': '手部'}
    config_3 = {'CHS': '躯干', 'EN': 'Body', 'CHT': '躯干'}
    config_4 = {'CHS': '脚部', 'EN': 'Foot', 'CHT': '腳部'}
    config_5 = {'CHS': '位面球', 'EN': 'Sphere', 'CHT': '位面球'}
    config_6 = {'CHS': '连结绳', 'EN': 'Rope', 'CHT': '連結繩'}
    configs = [config_1, config_2, config_3, config_4, config_5, config_6]
    new_relic_lines = []

    for line in relic_lines:
        relic_id = line.split(" : ")[0][-1]
        config_index = int(relic_id) - 1
        config = configs[config_index][LANGUAGE]
        new_line = f"{line.strip()} : {config}\n"
        new_relic_lines.append(new_line)

    handleResSave(avatar_file_path, avatar_lines)
    handleResSave(lightcone_file_path, lightcone_lines)
    handleResSave(item_file_path, item_lines)
    handleResSave(food_file_path, food_lines)
    handleResSave(head_file_path, head_lines)
    handleResSave(monster_file_path, monster_lines)
    handleResSave(stage_file_path, stage_lines)
    handleResSave(scene_file_path, scene_lines)
    handleResSave(relic_file_path, new_relic_lines)

def handleResSave(file_path, lines):
    lines = list(filter(lambda x: x.strip(), lines))
    with open(file_path, "w", encoding="utf-8") as output_file:
        output_file.write("".join(lines))
    with open(file_path, "r+", encoding="utf-8") as file:
        content = file.read()
        content = content.rstrip("\n")
        file.seek(0)
        file.write(content)
        file.truncate()

    input_entry_path = os.path.join(os.path.dirname(current_file_path), f"default\\entry-{LANGUAGE}.txt")
    output_entry_path = os.path.join(os.path.dirname(current_file_path), "output\\entry.txt")
    shutil.copy(input_entry_path, output_entry_path)

def handleConfigLoad():
    start_flag_avatar = False
    start_flag_relic = False
    avatar_lines = []
    relic_lines = []

    try:
        with open(f'{current_file_path}/../handbook/{VERSION}-CHS.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("# Avatars"):
                    start_flag_avatar = True
                if line.startswith("61011 :"):
                    start_flag_relic = True

                if start_flag_avatar and not line.startswith(("# Avatars", "# Items")):
                    avatar_lines.append(line)
                elif start_flag_relic and not line.startswith("71000 :"):
                    relic_lines.append(line)

                if start_flag_avatar and line.startswith("# Items"):
                    start_flag_avatar = False
                elif start_flag_relic and line.startswith("71000 :"):
                    start_flag_relic = False

        with open(f'{current_file_path}/../output/avatar.txt', 'r', encoding='utf-8') as file:
            avatar = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]

        with open(f'{current_file_path}/../output/relic.txt', 'r', encoding='utf-8') as file:
            relic = [line for line in file.readlines() if
                     not (line.strip().startswith("//") or line.strip().startswith("#"))]
    except FileNotFoundError:
        input("文件不存在, 请确认文件名是否正确.")

    for line in avatar_lines:
        line = line.strip()
        parts = line.split(' : ')
        if len(parts) == 2:
            config_know_data[parts[1]] = parts[0]
    for i, line in enumerate(relic_lines):
        line = line.strip()
        parts = line.split(' : ')
        if len(parts) == 2:
            config_know_data[parts[1]] = parts[0]

    for i, line in enumerate(avatar):
        line = line.strip()
        parts = line.split(' : ')
        config_target_data[parts[0]] = parts[1]
    for i, line in enumerate(relic):
        line = line.strip()
        parts = line.split(' : ')
        config_target_data[parts[0]] = parts[1]

def handleMyRelicTranslate():
    input_myrelic_path = os.path.join(os.path.dirname(current_file_path), "default\\myrelic.txt")
    output_myrelic_path = os.path.join(os.path.dirname(current_file_path), "output\\myrelic.txt")

    if LANGUAGE == 'CHS':
        shutil.copy(input_myrelic_path, output_myrelic_path)
    else:
        handleConfigLoad()
        config_part = {'头部': 'Head', '手部': 'Hand', '躯干': 'Body', '脚部': 'Foot', '位面球': 'Sphere', '连接绳': 'Rope'}
        config_discribe_break = {'CHS': '击破', 'EN': 'Break', 'CHT': '擊破'}
        config_discribe_speed = {'CHS': '高速', 'EN': 'HSpeed', 'CHT': '高速'}
        config_discribe_heal = {'CHS': '坦克', 'EN': 'Tank', 'CHT': '坦克'}

        try:
            with open(input_myrelic_path, 'r', encoding='utf-8') as infile, open(output_myrelic_path, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    line = line.strip()
                    parts = line.split(' : ')
                    if parts[0] in config_know_data:
                        relic_id = config_know_data[parts[0]]
                        if relic_id in config_target_data:
                            parts[0] = config_target_data[relic_id]

                    if parts[1] in config_part:
                        parts[1] = config_part[parts[1]]

                    if '(' in parts[2]:
                        avatar, describe = parts[2].split('(', 1)
                        describe = describe.strip(')')
                        if describe in config_discribe_break['CHS']:
                            describe = config_discribe_break[LANGUAGE]
                        elif describe in config_discribe_speed['CHS']:
                            describe = config_discribe_speed[LANGUAGE]
                        elif describe in config_discribe_heal['CHS']:
                            describe = config_discribe_heal[LANGUAGE]
                    else:
                        avatar = parts[2]
                        describe = ''

                    if avatar in config_know_data:
                        avatar_id = config_know_data[avatar]
                        if avatar_id in config_target_data:
                            if describe != '':
                                parts[2] = f'{config_target_data[avatar_id]}({describe})'
                            else:
                                parts[2] = config_target_data[avatar_id]

                    outfile.write(' : '.join(parts) + '\n')

        except FileNotFoundError:
            print(f"未找到文件 {input_myrelic_path}")


if __name__ == '__main__':
    print("请确认您的文件名格式为X.X.X(版本号)-XXX(语言代码).txt")
    VERSION = input("输入版本号: ")
    LANGUAGE = input("输入语言代码(CHS/EN/CHT): ")
    FILENAME = VERSION + "-" + LANGUAGE

    current_file_path = os.path.abspath(__file__)

    input_file_path = os.path.join(os.path.dirname(current_file_path), f"handbook\\{FILENAME}.txt")
    output_folder_path = os.path.join(os.path.dirname(current_file_path), "output")
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    avatar_file_path = os.path.join(os.path.dirname(current_file_path), "output\\avatar.txt")
    lightcone_file_path = os.path.join(os.path.dirname(current_file_path), "output\\lightcone.txt")
    item_file_path = os.path.join(os.path.dirname(current_file_path), "output\\item.txt")
    food_file_path = os.path.join(os.path.dirname(current_file_path), "output\\food.txt")
    head_file_path = os.path.join(os.path.dirname(current_file_path), "output\\head.txt")
    monster_file_path = os.path.join(os.path.dirname(current_file_path), "output\\monster.txt")
    stage_file_path = os.path.join(os.path.dirname(current_file_path), "output\\stage.txt")
    scene_file_path = os.path.join(os.path.dirname(current_file_path), "output\\scene.txt")
    relic_file_path = os.path.join(os.path.dirname(current_file_path), "output\\relic.txt")

    handleResDevide()

    config_know_data = {}
    config_target_data = {}
    handleMyRelicTranslate()
