from selenium import webdriver
from WorkerBot import WorkerBot
from FindEnemiesBot import FindEnemiesBot
import logging


class Controler:
    def __init__(self, user, password, driver_path, level, character_name):
        self.DRIVER_PATH = driver_path
        self.PASS = password
        self.USER = user
        self.LEVEL = level
        self.character_name = character_name

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
        browser = webdriver.Chrome(self.DRIVER_PATH)
        bot = WorkerBot(browser, self.character_name)
        bot.start_bot()
        bot.login(self.USER, self.PASS)
        logging.info('Bot has logged properly')
        while True:
            logging.info('Play Loop Executed')
            bot.update_status()
            if not bot.emeraldAction and bot.energyAmount > 0:
                bot.attack(bot.attack_choose())
            bot.make_emerald_action(hard=True)

    def fight(self):
        browser = webdriver.Chrome(self.DRIVER_PATH)
        bot = WorkerBot(browser, self.character_name)
        bot.start_bot()
        bot.login(self.USER, self.PASS)
        logging.info('Bot has logged properly')
        while True:
            logging.info('Play Loop Executed')
            bot.update_status()
            if not bot.emeraldAction and bot.energyAmount > 0:
                bot.attack(bot.attack_choose())

    def find_enemies(self):
        browser = webdriver.Chrome(self.DRIVER_PATH)
        bot = FindEnemiesBot(browser, self.character_name)
        bot.start_bot()
        bot.login(self.USER, self.PASS)
        logging.info('Bot has logged properly')

        bot.gather_potential_enemies()
        bot.check_potential_players()

