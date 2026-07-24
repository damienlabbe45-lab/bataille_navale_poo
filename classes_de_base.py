from pandas import DataFrame
from logs import LogErreur
from typing import Self


class Seabattle(LogErreur):
    """classe pour faire la grille des coups des joueurs ou des ordinateurs"""
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
    """classe des bateaux"""
    def __init__(self: Self, name: str, coor: list[tuple[int, str]]) -> None:
        from secrets import SystemRandom
        self.name = name
        self.coor = coor
        self.shot = SystemRandom().randint(0, 2)

    def ship_touch(self: Self, coor: tuple[int, str]) -> int:
        """permet de savoir si le navire a été touché ou coulé"""
        if coor in self.coor:
            print(f"{self.name} a été touché")
            self.coor.remove(coor)
        if len(self.coor) == 0:
            print(f"{self.name} a été coulé")
        return 0 if len(self.coor) != 0 else self.shot
