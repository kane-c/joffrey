from __future__ import division
from random import choice
import re
from registry import BasePlugin, plugin_registry
import os
import random
import string

class Phrangman(BasePlugin):
    count_rules = {3: 5, 4: 7, 'other': 12}
    commands = ('hangman start', 'hangman area', 'hangman stop', 'hangman letter')
    script_dir = ''

    def __init__(self):
        self.reset()
        self.script_dir = os.path.dirname(__file__)

        # Load Words Data
        words_path = os.path.join(self.script_dir, 'data/words/')
        for knowledge_area in os.listdir(words_path):
            self.knowledge_areas.append(knowledge_area)

        # Load 'graphic' elements ;)
        hangman_images_path = os.path.join(self.script_dir, 'data/hangman/')
        self.hangman_images = {}
        for hangman_image in os.listdir(hangman_images_path):
            f = open(os.path.join(hangman_images_path, hangman_image), "r")
            image = f.read()
            try:
                self.hangman_images[int(hangman_image)] = image
            except ValueError:
                pass

        self.available_characters = string.ascii_letters

    def reset(self):
        self.knowledge_areas = []
        self.word = ''
        self.selected_characters = []

    def getCountRule(self):
        if self.word == '':
            return -1
        else:
            if len(self.word) in self.count_rules:
                return self.count_rules[len(self.word)]
            else:
                return self.count_rules['other']

    def getWordMask(self):
        mask = ''
        letter_choices = list(self.word)
        for letter in letter_choices:
            if letter in self.selected_characters:
                mask += letter.upper()
            else:
                mask += '_'
        return mask

    def getHangProgression(self):
        bad_tries = 0
        for l in self.selected_characters:
            if l not in self.word:
                bad_tries += 1

        progression = int(bad_tries / self.getCountRule() * 100)
        print (progression)
        if progression > 100:
            progression = 100
        progression = int((progression / 10)) * 10
        print progression
        return progression

    def getHangProgressionImage(self, progression=10):
        return '\n'+self.hangman_images[progression] + '\n\n'

    def wonYet(self):
        for l in self.word:
            if l not in self.selected_characters:
                return False
        return True

    def process(self, message, sender, command=None, *args):
        if '!hangman start' == message.lower():
            return_msg = 'Hahaha. You peasants will all be hang if you can\'t get it right.\nNow tell me which area of knowledges you want to challenge by typing "hangman area <name of the area>":\n'
            for area in self.knowledge_areas:
                return_msg += area + ','
            return return_msg

        elif '!hangman area' in message.lower():
            message_words = message.lower().split()
            area_name = message_words[2]

            if self.getHangProgression() < 100 and self.getHangProgression() > 0:
                return 'You haven\'t solved the other challange yet you stupid'

            if area_name in self.knowledge_areas:
                lines = open(self.script_dir + '/data/words/' + area_name).read().splitlines()
                self.word = random.choice(lines)
                msg_area = self.getHangProgressionImage()
                mask = self.getWordMask()
                msg_area += 'Solve this: ' + mask

                return msg_area
            else:
                return 'Can\'t you read you peasant, well I guess not. Pick one of the areas that I have said above ^'

        elif '!hangman stop' in message.lower():
            self.reset()
            return 'SHAME ON YOU PEASANT! You dared to quit this Godly made game'

        elif '!hangman letter' in message.lower():
            message_words = message.lower().split()
            guess = message_words[2]
            if guess not in self.available_characters:
                return 'Hey, in my kingdom you are only allowed to use ASCHII characters'

            if guess in self.selected_characters:
                return 'I guess you peasant has a short-term memory issue. You have already guessed that character before'
            else:
                self.selected_characters.append(guess)
                if self.wonYet():
                    return 'CONGRATULATION! I KNOW PROMOTE YOU TO BECOME THE HAND OF THE KING!'

                progression = self.getHangProgression()
                game_progress_msg = self.getHangProgressionImage(progression)

                if progression == 100:
                    game_progress_msg += 'HAHAHA! GAME ENDED! YOU SHALL BE SERVED IDIOT!\n*CHOPPING SOUND*'
                    self.reset()
                else:
                    mask = self.getWordMask()
                    game_progress_msg += 'So far: ' + mask
                return game_progress_msg

#	def post_process(self, reply, message, sender):
#		return '{}, peasant'.format(reply)

plugin_registry.register(Phrangman())
