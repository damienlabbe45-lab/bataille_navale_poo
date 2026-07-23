from typing import Self
from classe import Seabattle, Matrixbatlleship


class BatlleshipGame:
    def __init__(self: Self, name_playeur: str, ship_names: list[str], name_figther: str) -> None:
        self.playeur = Seabattle(name_playeur)
        self.figther = Matrixbatlleship(name_figther, ship_names)

    def choice_computer(self: Self) -> None:
        from secrets import choice
        coors = self.playeur.find_coor("^")
        dict_string_number = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10}
        cols_letter = list(dict_string_number.keys())

        if len(coors) != 0:
            coor: None | tuple[int, str] = None

            while coor is None:
                choice = choice(coors)
                coors_possiblility = [coor for coor in
                                      [(choice[0] - 1, choice[1]), (choice[0] + 1, choice[1]),
                                       (choice[0], cols_letter[dict_string_number[choice[1]] + 1]),
                                       (choice[0], cols_letter[dict_string_number[choice[1]] - 1])]
                                      if self.playeur.map_battle.loc[coor[0], coor[1]] == " "]

                if len(coors_possiblility) != 0:
                    coor = choice(coors_possiblility)

                else:
                    coors.remove(choice)

        else:

            coor = choice(self.playeur.find_coor(" "))

        self.touch_ship(coor)

    def choice_human(self) -> None:
        """fonction servant à avoir les inputs du joueur jusqu'à qu'il met des coordonnées valides"""
        number = None
        while number is None:
            user_input = input("veillez indiquer les coordonnées pour tirer\n").upper()
            if user_input[0] not in self.playeur.map_battle.columns:
                print("veillez mettre A, B , C, D, E, F, G, H, I, J, au tout début. ce sera le nom de colonne")
            elif user_input[1:].isdigit():
                number = int(user_input[1:])
                if not (0 < number < 11):
                    number = None
                    print("Veillez mettre un nombre entre 1 et 10 après les colonnes")
        self.touch_ship(tuple(number, user_input[0]))

    def touch_ship(self: Self, coor: tuple[int, str]) -> None:
        if self.figther.map_battle.loc[coor[0], coor[1]] != " ":
            ship_name = self.figther.map_battle.loc[coor[0], coor[1]]
            ship = [ship for ship in self.figther.list_Ships if ship.name == ship_name][0]
            ship.ship_touch(coor)
            self.playeur.map_battle.loc[coor[0], coor[1]] = "^"
            if len(ship.coor) == 0:
                coors = self.figther.find_coor(ship_name)
                self.playeur.assign_coor(coors, ".")
        else:
            print(f"loupé {self.playeur.alias}")
            self.playeur.map_battle.loc[coor[0], coor[1]] = "~"

    def if_victory(self: Self) -> bool:
        return self.playeur.find_coor("^") != self.figther.find_not_coor(" ")

    def victory(self: Self) -> None:
        print(f"victoire {self.playeur.alias} !!!!!!")
