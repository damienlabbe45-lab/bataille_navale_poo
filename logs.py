"""fichier pour le système des erreurs. tout a été fait au départ
dans mon projet personnel. mais c'est juste adapté ici. c'est surtout pour avoir
l'affichage des erreurs sur console et sur fichoier en même temps et en fr avec les
microsecondes."""

from logging import Formatter
from typing import Self


class FormatDate(Formatter):
    """Formateur personnalisé pour utiliser la fonction date() pour l'horodatage."""

    def formatTime(self: Self, record, datefmt=None):
        """
        Retourne la chaîne de date/heure personnalisée.
        """
        from datetime import datetime
        maintenant = datetime.now()
        return maintenant.strftime("%d %B %Y à %H heure %M minutes %S secondes %f microsecondes").replace(
            m := maintenant.strftime("%B"),
            {'January': 'janvier', 'February': 'février', 'March': 'mars', 'April': 'avril', 'May': 'mai',
             'June': 'juin',
             'July': 'juillet', 'August': 'août', 'September': 'septembre', 'October': 'octobre',
             'November': 'novembre', 'December': 'décembre'}[m])


class LogErreur(object):
    """Mixin pour initialiser le système de logging (uniquement les erreurs)."""

    def loggingbattleship(self: Self):
        """Configure le logging pour afficher uniquement les erreurs dans la console et un fichier."""
        from logging import getLogger, DEBUG, WARNING
        import sys
        from sys import stdout
        from pathlib import Path
        stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)
        LOG_FILENAME = Path(__file__).resolve().parents[0] / 'log_battleship.log'
        # Utilisation du Formateur
        CUSTOM_FORMETTER = FormatDate(
            fmt='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        root_logger = getLogger()
        # Vérifie si la configuration n'a pas déjà été faite
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        if not root_logger.handlers:
            from logging import StreamHandler, FileHandler

            class UnbufferedStreamHandler(StreamHandler):
                """Handler console qui force l'affichage immédiat à chaque ligne."""

                def emit(self, record):
                    super().emit(record)
                    self.flush()

            class UnbufferedFileHandler(FileHandler):
                """Handler fichier qui force l'écriture sur le disque à chaque ligne."""

                def emit(self, record):
                    super().emit(record)
                    self.flush()

                # 1. Gestionnaire pour la console (StreamHandler)

            console_handler = UnbufferedStreamHandler(stdout)
            console_handler.setLevel(WARNING)
            console_handler.setFormatter(CUSTOM_FORMETTER)
            # gestionnaire pour le fichier
            file_handler = UnbufferedFileHandler(
                LOG_FILENAME, encoding='utf-8')
            file_handler.setLevel(WARNING)
            file_handler.setFormatter(CUSTOM_FORMETTER)

            root_logger.setLevel(DEBUG)
            root_logger.addHandler(console_handler)
            root_logger.addHandler(file_handler)

        def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
            import sys
            # Permet de laisser le Ctrl+C couper le proggramme normalement sans polluer
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                # Envoie le crash directement dans le root_logger (donc écran + fichier log)
                return root_logger.error("Crash fatal détecté (Hors-Log) :",
                                         exc_info=(exc_type, exc_value, exc_traceback))
                # On remplace l'intercepteur par défaut de Python par le nôtre

        sys.excepthook = handle_unhandled_exception
