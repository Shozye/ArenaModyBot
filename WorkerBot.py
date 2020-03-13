from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from time import time
import json
import os.path
import selenium
import logging
from selectors import init_selectors
from Bot import Bot
from time import sleep


class WorkerBot(Bot):
    """
    This class should be used to play: gather emeralds and fight in a long run
    """
    def __init__(self, browser, character_name, lowerbound_attack=1000):
        super(WorkerBot, self).__init__(browser, character_name)
        self.lowerBoundOfAttack = lowerbound_attack
        self.arena_site = 'https://g.arenamody.pl/duels.php'
        self.jobs_site = 'https://g.arenamody.pl/jobs.php'

    def make_emerald_action(self, hard=False):
        """
        It is unit emerald action.
        It will
        - click to start photoSession
        - click to stop photoSession (and gather emerald)
        - if hard == True if will wait till end of photoSession
        :param hard: if param == hard, then Bot will wait when the PhotoSession is making
        """
        if self.browser.current_url != self.jobs_site:
            self.browser.get(self.jobs_site)
            logging.info('Changing site to jobs')
        start_emerald = self.browser.find_elements_by_css_selector(self.selectors['startEmerald'])[0]
        try_emerald = self.browser.find_elements_by_css_selector(self.selectors['tryEmerald'])[0]
        popup_emerald = self.browser.find_elements_by_css_selector(self.selectors['popUpEmerald'])[0]
        stop_emerald = self.browser.find_elements_by_css_selector(self.selectors['stopEmerald'])[0]
        if start_emerald.is_displayed():
            logging.info('Start Emerald Click')
            start_emerald.click()
            WebDriverWait(self.browser, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, self.selectors['stopEmerald'])))
        elif stop_emerald.is_displayed():
            logging.info('Photo session is in progress')
            if hard:
                logging.info('Wait for photo session end')
                try:
                    WebDriverWait(self.browser, 1800).until(
                        ec.visibility_of_element_located((By.ID, self.ids['photoSessionIndicator'])))
                except selenium.common.exceptions.TimeoutException:
                    self.browser.refresh()
                    logging.info('selenium.common.exceptions.TimeoutException called in stop_emerald.is_displayed()')
            self.browser.refresh()
            pass
        elif try_emerald.is_displayed():
            logging.info('Trying to get emerald action is executed')
            try_emerald.click()
            emeralds_info = self.browser.find_elements_by_css_selector(self.selectors['amOfEmeralds'])
            if len(emeralds_info) == 0:
                logging.info('You have not taken emerald')
            else:
                self.emeraldTaken += int(emeralds_info[0].text)
                logging.info(
                    'You have acquired ' + emeralds_info[0].text + ' emeralds. That\'s ' + str(self.emeraldTaken) +
                    'in total')
            popup_emerald.click()
        else:
            raise Exception('Bot should be on jobs site, but perhaps he isn\'t')

    def attack_choose(self):
        """
        :return: return id of enemy to attack in string
        """
        enemies = list(self.enemy_list.items())
        enemies.sort(key=lambda x: x[1][0], reverse=True)
        for item in enemies:
            if time() - item[1][1] > 3600:
                logging.info(json.dumps(item[0]))
                return item[0]

        raise Exception('EnemyList is empty')

    def attack(self, enemy_id):
        """
        It will attack character with given ID,
        and then update enemy_list
        :param enemy_id: id to attack
        """
        money_before = self.update_money(ret=True)
        self.browser.get(self.profile_start_site + enemy_id)
        if (int(self.browser.find_element_by_class_name(self.classes['enemyLevel']).text.split(' ')[1]) >=
                self.stats['level']):
            self.enemy_list[enemy_id] = (-100000, time())
            self.save_enemy_list()
        else:
            self.retry_click(By.CSS_SELECTOR, self.selectors['challengeFromProfile'])
            WebDriverWait(self.browser, 20).until(
                ec.element_to_be_clickable((By.ID, self.ids['challenge'])))
            sleep(3)
            self.retry_click(By.ID, self.ids['challenge'])

            succeed = False
            for attempt in range(10):
                print('refreshed')
                money_after = self.update_money(ret=True)
                if money_after == money_before:
                    self.browser.refresh()
                else:
                    succeed = True
                    break
            if succeed:
                money_change = money_after - money_before
                print(money_after, money_before, money_change)
                self.enemy_list[enemy_id] = (money_change - self.lowerBoundOfAttack, time())
                self.save_enemy_list()
            else:
                print('Enemy has been attacked or i have attacked him 5 times')
                self.enemy_list[enemy_id] = (self.enemy_list[enemy_id][0], 86400 + time())
