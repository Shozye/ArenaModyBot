import Controler
from Controler import Controler
import logging


def main():
    """
Type your login, password, driver_path and character name to respective places
to use methods connected to fight, you first have to findEnemies()
    """
    user = 'Kurowa'
    password = 'kolec123'
    driver_path = r'C:\Users\Rodzice.Mateusz-PC\Desktop\PythonProjects\ArenaModyBot\chromedriver.exe'  # it should be raw string
    level = logging.DEBUG  # logging.DEBUG or logging.INFO
    character_name = 'Kurowa'
    lowerbound_attack = 1000
    control_panel = Controler(user, password, driver_path, level, character_name,
                              lowerbound_attack=lowerbound_attack)  # NOT INTERESTED
    #control_panel.gather_emeralds()
    #control_panel.find_enemies()
    control_panel.gather_emerald_and_fight()


if __name__ == '__main__':
    main()
