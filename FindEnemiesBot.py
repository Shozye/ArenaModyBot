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
from Bot import Bot


class FindEnemiesBot(Bot):
    """
    This class should be used to process, change and create good enemy_list
    """
    def __init__(self, browser, character_name, level_treshold):
        super(FindEnemiesBot, self).__init__(browser, character_name)
        self.ranking_site = 'https://g.arenamody.pl/ranking.php'
        self.potential_enemies = set()
        self.checked_enemies = self.initialize_checked_enemies()
        self.level_treshold = level_treshold

    def save_checked_enemies(self):
        """
        saving checked_enemies to file
        """
        filename = self.character_name + "_checked_enemies.txt"
        with open(filename, 'w') as file:
            json.dump(self.checked_enemies, file)

    def initialize_checked_enemies(self):
        """
        loading checked_enemies from file
        """
        filename = self.character_name + "_checked_enemies.txt"
        if os.path.isfile(filename):
            with open(filename) as file:
                checked_enemies = json.load(file)
        else:
            checked_enemies = list()
        return checked_enemies

    def gather_potential_enemies_from(self, tab):
        """
        the function takes enemies from ranking
        :param tab: the tab in the ranking, from which I want to gather potential enemies
        """
        if self.browser.current_url != self.ranking_site:
            self.browser.get(self.ranking_site)
        self.browser.execute_script("getRanking(currentType, '" + tab + "')")
        for i in range(1, 21):
            self.browser.execute_script("getRanking('daily','" + tab + "' ," + str(i) + ")")
            try:
                WebDriverWait(self.browser, 10).until(ec.element_to_be_clickable((By.ID, "N" + str(20 * i - 19))))
            except selenium.common.exceptions.StaleElementReferenceException:
                pass
            for attempt in range(10):
                succeed = False
                try:
                    ids = self.browser.find_elements_by_css_selector('td>a.player-name')
                    ids = list(map(lambda x: x.get_attribute('href'), ids))
                    ids = set(map(lambda x: x.split('=')[1], ids))
                    succeed = True
                    break
                except selenium.common.exceptions.StaleElementReferenceException:
                    pass
            if succeed:
                self.potential_enemies = self.potential_enemies | ids
                logging.debug('Succeed in attempt ' + str(attempt))
            else:
                raise Exception('selenium.common.exceptions.StaleElementReferenceException')
        # print(list(self.potential_enemies))

    def gather_potential_enemies(self):
        """
        this function gathers processes potential enemies to avoid checking the same person twice
        :return:
        """
        self.gather_potential_enemies_from('exp')
        self.gather_potential_enemies_from('duels_won')
        self.gather_potential_enemies_from('duels_money_won')
        to_del = []
        for potential_enemy in self.potential_enemies:
            if potential_enemy in self.enemy_list.keys() or potential_enemy in self.checked_enemies:
                to_del.append(potential_enemy)
        for todel in to_del:
            self.potential_enemies.remove(todel)

    def check_player(self, player_id):
        """
        checks if I have higher stats than enemy
        :param player_id: string
        :return: True if I can attack this person and win else False
        """
        self.browser.get(self.profile_start_site + str(player_id))
        enemy_stats = {
            'level': int(self.browser.find_element_by_class_name(self.classes['enemyLevel']).text.split(' ')[1]),
            'style': int(self.browser.find_element_by_css_selector(self.selectors['enemyStyle']).text),
            'creativity': int(self.browser.find_element_by_css_selector(self.selectors['enemyCreativity']).text),
            'devotion': int(self.browser.find_element_by_css_selector(self.selectors['enemyDevotion']).text),
            'beauty': int(self.browser.find_element_by_css_selector(self.selectors['enemyBeauty']).text),
            'generosity': int(self.browser.find_element_by_css_selector(self.selectors['enemyGenerosity']).text),
            'loyalty': int(self.browser.find_element_by_css_selector(self.selectors['enemyLoyalty']).text)
        }
        logging.debug('enemylevel ' + self.browser.find_element_by_class_name(self.classes['enemyLevel']).text)
        logging.debug(self.stats['level'])
        logging.debug(enemy_stats['level'])
        if (self.stats['level'] > enemy_stats['level'] >= self.stats['level'] - self.level_treshold and
                self.stats['style'] > enemy_stats['style'] and
                self.stats['creativity'] > enemy_stats['creativity'] and
                self.stats['devotion'] > enemy_stats['devotion'] and
                self.stats['beauty'] > enemy_stats['beauty'] and
                self.stats['generosity'] > enemy_stats['generosity']):
            return True
        else:
            return False
    def check_potential_players(self):
        """
        checks every person from previously gathered list of potential players
        if the function check_player() returns True
        if yes, then append this person to enemy_list
        """
        for enemy_id in self.potential_enemies:
            if self.check_player(enemy_id):
                self.enemy_list[enemy_id] = [0,0]
                self.save_enemy_list()
            else:
                self.checked_enemies.append(enemy_id)
                self.save_checked_enemies()

    def recheck_people_from_enemy_list(self):
        """
        This function deletes every enemy with level lower than my_level - level_treshold and
        bigger than my_level
        """
        to_del = []
        for enemy_id in self.enemy_list:
            if self.check_player(enemy_id):
                pass
            else:
                to_del.append(enemy_id)
                self.checked_enemies.append(enemy_id)
        for _ in to_del:
            del self.enemy_list[_]
        self.save_enemy_list()
        self.save_checked_enemies()
    def recheck_people_from_checked_list(self):
        """
        this function rechecks every character from checked_list if he satisfies the condition
        my_level > enemy_level > my_level - self.treshold
        """
        to_del = []
        for enemy_id in self.checked_enemies:
            if self.check_player(enemy_id):
                to_del.append(enemy_id)
        for _ in to_del:
            self.enemy_list[_] = [0, 0]
            self.checked_enemies.remove(_)
        self.save_checked_enemies()
        self.save_enemy_list()
