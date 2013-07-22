from __future__ import division
from random import choice
import re
from plugins.plugin_settings.Phrangman import *
from registry import BasePlugin, plugin_registry
import os
import random
import string

class Phrangman(BasePlugin):

    commands = ('start', 'area', 'stop', 'help')

    def __init__(self):
        self.reset()
        self.knowledge_areas = []
        self.count_rules = PHRANGMAN_COUNT_RULES if 'PHRANGMAN_COUNT_RULES' in globals() else {3: 5, 4: 7, 'other': 12}
        script_dir = os.path.dirname(__file__)

        # Load Words Data
        self.words_path = os.path.join(script_dir, PHRANGMAN_WORDS_PATH if 'PHRANGMAN_WORDS_PATH' in globals() else 'data/words/')
        for knowledge_area in os.listdir(self.words_path):
            self.knowledge_areas.append(knowledge_area)

        # Load 'graphic' elements ;)
        self.hangman_images_path = os.path.join(script_dir, PHRANGMAN_HANGMAN_IMAGES_PATH if 'PHRANGMAN_HANGMAN_IMAGES_PATH' in globals() else 'data/words/')
        self.hangman_images = {}
        for hangman_image in os.listdir(self.hangman_images_path):
            f = open(os.path.join(self.hangman_images_path, hangman_image), "r")
            image = f.read()
            try:
                self.hangman_images[int(hangman_image)] = image
            except ValueError:
                pass

        self.available_characters = string.ascii_letters

    def reset(self):
        self.word = ''
        self.selected_characters = []

    def isGameOn(self):
        return self.word != ''

    def getCountRule(self):
        if self.word == '':
            return -1
        else:
            return self.count_rules[len(self.word)] if len(self.word) in self.count_rules else self.count_rules['other']

    def getWordMask(self):
        mask = ''
        letter_choices = list(self.word)
        for letter in letter_choices:
            mask += letter.upper() if letter in self.selected_characters else '_'
        return mask

    def getHangProgression(self):
        if not self.isGameOn():
            return -1

        bad_tries = 0
        for l in self.selected_characters:
            if l not in self.word:
                bad_tries += 1

        progression = int(bad_tries / self.getCountRule() * 100)
        if progression > 100:
            progression = 100
        progression = int((progression / 10)) * 10

        return progression

    def getHangProgressionImage(self, progression=10):
        if progression%10 == 0:
            return '\n'+self.hangman_images[progression] + '\n\n'
        else:
            return ''

    def wonYet(self):
        for l in self.word:
            if l not in self.selected_characters:
                return False
        return True

    def process(self, message, sender, command=None, *args):
        if '!hangman start' == message.lower():
            if self.isGameOn() :
                return 'You haven\'t solved the other Hangman challange yet.'

            return_msg = 'Listen carefully. You peasants will all be hang if you can\'t get it right.\nNow tell me which area of knowledges you want to challenge:\n'
            for area in self.knowledge_areas:
                if '.' not in area:
                    return_msg += area + ','
            return_msg += ' or type !hangman help'
            return return_msg

        elif '!hangman area' in message.lower():
            if self.isGameOn() :
                return 'You haven\'t solved the other Hangman challange yet.'

            message_words = message.lower().split()
            area_name = message_words[2]

            if area_name in self.knowledge_areas:
                lines = open(self.words_path + area_name).read().splitlines()
                self.word = random.choice(lines)
                msg_area = self.getHangProgressionImage()
                mask = self.getWordMask()
                msg_area += 'Solve this: ' + mask

                return msg_area
            else:
                return 'Can\'t you read you peasant. Well I guess not. Puuhleese Pick one of the areas that I have said above ^'

        elif '!hangman stop' in message.lower():
            self.reset()
            return 'Shame on you Peasants! You dared to quit this holy game'

        elif '!hangman letter' in message.lower():
            if not self.isGameOn():
                return 'You need to start the game first and choose an area of knowledge. Or should I just chop your head off now? teehee'

            message_words = message.lower().split()
            guess = message_words[2]
            if guess not in self.available_characters:
                return 'Hey, in my kingdom you are only allowed to use ASCHII characters'

            if guess in self.selected_characters:
                return 'I guess you peasant has a short-term memory issue. You have already guessed that character before'
            else:
                self.selected_characters.append(guess)
                if self.wonYet():
                    return 'Congratulation! I now promote you to become Hand of the King!'

                progression = self.getHangProgression()
                game_progress_msg = self.getHangProgressionImage(progression)

                if progression == 100:
                    game_progress_msg += 'Ha Ha Ha! Game Ended! You shall be served idiot!\n*Chopping Sound* (X_X) ... (==<'
                    self.reset()
                else:
                    mask = self.getWordMask()
                    game_progress_msg += 'So far: ' + mask
                return game_progress_msg
        elif '!hangman help' in message.lower():
            return 'Available commands are\n!hangman start: to start a game\n!hangman area <name of knowledge>: to choose an area of prefer knowledge\n!hangman letter <letter>: to guess\n!hangman stop: to stop the game'

plugin_registry.register(Phrangman())
