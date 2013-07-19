from random import choice
import re
from registry import BasePlugin, plugin_registry
import os
import random

class Phrangman(BasePlugin):
    commands = ('hangman start', 'hangman area', 'hangman stop', 'hangman letter')
    msg_start = 'Hahaha. You peasants will all be hang if you can\'t get it right.\nNow tell me which area of knowledges you want to challenge by typing "hangman area <name of the area>":\n'
    knowledge_areas = []
    count_rules = {'3': 3, '4': 4, 'other': 9}
    hangman_images = { }
    word = ''
    selected_characters = []
    available_characters = []
    progression = 0
    
	def __init__(self):
		for knowledge_area in os.listdir('./data/words/'):
			knowledge_areas += file += ','
		for hangman_image in os.listdir('./data/hangman'):
			f = open (hangman_image,"r")
			image = f.read()
			hangman_images[hangman_image] = image
		
		for i in range(1,26):
			available_characters = str(unichr(96+i))
		}
	
	def getWordMask(self):
		mask = ''
		letter_choices = list(word)
		for letter in letter_choices:
			if letter in selected_characters:
				mask += letter.upper()
			else:
				mask += '_'
		return mask

    def process(self, message, sender):
        if 'hangman start' == message.lower():
        	msg_start = msg_start
        	for area in knowledge_areas:
				return_msg += self.knowledge_areas += ','
			return start_msg        	
        	
		elif 'hangman area' in message.lower():				
        	message_words = message.lower().split()
        	area_name = message_words[2] 
        	if progression < 1 :
        		return 'You haven\'t solved the other challange yet you stupid peasants.'

            if area_name in knowledge_areas:
                msg_area = hangman_images['10'] + '\n\n'
				lines = open('./data/words/'+area_name).read().splitlines()
				word = random.choice(lines)
				mask = getWordMask()
				msg_area += mask
				
				return msg_area
				
            else:
            	return 'Can\'t you read you peasant, well I guess not. Pick one of the areas that I have said above'

    def post_process(self, reply, message, sender):
        return '{}, peasant'.format(reply)

plugin_registry.register(Phrangman())
