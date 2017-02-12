#!/usr/bin/env python3

import os
import sys
import time
import random
import shelve
import webbrowser


COUNTER_DATA = '.counter_data' # Path for counter data file
QUOTES_FILE = 'quotes.txt' # Path for quotes file
WIDTH = 30 # Width of the entire program
LEFT_PADDING = 2 # Left padding for the entire program
RESET_BAR = 20 # Length of reset bar
RESET_SPEED = 0.5 # Larger value means slower reset

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
	''' Print a horizontal divider '''
	print(leftPadString('\n%s\n' % ('='*(WIDTH-2)), LEFT_PADDING))

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

def printQuote():
	''' Print a random quote '''
	with open(QUOTES_FILE, 'r') as file:
		lines = file.read().split('\n')
		quotes = []
		for line in lines[1:]:
			quotes.append(line)
		quote = random.choice(quotes)
		author, saying = quote.split('-')
		centeredSaying = centerAlignString(saying.strip(), WIDTH-2)
		print(leftPadString(centeredSaying, LEFT_PADDING))
		print(('(%s)' % author.strip()).center(WIDTH-2+(LEFT_PADDING*2)))


# Print program title
print(leftPadString('\n%s' % ('-'*(WIDTH-2)), LEFT_PADDING))
print(leftPadString('|%s|' % 'NO FAP CHALLENGE COUNTER'.center(WIDTH-2), LEFT_PADDING-1))
print(leftPadString('%s\n' % ('-'*(WIDTH-2)), LEFT_PADDING))

# Change working directory to script's location
scriptPath = os.path.realpath(__file__)
scriptDirectory = os.path.dirname(scriptPath)
os.chdir(scriptDirectory)

# Print random quote
printQuote()
printDivider()

while True:
	with shelve.open(COUNTER_DATA) as shelf:
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
		print('EPOCH'.center(WIDTH-2+(LEFT_PADDING*2)))
		print('-----'.center(WIDTH-2+(LEFT_PADDING*2)))
		if epochExists:
			print(getTimeString(epoch)[0].center(WIDTH-2+(LEFT_PADDING*2)))
			print(getTimeString(epoch)[1].center(WIDTH-2+(LEFT_PADDING*2)))
		else:
			print('-'.center(WIDTH-2+(LEFT_PADDING*2)))

		# Display today
		print()
		print('TODAY'.center(WIDTH-2+(LEFT_PADDING*2)))
		print('-----'.center(WIDTH-2+(LEFT_PADDING*2)))
		print(getTimeString(getCurrentTime())[0].center(WIDTH-2+(LEFT_PADDING*2)))
		print(getTimeString(getCurrentTime())[1].center(WIDTH-2+(LEFT_PADDING*2)))

		# Display day
		print()
		print('DAY'.center(WIDTH-2+(LEFT_PADDING*2)))
		print('---'.center(WIDTH-2+(LEFT_PADDING*2)))
		if epochExists:
			print(str(getDays(epoch)).center(WIDTH-2+(LEFT_PADDING*2)))
		else:
			print('-'.center(WIDTH-2+(LEFT_PADDING*2)))

		reset = False
		while True:
			printDivider()
			print(leftPadString('(0) RESET', LEFT_PADDING))
			print(leftPadString('(1) PANIC', LEFT_PADDING))
			print(leftPadString('(2) ABOUT', LEFT_PADDING))
			print(leftPadString('(3) EXIT\n', LEFT_PADDING))

			# Prompt response
			response = ''
			while True:
				response = input(leftPadString('Enter a number: ', LEFT_PADDING))
				if response in '0 1 2 3'.split():
					break
				else:
					print(leftPadString('Invalid response.\n', LEFT_PADDING))
			printDivider()

			# Evaluate response
			if response == '0':
				# Confirm reset
				confirm = ''
				while True:
					confirm = input(leftPadString('Are you sure? (Y/N) ', LEFT_PADDING))
					if confirm in 'Y y N n'.split():
						break
					else:
						print(leftPadString('Invalid response.\n', LEFT_PADDING))
				# Reset epoch
				if confirm.upper() == 'Y':
					printDivider()
					print('Resetting counter...'.center(WIDTH-2+(LEFT_PADDING*2))) 
					print()
					print(' '*(int((WIDTH-2-RESET_BAR)/2)+LEFT_PADDING), end='')
					for i in range(RESET_BAR): 
						time.sleep(RESET_SPEED)
						print('|', end='', flush=True)
					print()
					printDivider()
					resetCounter(shelf)
					reset = True
			elif response == '1':
				# Panic button
				print(leftPadString('Panic button initiated...', LEFT_PADDING))
				webbrowser.open('https://emergency.nofap.com')
			elif response == '2':
				# Display about
				print(leftPadString('Author: Marcus Mu', LEFT_PADDING))
				print(leftPadString('Email: chunkhang@gmail.com', LEFT_PADDING))
				print(leftPadString('Last Updated: 2017-02-12', LEFT_PADDING))
			else:
				# Exit program
				sys.exit()

			if reset:
				break 