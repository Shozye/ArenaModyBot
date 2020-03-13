from selenium import webdriver
from WorkerBot import WorkerBot
from FindEnemiesBot import FindEnemiesBot
from random import random
import logging


class Controler:
    '''
    This class is used as easy control panel
    the methods here should be only commands needed to bot for proper functioning
    if method ends, bot also should end
    These methods should be called in config.py
    '''

    def __init__(self, user, password, driver_path, level, character_name, lowerbound_attack=None, level_treshold=None):
        self.lowerBoundOfAttack = lowerbound_attack
        self.DRIVER_PATH = driver_path
        self.PASS = password
        self.USER = user
        self.LEVEL = level
        self.character_name = character_name
        self.level_treshold = level_treshold

        logging.basicConfig(filename='16.02.2020.log', level=self.LEVEL,
                            format='%(levelname)s:%(asctime)s:%(message)s')

    def gather_emeralds(self):
        browser = webdriver.Chrome(self.DRIVER_PATH)
        bot = WorkerBot(browser, self.character_name)
        bot.start_bot()
        bot.login(self.USER, self.PASS)
        logging.info('Bot has logged properly')
        while True:
            logging.info('Play Loop Executed')
            bot.make_emerald_action(hard=True)
            bot.update_status()

    def gather_emerald_and_fight(self):
        '''
        To fight, there has to be created enemy list
        by using find_enemies method
        '''
        browser = webdriver.Chrome(self.DRIVER_PATH)
        bot = WorkerBot(browser, self.character_name, lowerbound_attack=self.lowerBoundOfAttack)
        bot.start_bot()
        bot.login(self.USER, self.PASS)
        logging.info('Bot has logged properly')
        while True:
            logging.info('Play Loop Executed')
            bot.update_status()
            if not bot.emeraldAction and bot.energyAmount > 0:
                bot.attack(bot.attack_choose())
            if not bot.emeraldAction and bot.energyAmount > 0 and random() > 0.5:
                bot.attack(bot.attack_choose())
            bot.make_emerald_action(hard=True)

    def fight(self):
        '''
        To fight, there has to be created enemy list
        by using find_enemies method
        '''
        browser = webdriver.Chrome(self.DRIVER_PATH)
        bot = WorkerBot(browser, self.character_name, lowerbound_attack=self.lowerBoundOfAttack)
        bot.start_bot()
        bot.login(self.USER, self.PASS)
        logging.info('Bot has logged properly')
        while True:
            logging.info('Play Loop Executed')
            bot.update_status()
            if not bot.emeraldAction and bot.energyAmount > 0:
                bot.attack(bot.attack_choose())
            else:
                logging.info('Cant attack anymore')
                break

    def find_enemies(self):
        browser = webdriver.Chrome(self.DRIVER_PATH)
        bot = FindEnemiesBot(browser, self.character_name, self.level_treshold)
        bot.start_bot()
        bot.login(self.USER, self.PASS)
        logging.info('Bot has logged properly')

        bot.gather_potential_enemies()
        bot.check_potential_players()

    def recheck_checked_characters(self):
        browser = webdriver.Chrome(self.DRIVER_PATH)
        bot = FindEnemiesBot(browser, self.character_name, self.level_treshold)
        bot.start_bot()
        bot.login(self.USER, self.PASS)
        logging.info('Bot has logged properly')

        bot.recheck_people_from_checked_list()

    def recheck_enemy_list(self):
        browser = webdriver.Chrome(self.DRIVER_PATH)
        bot = FindEnemiesBot(browser, self.character_name, self.level_treshold)
        bot.start_bot()
        bot.login(self.USER, self.PASS)
        logging.info('Bot has logged properly')

        bot.recheck_people_from_enemy_list()
