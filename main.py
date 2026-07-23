from classe_jeu import BatlleshipGame
from secrets import choice


def input_playeurs() -> int:
    user = ""
    liste_number_str = [str(i) for i in range(3)]
    while isinstance(user, str):
        user = input("Veillez entre le nombre de joueur (entre 0 et 2 inclus")
        if user in liste_number_str:
            return int(user)

def preparations_battle() -> list[BatlleshipGame]:
    nb_playeur = input_playeurs()
    list_playeur: list[str] = []
    for _ in range(nb_playeur):
        list_playeur.append(input("entre un nom"))

    for i in range(2 - nb_playeur):
        list_playeur.append(f"\n{i}")

    ships_names: list[str] = ["Jupiter", "Zeus", "Aphrodite", "Vénus", "Marth", "Lucina", "Mars", "Arès", "Hades",
                              "Pluton", "Anubis", "Ra", "Mercure", "Hermès", "Athéna", "Minerve", "Minerva", "Corrin",
                              "Byleth", "Bastet", "Thor", "Odin", "Grima", "Corren", "Casper", "Pill", "Halt", "Treaty",
                              "Oblige", "Seth", "Théménos", "Cyrus", "Hephaïstos", "Cupidon", "Zorro", "Lefantôme"]
    playeurs: list[BatlleshipGame] = []

    for playeur in range(2):
        ships_playeur: list[str] = []
        for _ in range(5):
            ship = choice(ships_names)
            ships_playeur.append(ship)
            ships_names.remove(ship)

        playeurs.append(BatlleshipGame(list_playeur[playeur], ships_playeur, list_playeur[playeur - 1]))

    return playeurs


def battle_game(playeurs: list[BatlleshipGame]) -> None:
    i = choice([0, 1])

    while playeurs[i % 2].if_victory():
        playeur = playeurs[i % 2]
        print(f" c'est à vous {playeur.playeur.alias}")
        print(playeur.playeur.map_battle)

        if "\n" in playeur.playeur.name:
            playeur.choice_computer()

        else:
            playeur.choice_human()

        i += 1

    playeurs[(i + 1) % 2].victory()


def main() -> None:
    battle_game(preparations_battle())


if __name__ == "__main__":
    main()

