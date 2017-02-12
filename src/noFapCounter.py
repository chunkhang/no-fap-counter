#!/usr/bin/env python3

import os
import sys
import time
import random
import shelve
import webbrowser


QUOTES_FILE = 'quotes.txt'


def getCurrentTime():
	''' Return current time '''
	return time.time()

def getTimeString(t):
	''' Return a tuple of formatted string of structured time '''
	structuredTime = time.localtime(t)
	date = time.strftime("%d %B %Y", structuredTime)
	_time = time.strftime("%I:%M %p", structuredTime)
	return (date, _time)

def getDays(t):
	''' Return an integer of days elapsed since t '''
	now = getCurrentTime()
	seconds = now - t
	days = int(seconds // 60 // 60 // 24)
	return days

def resetCounter(s):
	''' Store the current time in data '''
	now = getCurrentTime()
	s['epoch'] = now

def printDivider():
	print()
	print(' ============================')
	print()

def leftAlignString(text, width):
	''' Return a string left-aligned within the given width '''
	words = text.split()
	# Check longest word against width
	longestWord = ''
	for word in words:
		if len(word) > len(longestWord):
			longestWord = word
	assert len(longestWord) <= width, 'Longest word cannot exceed width'
	# Left-align text
	string = ''
	line = ''
	firstWord = True
	for word in words:
		lineLength = len(line)
		wordLength = len(word) + 1
		if firstWord:
			line += word
			firstWord = False
			continue
		if lineLength + wordLength > width:
			line += ('\n')
			string += line
			line = word
		else:
			line += (' ' + word)
	string += line
	return string

def centerAlignString(text, width):
	''' Return a string centered-aligned within the given width '''
	leftAlignedText = leftAlignString(text, width)
	lines = leftAlignedText.split('\n')
	centeredLines = list(map(lambda line: line.center(width), lines))
	return '\n'.join(centeredLines)

def leftPadString(text, padding):
	''' Return a string left-padded with the given padding '''
	lines = text.split('\n')
	paddedLines = (map(lambda line: ' '*padding + line, lines))
	return '\n'.join(paddedLines)

print()
print(' ---------------------------- ')
print('|  NO FAP CHALLENGE COUNTER  |')
print(' ---------------------------- ')
print()
# print(' Author: Marcus Mu')
# print(' Email: chunkhang@gmail.com')
# print(' Last Updated: 2017-02-09')

# Change working directory to script's location
scriptPath = os.path.realpath(__file__)
scriptDirectory = os.path.dirname(scriptPath)
os.chdir(scriptDirectory)

# Display random quote
with open(QUOTES_FILE, 'r') as file:
	lines = file.read().split('\n')
	quotes = []
	for line in lines[1:]:
		quotes.append(line)
	quote = random.choice(quotes)
	author, saying = quote.split('-')
	centeredSaying = centerAlignString(saying.strip(), 28)
	print(leftPadString(centeredSaying, 1))
	print(('(%s)' % author.strip()).center(30))

printDivider()

while True:
	with shelve.open('.counter_data') as shelf:
		# Display epoch
		epochExists = True
		if 'epoch' not in shelf:
			# Set default value for epoch
			shelf['epoch'] = None
			epochExists = False
		else:
			if shelf['epoch'] is None:
				epochExists = False
			else:
				epoch = shelf['epoch']
		print('EPOCH'.center(30))
		print('-----'.center(30))
		if epochExists:
			print(getTimeString(epoch)[0].center(30))
			print(getTimeString(epoch)[1].center(30))
		else:
			print('-'.center(30))

		# Display today
		print()
		print('TODAY'.center(30))
		print('-----'.center(30))
		print(getTimeString(getCurrentTime())[0].center(30))
		print(getTimeString(getCurrentTime())[1].center(30))

		# Display day
		print()
		print('DAY'.center(30))
		print('---'.center(30))
		if epochExists:
			print(str(getDays(epoch)).center(30))
		else:
			print('-'.center(30))

		reset = False
		while True:
			printDivider()
			print(' (0) RESET')
			print(' (1) PANIC')
			print(' (2) NOTE')
			print(' (3) EXIT')
			print()

			# Prompt response
			response = ''
			while True:
				response = input(' Enter a number: ')
				if response in '0 1 2 3'.split():
					break
				else:
					print(' Invalid response.\n')

			if response == '0':
				# Confirm reset
				printDivider()
				confirm = ''
				while True:
					confirm = input(' Are you sure? (Y/N) ')
					if confirm in 'Y y N n'.split():
						break
					else:
						print(' Invalid response.\n')
				# Reset epoch
				if confirm.upper() == 'Y':
					printDivider()
					print('Resetting counter...'.center(30)) 
					print()
					print('     ', end='')
					for i in range(20): 
						time.sleep(0.5)
						print('|', end='', flush=True)
					print()
					printDivider()
					resetCounter(shelf)
					reset = True
			elif response == '1':
				# Panic button
				printDivider()
				print(' Panic button initiated...')
				webbrowser.open('https://emergency.nofap.com')
			elif response == '2':
				# Display note
				printDivider()
				print(' EPOCH  Date and time of last')
				print('        reset                ')
				print(' TODAY  Current date and time')
				print(' DAY    Number of days since ')
				print('        epoch                ')
				print('        (1 day = 24 hours)   ')
				print(' PANIC  Opens the panic link ')
				print('        (emergency.nofap.com)')
				print(' RESET  Reset the counter    ')
				print(' EXIT   Exit the program     ')
			else:
				# Exit program
				printDivider()
				sys.exit()

			if reset:
				break 