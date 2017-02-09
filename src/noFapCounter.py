#!/usr/bin/env python3

import os
import sys
import time
import shelve
import termios

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
	''' Return an integer of days elapsed since t'''
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

print()
print(' ---------------------------- ')
print('|  NO FAP CHALLENGE COUNTER  |')
print(' ---------------------------- ')
print()
print(' Author: Marcus Mu')
print(' Email: chunkhang@gmail.com')
print(' Last Updated: 09/02/17')
printDivider()

# Change working directory to script's location
scriptPath = os.path.realpath(__file__)
scriptDirectory = os.path.dirname(scriptPath)
os.chdir(scriptDirectory)

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
			print(' (1) RESET')
			print(' (2) NOTE')
			print(' (3) EXIT')
			print()

			# Prompt response
			response = ''
			while True:
				response = input(' Enter a number: ')
				if response in '1 2 3'.split(' '):
					break
				else:
					print(' Invalid response.\n')

			if response == '1':
				# Confirm reset
				printDivider()
				confirm = ''
				while True:
					confirm = input(' Are you sure? (Y/N) ')
					if confirm in 'Y y N n'.split(' '):
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
						# sys.stdout.write('|')
						# sys.stdout.flush()
						print('|', end='', flush=True)
					print()
					printDivider()
					resetCounter(shelf)
					reset = True
			elif response == '2':
				# Display note
				printDivider()
				print(' Note:')
				print()
				print(' EPOCH  Date and time of last')
				print('        reset                ')
				print(' TODAY  Current date and time')
				print(' DAY    Number of days since ')
				print('        epoch                ')
				print('        (1 day = 24 hours)   ')
			else:
				# Exit program
				printDivider()
				print('Have a nice day!'.center(30))
				sys.exit()

			if reset:
				break 