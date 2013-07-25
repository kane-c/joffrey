from __future__ import division
from random import choice
import re
from plugins.plugin_settings.Phrangman import *
from registry import BasePlugin, plugin_registry
import os
import random
import string

class Phrangman(BasePlugin):

    commands = {
        '!hangman': 'Play the hangman game ^_^'
    }

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


    def reset(self):
        self.word = ''
        self.selected_characters = []
        self.available_characters = set([c for c in string.ascii_lowercase])

    def isGameOn(self):
        return self.word != ''

    def getCountRule(self):
        if self.word == '':
            return -1
        else:
            return self.count_rules[len(self.word)] if len(self.word) in self.count_rules else self.count_rules['other']

    def getWordMask(self):
        mask = ''
        for letter in list(self.word.lower()):
            if letter in self.selected_characters:
                mask += letter.upper() + ' '
            else:
                mask += '    ' if letter == ' ' else '_ '
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

    def displayAvailableCharacters(self):
        return_str = '[ '
        sorted_avail = sorted(self.available_characters.difference(self.selected_characters),
                              key=lambda item:(float('inf'), item))
        for c in sorted_avail:
            return_str += c + ' '
        return return_str + ']'


    def process(self, message, sender, command=None, *args):
        if command != 'hangman': return
        if len(args) == 1 and args[0] == '': args = []
        args = [a.lower() for a in args]
        if len(args) == 0:
            if self.isGameOn() :
                return 'Another hangman game is already in progress.'

            return_msg = 'Listen carefully. You peasants will all be hang if you can\'t get it right.\nNow tell me which area of knowledges you want to challenge:\n\n'
            for area in self.knowledge_areas:
                if '.' not in area:
                    return_msg += ' ' + area + '\n'
            return_msg += '\nFor example Type !hangman food or type !hangman help for more information'
            return return_msg

        elif args[0] in self.knowledge_areas:
            if self.isGameOn() :
                return 'You haven\'t solved the other Hangman challange yet.'

            area_name = args[0]
            lines = open(self.words_path + area_name).read().splitlines()
            self.word = random.choice(lines)
            msg_area = self.getHangProgressionImage()
            mask = self.getWordMask()
            msg_area += 'Solve this: ' + mask
            msg_area += '\nAvailable characters: ' + self.displayAvailableCharacters()

            return msg_area

        elif args[0] == 'guess':
            if not self.isGameOn():
                return 'You need to start the game first and choose a topic first Or should I just chop your head off now? teehee'
            args.remove('guess')
            guess_word = ''.join(args)

            if guess_word.lower() == self.word.lower():
                self.reset()
                return 'Good guess! I now promote you to become Hand of the King'
            else:
                self.reset()
                return 'Ha ha ha! What a risky and unpaid move.\nGame Ended! You shall be served idiot!\n*Chopping Sound* (X_X) ... (==<'


        elif args[0] == 'stop':
            self.reset()
            return 'Shame on you Peasants! You dared to quit this holy game'

        elif args[0] in self.available_characters:
            if not self.isGameOn():
                return 'You need to start the game first and choose a topic first Or should I just chop your head off now? teehee'

            guess = args[0]

            if guess in self.selected_characters:
                return 'I guess you peasant has a short-term memory issue. You have already guessed that character before'
            else:
                self.selected_characters.append(guess)
                if self.wonYet():
                    self.reset()
                    return 'Congratulations! I now promote you to become Hand of the King!'

                progression = self.getHangProgression()
                game_progress_msg = self.getHangProgressionImage(progression)

                if progression == 100:
                    game_progress_msg += 'Ha Ha Ha! Game Ended! You shall be served idiot!\n*Chopping Sound* (X_X) ... (==<'
                    self.reset()
                else:
                    mask = self.getWordMask()
                    game_progress_msg += 'So far: ' + mask
                    game_progress_msg += '\nAvailable characters: ' + self.displayAvailableCharacters()
                return game_progress_msg
        elif args[0] == 'help':
            return 'Available commands are\n!hangman: to start a game\n!hangman foods: to start playing hangman with the topic foods\n!hangman a: to guess letter a\n!hangman guess yamaha: to guess the word yamaha (you may get punished for wrong guess)\n!hangman stop: to stop the game'
        else :
            return 'Are you trying to hack this godly game or simply just retarded? Nice try'

plugin_registry.register(Phrangman())
