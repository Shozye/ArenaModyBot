# ArenaModyBot
**The only purpose of creating this bot is for learning activities**
Bot to arenamody.pl which automates boring activities such as
 - **gathering emeralds**
 - **fighting**
 ## How to use
To use, open **config.py**, type your username, password etc.
Then uncomment one of the methods below.
Note that if you want to use bot to fighting, you need to use **findEnemies()** method first
## Overview of methods
**gather_emeralds()** - Bot will gather emeralds
**find_enemies()** - Bot will check ranking for characters that you can win with.
Then it will add them to **enemies_list** if your character can defeat it, or to **checked_enemies** otherwise
**gather_emerald_and_fight()** - Bot will attack enemies from enemy_list till energy is bigger than 6.
 Otherwise bot will start photosession and wait for its end
**fight()** - Bot will lose all its energy and then stop working.
 If there is any emerald activity, he will turn off
**recheck_checked_characters()** - Checks characters from checked_characters if you can win against them and
 if they have level high enough. If yes, it will add them to enemy_list
**recheck_enemy_list()** - It checks characters from enemy_list and throw out the ones that are better than your character
## Files
**Bot.py** - File containing basic methods of bot, Parent of FindEnemiesBot and WorkerBot
**FindEnemiesBot.py** - file with class responsible for processing enemy_list
**WorkerBot.py** - file with class responsible for working
**selectors.py** - file with function that helps organising my code and increases readability
**Controler.py** - file with class responsible for giving methods that are enough to put bot to working
**config.py** - File to control work of bot
## How does choosing enemies work
**level_treshold** is a variable that if you are better than your enemy in every skill, and
**enemy_level + level_treshold > my_level > enemy_level**
Then enemy will land in enemy_list
Then, after fighting, money that you have acquired and time when you fought will be **saved**.
If you **won't be able to attack** enemy then bot will add **24hour** timer to attack enemy
Enemies are being chosen based on money_acquired **sorted**.
**lowerbound_attack** is a variable that gives priority to fight enemies that bot wasn't fighting yet if
 there are no enemies that gives more money than lowerbound_attack