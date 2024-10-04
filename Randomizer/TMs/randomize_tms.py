import json
import random
import os
import Randomizer.shared_Variables as SharedVariables
import Randomizer.helper_function as HelperFunctions


def randomize_tms(config):
    if config["randomize_tms"] == "yes":
        tmsfile = HelperFunctions.open_json_file('TMs/itemdata_array_clean.json')
        movesfile = HelperFunctions.open_json_file('TMs/move_list.json')
        move_count = len(movesfile['moves']) - 1
        spoilers = HelperFunctions.spoilerlog("TM Changes")
        SharedVariables.usedMoves = []
        for item in tmsfile['values']:
            if item['ItemType'] == "ITEMTYPE_WAZA" and item['Id'] != 1230:
                rand = random.randint(0, move_count)
                choice_id = movesfile['moves'][rand]['id']

                if config["include_tms_without_animations"] == "yes":
                    while choice_id in SharedVariables.usedMoves:
                        rand = random.randint(0, move_count)
                        choice_id = movesfile['moves'][rand]['id']
                else:
                    while choice_id in SharedVariables.usedMoves or choice_id not in SharedVariables.allowed_moves:
                        rand = random.randint(0, move_count)
                        choice_id = movesfile['moves'][rand]['id']
                
                move_name = movesfile['moves'][rand]['name']
                spoilers.write(HelperFunctions.get_itemname(item['Id'])+": "+move_name+"\n")
                item['MachineWaza'] = movesfile['moves'][rand]['devName']
                SharedVariables.usedMoves.append(choice_id)
        spoilers.close()
        outdata = json.dumps(tmsfile, indent=2)
        with open(os.getcwd() + "/Randomizer/TMs/" + "itemdata_array.json", 'w') as outfile:
            outfile.write(outdata)
        return True
    return False

