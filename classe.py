from pandas import DataFrame
from logs import LogErreur
from typing import Self, Any


class Seabattle(DataFrame, LogErreur):
    def __init__(self: Self, name: str) -> None:
        from string import ascii_uppercase
        self.map_battle = DataFrame(data=" ", index=range(1, 11), columns=list(ascii_uppercase[:10]))
        self.loggingbattleship()
        self.name: str = name
        if "/n" in self.name:
            self.alias = "Ordinateur " + self.name[2:]
        else:
            self.alias = self.name

    def find_coor(self: Self, text: str) -> list[tuple[int, str]]:
        """donne les coordonnées ayant les valeurs de la chaîne"""
        return [
            (row, col) for row in range(1, 11) for col in "ABCDEFGHIJ" if
            row in self.map_battle.index and col in self.map_battle.columns and
            self.map_battle.loc[row, col] == text]

    def find_not_coor(self: Self, text: str) -> list[tuple[int, str]]:
        """donne les coordonnées n'ayant pas la valeur de la chaîne"""
        return [
            (row, col) for row in range(1, 11) for col in "ABCDEFGHIJ" if
            row in self.map_battle.index and col in self.map_battle.columns and
            self.map_battle.loc[row, col] != text]

    def assign_value(self: Self, coor: list[tuple[int, str]], value: str) -> None:
        """met la valeur à toutes les coordonnées dans le dataframe"""
        for row, col in coor:
            if row in self.map_battle.index and col in self.map_battle.columns:
                self.map_battle.loc[row, col] = value


class Ship:
    def __init__(self: Self, name: str, coor: list[tuple[int, str]]) -> None:
        self.name = name
        self.coor = coor

    def ship_touch(self: Self, coor: tuple[Any, Any]) -> None:
        if coor in self.coor:
            print(f"{self.name} a été touché")
            self.coor.remove(coor)
        if len(self.coor) == 0:
            print(f"{self.name} a été coulé")


class Matrixbatlleship(Seabattle):
    def __init__(self: Self, name: str, list_ships: list[str]) -> None:
        super().__init__(name)
        self.list_Ships: list[Ship] = []
        length_ship = [2, 3, 3, 4, 4, 5]
        list_dir = ["haut", "bas", "droite", "gauche"]
        from secrets import choice
        for i, ship in enumerate(list_ships):
            length = length_ship[i]
            coor = self.find_coor("")
            coords_dangerous = self.find_not_coor("")
            coor = self.verify_coor(coor, coords_dangerous, 3)
            list_ship = list_dir[:]
            choose_dir = choice(list_ship)
            if "/n" in self.name:
                coor_value = choice(coor)
                coor_values = self.append_coor(coor_value, coords_dangerous, choose_dir, length - 1)
            else:
                coor_value = self.input_coor(coor)
                coor_values = self.append_coor(coor_value, coords_dangerous, choose_dir, length - 1)
            self.assign_value(coor_values, str(length))
            self.list_Ships.append(Ship(name=ship, coor=coor_values))

    def append_coor(self: Self, coor: tuple[int, str], coors_dangerous: list[tuple[int, str]], direction: str,
                    number: int) -> list[tuple[int, str]]:
        """Prend toutes les coordonnées d'un bateau en fonction de sa taille sans jamais la modifier"""
        dict_string_number = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10}
        cols_letter = list(dict_string_number.keys())
        start_row, start_col = coor[0], coor[1]
        start_col_idx = cols_letter.index(start_col)
        test_direction = [direction] + [d for d in ["droite", "gauche", "haut", "bas"] if d != direction]
        for d in test_direction:
            candidate_path = [coor]
            is_validate: bool = True
            for i in range(1, number + 1):
                if d == "droite":
                    next_row = start_row
                    next_col_idx = start_col_idx + i
                elif d == "gauche":
                    next_row = start_row
                    next_col_idx = start_col_idx - i
                elif d == "bas":
                    next_row = start_row + i
                    next_col_idx = start_col_idx
                elif d == "haut":
                    next_row = start_row - i
                    next_col_idx = start_col_idx
                if next_row < 1 or next_row > 10 or next_col_idx < 0 or next_col_idx >= 10:
                    is_validate = False
                    break
                next_coor = (next_row, cols_letter[next_col_idx])
                if next_coor in coors_dangerous:
                    is_validate = False
                    break
                candidate_path.append(next_coor)
            if is_validate:
                return candidate_path

    def verify_coor(self: Self, coor: list[tuple[int, str]], coors_dangerous: list[tuple[int, str]], number: int
                    ) -> list[tuple[int, str]]:
        """filtre les coordonnées donnant à des situtations impossibles à résoudre"""
        dict_string_number = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10}
        cols_letter = list(dict_string_number.keys())
        valid_coor = []
        for coords in coor:
            col: str = coords[1]
            row: int = coords[0]
            col_num = dict_string_number[col]
            ok_rigth = (col_num + number - 1 <= 10) and all((row, cols_letter[col_num + i - 1]) not in
                                                            coors_dangerous for i in range(number))
            ok_left = (col_num - number + 1 >= 1) and all(
                (row, cols_letter[col_num - i - 1]) not in coors_dangerous for i
                in range(number))
            ok_bottom = (row + number - 1 <= 10) and all((row - i, col) not in coors_dangerous for i in range(number))
            ok_top = (row - number + 1 >= 1) and all((row - i, col) not in coors_dangerous for i in range(number))
            if ok_bottom or ok_left or ok_rigth or ok_top:
                valid_coor.append((row, col))
        return valid_coor

    def input_coor(self: Self, coor: list[tuple[int, str]]) -> tuple[int, str]:
        """demande à l'utilisateur les coordonnées pour mettre un bateau"""
        user_col = ""
        cols = [cols[1] for cols in coor]
        while user_col not in cols:
            user_col = input(f"Veillez donner le nom d'une colonne parmis celles-ci {', '.join(col for col in cols)}")
        rows = [str(row[0]) for row in coor if user_col == row[0]]
        user_row = ""
        while user_row not in rows:
            user_col = input(f"Veillez donner le numéro d'une ligne parmis celles-ci {', '.join(row for row in rows)}")
        return int(user_row), user_col
