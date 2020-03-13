from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from time import time
import json
import os.path
import selenium
import logging
from selectors import init_selectors


class Bot:
    browser: webdriver.Chrome
    '''
    This class is base for other bots
    every other bot needs to have these functions 
    '''

    def __init__(self, browser, character_name):
        self.browser = browser
        self.character_name = character_name
        self.browser.implicitly_wait(20)
        self.start_site = 'https://www.arenamody.pl'
        self.profile_start_site = 'https://g.arenamody.pl/profile.php?id='
        self.energyAmount = None
        self.emeraldTaken = 0
        self.emeraldAction = False
        self.emeraldToTake = False
        _selectors = init_selectors()
        self.ids = _selectors['ids']
        self.names = _selectors['names']
        self.selectors = _selectors['selectors']
        self.classes = _selectors['classes']
        self.enemy_list = self.initialize_enemy_list()
        self.money = 0
        self.stats = dict()
        logging.info('Bot has initialized properly')

    def save_enemy_list(self):
        """
        saves enemy_list to file
        """
        filename = self.character_name + "_enemy_list.txt"
        with open(filename, 'w') as file:
            json.dump(self.enemy_list, file)

    def initialize_enemy_list(self):
        filename = self.character_name + "_enemy_list.txt"
        if os.path.isfile(filename):
            with open(filename) as file:
                enemy_list = json.load(file)
        else:
            enemy_list = dict()
        return enemy_list

    def retry_click(self, by, value):
        """
        it will click continuosly on the object till click will work specified by (by,value) pair
        :param by: By.(ID/SELECTOR/CLASS/ETC.)
        :param value: id/selector/class/etc specified in by
        :return:
        """
        result = False
        for attempt in range(50):
            try:
                web_element = self.browser.find_element(by, value)
                web_element.click()
                result = True
                break
            except selenium.common.exceptions.StaleElementReferenceException:
                logging.debug('selenium.common.exceptions.StaleElementReferenceException occurred')
                pass
        if not result:
            raise Exception('selenium.common.exceptions.StaleElementReferenceException occurred')

    def click_cookies_button(self):
        result = False
        for attempt in range(50):
            try:
                web_element = self.browser.find_element(By.CSS_SELECTOR, self.selectors['cookiesbutton'])
                web_element.click()
                result = True
                break
            except selenium.common.exceptions.ElementClickInterceptedException:
                logging.debug('selenium.common.exceptions.ElementCLickInterceptedException occurred')
                pass
        # It is only used to cookiesbutton

    def start_bot(self):
        self.browser.get(self.start_site)

    def login(self, username, password):
        """
        It controls every action till properly login
        :param username: username needed to login
        :param password: password needed to login
        """
        login_button = self.browser.find_element_by_id(self.ids['login_button'])
        user_field = self.browser.find_element_by_name(self.names['username'])
        pass_field = self.browser.find_element_by_name(self.names['password'])
        submit_button = self.browser.find_element_by_id(self.ids['login_submit'])
        wait = WebDriverWait(self.browser, 10)
        self.click_cookies_button()
        wait.until(ec.element_to_be_clickable((By.ID, self.ids['login_button'])))

        login_button.click()
        try:
            user_field.send_keys(username)
            pass_field.send_keys(password)
            submit_button.click()
        except selenium.common.exceptions.ElementNotInteractableException:
            login_button.click()
            user_field.send_keys(username)
            pass_field.send_keys(password)
            submit_button.click()
            logging.info('Bot has logged in after ElementNotInteractableException')

        wait.until(ec.title_contains('Arena Mody'))
        self.browser.refresh()

        logging.info('Browser refreshed after login')
        self.click_cookies_button()
        try:
            self.stats = self.init_stats()
        except selenium.common.exceptions.ElementClickInterceptedException:
            self.browser.refresh()
            self.stats = self.init_stats()

    def update_status(self):
        """
        Updates money, energy, and if emerald is making
        :return:
        """
        self.browser.refresh()
        self.update_money()
        energy_span = self.browser.find_element_by_id(self.ids['ladyEnergy'])
        self.energyAmount = int(energy_span.text)
        logging.info('There is ' + energy_span.text + ' energy.')
        try:
            photo_session_timer = self.browser.find_element_by_id(self.ids['photoSessionTimer'])
            photo_session_indicator = self.browser.find_element_by_id(self.ids['photoSessionIndicator'])
            if photo_session_timer.is_displayed():
                self.emeraldAction = True
                self.emeraldToTake = False
            elif photo_session_indicator.is_displayed():
                self.emeraldAction = True
                self.emeraldToTake = True
            else:
                self.emeraldAction = False
                self.emeraldToTake = False
        except selenium.common.exceptions.NoSuchElementException:
            logging.warning('selenium.common.exceptions.NoSuchElementException occurred')
        except selenium.common.exceptions.StaleElementReferenceException:
            logging.warning('selenium.common.exceptions.StaleElementReferenceException occured')
            photo_session_timer = self.browser.find_element_by_id(self.ids['photoSessionTimer'])
            photo_session_indicator = self.browser.find_element_by_id(self.ids['photoSessionIndicator'])
            if photo_session_timer.is_displayed():
                self.emeraldAction = True
                self.emeraldToTake = False
            elif photo_session_indicator.is_displayed():
                self.emeraldAction = True
                self.emeraldToTake = True
            else:
                self.emeraldAction = False
                self.emeraldToTake = False

    def update_money(self, ret=False):
        """
        :param ret: True/False
        :return: Integer
        """
        money = self.browser.find_element_by_id(self.ids['dollars']).text
        money = int(money.replace(',', ""))
        self.money = money
        if ret:
            return money

    def init_stats(self):
        """
        :return: dict object with my stats
        """
        self.retry_click(By.CLASS_NAME, self.classes['popularityButton'])
        logging.debug('level ' + self.browser.find_element_by_id(self.ids['currentLevel']).text)
        logging.debug('style ' + self.browser.find_element_by_id(self.ids['myStyle']).text)
        logging.debug('creativity ' + self.browser.find_element_by_id(self.ids['myCreativity']).text)
        logging.debug('devotion ' + self.browser.find_element_by_id(self.ids['myDevotion']).text)
        logging.debug('generosity ' + self.browser.find_element_by_id(self.ids['myGenerosity']).text)
        logging.debug('loyalty ' + self.browser.find_element_by_id(self.ids['myLoyalty']).text)
        stats = {
            'level': int(self.browser.find_element_by_id(self.ids['currentLevel']).text),
            'style': int(self.browser.find_element_by_id(self.ids['myStyle']).text),
            'creativity': int(self.browser.find_element_by_id(self.ids['myCreativity']).text),
            'devotion': int(self.browser.find_element_by_id(self.ids['myDevotion']).text),
            'beauty': int(self.browser.find_element_by_id(self.ids['myBeauty']).text),
            'generosity': int(self.browser.find_element_by_id(self.ids['myGenerosity']).text),
            'loyalty': int(self.browser.find_element_by_id(self.ids['myLoyalty']).text)
        }
        return stats
