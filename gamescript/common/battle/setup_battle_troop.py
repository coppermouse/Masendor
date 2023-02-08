import csv
import os

import pygame
from gamescript import subunit
from gamescript.common import utility

stat_convert = utility.stat_convert

letter_board = (
    "a", "b", "c", "d", "e", "f", "g", "h")  # letter according to subunit position in inspect ui similar to chess board
number_board = ("8", "7", "6", "5", "4", "3", "2", "1")  # same as above
board_pos = []
for dd in number_board:
    for ll in letter_board:
        board_pos.append(ll + dd)
board_pos = tuple(board_pos)


def setup_battle_troop(self, team_subunit_list, specific_team=None):
    """
    Read unit battle data from unit_pos file
    :param self: Battle or Game object
    :param team_subunit_list: List of team subunit group, can be list for preview or dict for battle
    :param specific_team: Assign the unit to which specific team
    """
    main_dir = self.main_dir

    with open(os.path.join(main_dir, "data", "ruleset", self.ruleset_folder, "map",
                           self.map_selected, str(self.map_source),
                           "troop_pos.csv"), encoding="utf-8", mode="r") as unit_file:
        rd = tuple(csv.reader(unit_file, quoting=csv.QUOTE_ALL))
        header = rd[0]
        int_column = ("ID", "Faction", "Team", "Leader")  # value int only
        list_column = ["POS"]  # value in list only
        float_column = ("Angle", "Start Health", "Start Stamina")  # value in float
        int_column = [index for index, item in enumerate(header) if item in int_column]
        list_column = [index for index, item in enumerate(header) if item in list_column]
        float_column = [index for index, item in enumerate(header) if item in float_column]
        leader_subunit = {}
        for troop in rd[1:]:  # skip header
            for n, i in enumerate(troop):
                troop = stat_convert(troop, n, i, list_column=list_column, int_column=int_column,
                                     float_column=float_column)
            troop = {header[index]: stuff for index, stuff in enumerate(troop)}
            if specific_team is None or specific_team == troop["Team"]:  # check player control
                if type(team_subunit_list) == dict:
                    if troop["Team"] not in team_subunit_list:
                        team_subunit_list[troop["Team"]] = pygame.sprite.Group()
                    which_team = team_subunit_list[troop["Team"]]
                else:  # for character selection
                    which_team = team_subunit_list

                leader = None
                if troop["Leader"] != 0:
                    leader = leader_subunit[troop["Leader"]]

                add_subunit = subunit.Subunit(troop["Troop ID"], troop["ID"], troop["Team"], troop["POS"],
                                              troop["Angle"], troop["Start Health"], troop["Start Stamina"], leader,
                                              self.faction_data.coa_list[troop["Faction"]])
                if type(troop["Troop ID"]) is str:  # leader subunit from L string leader id as troop id
                    leader_subunit[add_subunit.game_id] = add_subunit
                which_team.add(add_subunit)

                # Recal highest possible hitbox distance for battle
                if self.hitbox_distance < add_subunit.subunit_hitbox_size:
                    self.hitbox_distance = add_subunit.subunit_hitbox_size

                for index, weapon in self.troop_data.weapon_list.items():
                    if index in add_subunit.weapon_id[0] or index in add_subunit.weapon_id[1]:
                        if weapon["Magazine"] == 0 and self.max_melee_weapon_range < weapon["Range"]:
                            self.max_melee_weapon_range = weapon["Range"]

    unit_file.close()
