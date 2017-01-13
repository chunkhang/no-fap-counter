#!/usr/bin/env python3

import os, shelve, time, sys

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

print()
print(' ---------------------------- ')
print('|  NO FAP CHALLENGE COUNTER  |')
print(' ---------------------------- ')

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
		print()
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

		# Display days
		print()
		print('DAY'.center(30))
		print('---'.center(30))
		if epochExists:
			print(str(getDays(epoch)).center(30))
		else:
			print('-'.center(30))

		reset = False
		while True:
			print()
			print(' (1) RESET')
			print(' (2) NOTE')
			print(' (3) EXIT')
			print()

			# Prompt response
			response = ''
			while True:
				response = input(' Enter a number: ')
				if response in '1 2 3':
					break
				else:
					print(' Invalid response.\n')

			if response == '1':
				# Reset epoch
				print()
				print(' Counter reset...')
				resetCounter(shelf)
				reset = True
			elif response == '2':
				# Display note
				print()
				print(' Note:')
				print(' This program stores data in a')
				print(' hidden file, .counter_data,  ')
				print(' located in the same path as  ')
				print(' the program.')
			else:
				# Exit program
				print()
				print(' Have a nice day!')
				sys.exit()

			if reset:
				break 