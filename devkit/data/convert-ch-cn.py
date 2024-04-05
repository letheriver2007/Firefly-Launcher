import os

########## CONFIG ##########
FILENAME = "2.1.5-zh-cn"
############################

current_file_path = os.path.abspath(__file__)
input_file_path = os.path.join(os.path.dirname(current_file_path), f"input\\{FILENAME}.txt")
avatar_file_path = os.path.join(os.path.dirname(current_file_path), "output\\avatar.txt")
lightcone_file_path = os.path.join(os.path.dirname(current_file_path), "output\\lightcone.txt")
item_file_path = os.path.join(os.path.dirname(current_file_path), "output\\item.txt")
food_file_path = os.path.join(os.path.dirname(current_file_path), "output\\food.txt")
head_file_path = os.path.join(os.path.dirname(current_file_path), "output\\head.txt")
monster_file_path = os.path.join(os.path.dirname(current_file_path), "output\\monster.txt")
stage_file_path = os.path.join(os.path.dirname(current_file_path), "output\\stage.txt")
scene_file_path = os.path.join(os.path.dirname(current_file_path), "output\\scene.txt")
relic_file_path = os.path.join(os.path.dirname(current_file_path), "output\\RELIC BY HAND.txt") # RELIC BY HAND

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

with open(input_file_path, "r", encoding="utf-8") as input_file:
    lines = input_file.readlines()
    for line in lines:
        if line.startswith(("# Avatars")):
            start_flag_avatar = True
        if line.startswith(("20000 :")):
            start_flag_lightcone = True
        if line.startswith(("# Items", "11001 :", "100000 : 荣", "210001 :")):
            start_flag_item = True
        if line.startswith(("400004 : 果")):
            start_flag_food = True
        if line.startswith(("200001 :")):
            start_flag_head = True
        if line.startswith(("# NPC")):
            start_flag_monster = True
        if line.startswith(("# Battle")):
            start_flag_stage = True
        if line.startswith(("# Mazes")):
            start_flag_scene = True
        if line.startswith(("61011 :")):
            start_flag_relic = True

        if start_flag_avatar and not line.startswith(("# Avatars", "# Items")):
            avatar_lines.append(line)
        elif start_flag_lightcone and not line.startswith(("31011 :")):
            lightcone_lines.append(line)
        elif start_flag_item and not line.startswith(("# Items", "1001 : 三", "20000 :", "200001 :", "400004 : 果")):
            item_lines.append(line)
        elif start_flag_food and not line.startswith(("# Props")):
            food_lines.append(line)
        elif start_flag_head and not line.startswith(("210001 :")):
            head_lines.append(line)
        elif start_flag_monster and not line.startswith(("# NPC", "# Battle")):
            monster_lines.append(line)
        elif start_flag_stage and not line.startswith(("# Battle", "# Mazes")):
            stage_lines.append(line)
        elif start_flag_scene and not line.startswith(("# Mazes")):
            scene_lines.append(line)
        elif start_flag_relic and not line.startswith(("71000 :")):
            relic_lines.append(line)

        if start_flag_avatar and line.startswith(("# Items")):
            start_flag_avatar = False
        elif start_flag_lightcone and line.startswith(("31011 :")):
            start_flag_lightcone = False
        elif start_flag_item and line.startswith(("1001 : 三", "20000 :", "200001 :", "400004 : 果")):
            start_flag_item = False
        elif start_flag_food and line.startswith(("# Props")):
            start_flag_food = False
        elif start_flag_head and line.startswith(("210001 :")):
            start_flag_head = False
        elif start_flag_monster and line.startswith(("# Battle")):
            start_flag_monster = False
        elif start_flag_stage and line.startswith(("# Mazes")):
            start_flag_stage = False
        elif start_flag_scene and line.startswith(("THE END")):
            start_flag_scene = False
        elif start_flag_relic and line.startswith(("71000 :")):
            start_flag_relic = False

def write_to_file(file_path, lines):
    lines = list(filter(lambda x: x.strip(), lines))
    with open(file_path, "w", encoding="utf-8") as output_file:
        output_file.write("".join(lines))
    with open(file_path, "r+", encoding="utf-8") as file:
        content = file.read()
        content = content.rstrip("\n")
        file.seek(0)
        file.write(content)
        file.truncate()

write_to_file(avatar_file_path, avatar_lines)
write_to_file(lightcone_file_path, lightcone_lines)
write_to_file(item_file_path, item_lines)
write_to_file(food_file_path, food_lines)
write_to_file(head_file_path, head_lines)
write_to_file(monster_file_path, monster_lines)
write_to_file(stage_file_path, stage_lines)
write_to_file(scene_file_path, scene_lines)
write_to_file(relic_file_path, relic_lines)