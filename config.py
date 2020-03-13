import Controler
from Controler import Controler
import logging


def main():
    """
    Type username, password, path to chromedriver.exe, for bot to login
    character_name is variable used to operate with checked_enemies and enemy_list,
    If you want to create new enemy_list, for example, for different character
    change it
    lowerbound_attack: Bot will prefer to attack characters he attacked before if and only if
    money_he_got_from_enemy > lowerbound_attack
    level_treshold - used to process checked_enemies and enemy_list
    level difference between you and enemies you want to attack

    To use Bot use one of commented methods started by control_panel.[method]()
    """
    user = 'my-username'
    password = 'my-password'
    driver_path = r'my-path-to-chromedriver.exe'  # raw string
    level = logging.DEBUG  # logging.DEBUG or logging.INFO
    character_name = 'my-character-name'
    lowerbound_attack = 2800
    level_treshold = 10
    control_panel = Controler(user, password, driver_path, level, character_name,
                              lowerbound_attack=lowerbound_attack, level_treshold=level_treshold)  # NOT INTERESTED
    '''
    Use methods below
    '''
    # control_panel.gather_emeralds()
    # control_panel.find_enemies()
    # control_panel.gather_emerald_and_fight()
    control_panel.fight()
    #control_panel.recheck_checked_characters()
    #control_panel.recheck_enemy_list()


if __name__ == '__main__':
    main()
