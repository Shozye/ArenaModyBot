import Controler
from Controler import Controler
import logging


def main():
    """
Type your login, password, driver_path and character name to respective places
to use methods connected to fight, you first have to findEnemies()
    """
    user = ''
    password = ''
    driver_path = r''   # it should be raw string
    level = logging.DEBUG
    character_name = ''
    control_panel = Controler(user, password, driver_path, level, character_name)
    control_panel.gather_emerald_and_fight()


if __name__ == '__main__':
    main()
