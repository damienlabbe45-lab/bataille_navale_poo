from classe_jeu import BatlleshipGame
from secrets import choice


def input_playeurs(number: int, text: str) -> int:
    """permet de savoir le nombre de joueurs"""
    user = ""
    liste_number_str = [str(i) for i in range(number)]
    while isinstance(user, str):
        user = input(text)
        if user in liste_number_str:
            user= int(user)
    return user


def preparations_battle() -> list[BatlleshipGame]:
    """préparatifs pour faire la bataille navale"""
    nb_playeur = input_playeurs(3, "Veillez entre le nombre de joueur (entre 0 et 2 inclus)\n")
    list_playeur: list[str] = []
    for _ in range(nb_playeur):
        list_playeur.append(input("entre un nom"))

    for i in range(2 - nb_playeur):
        list_playeur.append(f"\n{i}")

    ships_names: list[str] = ["Jupiter", "Zeus", "Aphrodite", "Vénus", "Marth", "Lucina", "Mars", "Arès", "Hades",
                              "Pluton", "Anubis", "Ra", "Mercure", "Hermès", "Athéna", "Minerve", "Minerva", "Corrin",
                              "Byleth", "Bastet", "Thor", "Odin", "Grima", "Corren", "Casper", "Oscar", "Pill", "Halt",
                              "Treaty", "Oblige", "Seth", "Théménos", "Cyrus", "Hephaïstos", "Cupidon", "Zorro",
                              "Lefantôme", "Xana", "Harry", "Potter", "Tsuki", "Onyx", "Wellan", "Nashoba", "Aelita",
                              "Rhea", "Jaden", "Yugi", "Tincel", "Einstein", "Anankos", "Flamel", "Daraen", "Ike",
                              "Vulcain", "Demeter", "Ceres", "Teal'c", "Carter", "Sephiroth", "Owain", "Jack", 
                              "Harikeñ", "Catasfiore", "Vaan", "Balthier", "Agnès", "Casty", "Osvald", "Muriel",
                              "Anatiel", "Zéphilia", "Tamriel", "Wuunferth", "Yann", "Aucun", "Stole", "Arthur",
                              "Apollon", "Diane", "Artemis", "Dianthus", "Jedusort", "William", "Ulrich", "Joséphiroth"
                              , "Jim", "Morales", "Makoto", "Naegi", "Celica", "Yuri", "Moon", "Bernadetta", "Seiros"]
    playeurs: list[BatlleshipGame] = []
    nb_navire = input_playeurs(9, "Indiquez combien de navire vous voulez(entre 0 et 8 inclus)")
    for playeur in range(2):
        ships_playeur: list[str] = []
        for _ in range(nb_navire):
            ship = choice(ships_names)
            ships_playeur.append(ship)
            ships_names.remove(ship)
        playeurs.append(BatlleshipGame(list_playeur[playeur], ships_playeur, list_playeur[playeur - 1]))
    return playeurs


def battle_game(playeurs: list[BatlleshipGame]) -> None:
    """programme pour faire la bataille navale"""
    i = choice([0, 1])
    while playeurs[i % 2].if_victory():

        playeur = playeurs[i % 2]
        print(f" c'est à vous {playeur.player.alias}")
        playeur.touch_ship()
        i += 1

    playeurs[(i + 1) % 2].victory()


def main() -> None:
    """fonction principale du programme"""
    battle_game(preparations_battle())


if __name__ == "__main__":
    main()
