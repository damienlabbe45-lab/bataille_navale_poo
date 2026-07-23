from classe_jeu import BatlleshipGame
from secrets import choice


def input_playeurs() -> int:
    user = ""
    liste_number_str = [str(i) for i in range(3)]
    while isinstance(user, str):
        user = input("Veillez entre le nombre de joueur (entre 0 et 2 inclus")
        if user in liste_number_str:
            return int(user)


