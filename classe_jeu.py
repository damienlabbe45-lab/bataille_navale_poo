from typing import Self
from classes_de_base import Seabattle, Matrixbatlleship


class BatlleshipGame:
    """classe qui servira pour le joueur ou l'ordinateur sans possibilité de tricher"""

    def __init__(self: Self, name_playeur: str, ship_names: list[str], name_figther: str) -> None:
        self.player = Seabattle(name_playeur)
        self.figther = Matrixbatlleship(name_figther, ship_names)

    def choice_computer(self: Self) -> None:
        """choix de l'ordinateur pour saisir une coordonnée"""
        from secrets import choice
        coors = self.player.find_coor("^")
        dict_string_number = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10}
        cols_letter = list(dict_string_number.keys())

        if len(coors) != 0:
            coor: None | tuple[int, str] = None

            while coor is None and len(coors) > 0:
                selected_coor = choice(coors)
                row, col = selected_coor[0], selected_coor[1]
                col_idx = dict_string_number[col] - 1  # index de 0 à 9

                # Génération des voisins valides sur la grille 10x10
                neighbors = []
                if row > 1:

                    neighbors.append((row - 1, col))

                if row < 10:

                    neighbors.append((row + 1, col))

                if col_idx > 0:

                    neighbors.append((row, cols_letter[col_idx - 1]))

                if col_idx < 9:

                    neighbors.append((row, cols_letter[col_idx + 1]))

                coors_possiblility = [
                    c for c in neighbors
                    if self.player.map_battle.loc[c[0], c[1]] == " "
                ]

                if len(coors_possiblility) != 0:
                    coor = choice(coors_possiblility)
                else:
                    coors.remove(selected_coor)

            if coor is None:
                coor = choice(self.player.find_coor(" "))

        else:
            coor = choice(self.player.find_coor(" "))

        self.touch_ship(coor)

    def choice_human(self) -> None:
        """fonction servant à avoir les inputs du joueur jusqu'à qu'il met des coordonnées valides"""
        number = None
        while number is None:
            user_input = input("veillez indiquer les coordonnées pour tirer\n").upper()
            if user_input[0] not in self.player.map_battle.columns:
                print("veillez mettre A, B , C, D, E, F, G, H, I, J, au tout début. ce sera le nom de colonne")
            elif user_input[1:].isdigit():
                number = int(user_input[1:])
                if not (0 < number < 11):
                    number = None
                    print("Veillez mettre un nombre entre 1 et 10 après les colonnes")
        self.touch_ship((number, user_input[0]))

    def touch_ship(self: Self, coor: tuple[int, str]) -> None:
        """permet de vérifier si un navire adverse a été touché"""
        if self.figther.map_battle.loc[coor[0], coor[1]] != " ":
            ship_name: str = self.figther.map_battle.loc[coor[0], coor[1]]
            ship = [ship for ship in self.figther.list_Ships if ship.name == ship_name][0]
            ship.ship_touch(coor)
            self.player.map_battle.loc[coor[0], coor[1]] = "^"
            if len(ship.coor) == 0:
                coors = self.figther.find_coor(ship_name)
                self.player.assign_value(coors, ".")
        else:
            print(f"loupé {self.player.alias}")
            self.player.map_battle.loc[coor[0], coor[1]] = "~"

    def if_victory(self: Self) -> bool:
        """servira pour vérifier sur le while que tout les bateaux adverses ont été coulés"""
        return sorted(self.player.find_coor(".")) != sorted(self.figther.find_not_coor(" "))

    def victory(self: Self) -> None:
        """affiche la victoire du joueur"""
        print(f"victoire {self.player.alias} !!!!!!")
