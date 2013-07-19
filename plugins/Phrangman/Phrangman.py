from random import choice
import re
from registry import BasePlugin, plugin_registry
import os
import random

class Phrangman(BasePlugin):
	
	count_rules = {'3': 5, '4': 7, 'other': 12}	
	commands = ('hangman start', 'hangman area', 'hangman stop', 'hangman letter')
    
	def __init__(self):
		self.reset()
		script_dir = os.path.dirname(__file__)					
	
		# Load Words Data
		words_path = os.path.join(script_dir, 'data/hangman/')		
		knowledge_areas = []
		for knowledge_area in os.listdir(words_path):
			self.knowledge_areas.append(os.path.join(words_path, knowledge_area))
		hangman_images_path = os.path.join(script_dir, 'data/hangman/')
		
		# Load 'graphic' elements ;)
		self.hangman_images = { }		
		for hangman_image in os.listdir(hangman_images_path):
			f = open (os.path.join(hangman_images_path, hangman_image),"r")
			image = f.read()
			self.hangman_images[hangman_image] = image
		
		for i in range(1,26):
			self.available_characters = str(unichr(96+i))
	
	def reset(self):
		self.count_rule = 9
		self.word = ''
		self.selected_characters = []
		self.available_characters = []
		
	def getCountRule(self):
		if self.word == '':
			return -1
		else:
			if `self.word.__len__()` in count_rules:
				return count_rules[`self.word.__len__()`]
			else
				return count_rules['other']
				
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
		progression = round(len(self.selected_characters) / self.getCountRule()) * 100
		if progression > 100:
			progression = 100
		progression = (progression//10) * 10
		return progression
		
	def getHangProgressionImage(self, progression):
		return self.hangman_images['10'] + '\n\n'
		
	def wonYet(self):
		for l in word:
			if l not in self.selected_characters:
				return false
		return true 

	def process(self, message, sender):
		if 'hangman start' == message.lower():
			msg_start = 'Hahaha. You peasants will all be hang if you can\'t get it right.\nNow tell me which area of knowledges you want to challenge by typing "hangman area <name of the area>":\n'
			for area in knowledge_areas:
				return_msg += area + ','
			return start_msg        	
        	
		elif 'hangman area' in message.lower():				
			message_words = message.lower().split()
			area_name = message_words[2] 
        	if self.getHangProgression() < 100 :
        		return 'You haven\'t solved the other challange yet you stupid peasants.'
			
			if area_name in knowledge_areas:
				lines = open('./data/words/' + area_name).read().splitlines()			
				self.word = random.choice(lines)
				msg_area = self.getHangProgressionImage()
				mask = self.getWordMask()
				msg_area += 'Solve this: ' + mask
				
				return msg_area
			else:
				return 'Can\'t you read you peasant, well I guess not. Pick one of the areas that I have said above ^'

		elif 'hangman letter' in message.lower():
			message_words = message.lower().split()
			guess = message_words[2] 
        	if guess not in self.available_characters:
        		return 'Hey, in my kingdom you are only allowed to use ASCHII characters.'
        		
        	if guess in self.selected_characters:
        		return 'I guess you peasant has a short-term memory issue. You have already guessed that character before.'
       		else:
       			self.selected_characters.append(guess)
       			if wonYet():
       				return 'CONGRATULATION! I KNOW PROMOTE YOU TO BECOME THE HAND OF THE KING!'
				
				progression = self.getHangProgression()
				game_progress_msg = self.getHangProgressionImage(progression)
				
				if progression == 100:
					game_progress_msg += 'HAHAHA! GAME ENDED! YOU SHALL BE SERVED IDIOT!\n*CHOPPING SOUND*'
					self.reset()
				else:
					mask = self.getWordMask()
					msg_area += 'So far: ' + mask
				
				return game_progress_msg
		
		elif 'hangman stop' in message.lower():
			self.reset()
			return 'SHAME ON YOU PEASANT! You dared to quit this Godly made game'
			
	def post_process(self, reply, message, sender):
		return '{}, peasant'.format(reply)

plugin_registry.register(Phrangman())
