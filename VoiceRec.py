from gtts import gTTS
import speech_recognition as sr
import re
import webbrowser
import smtplib
import pyautogui
import os
import time
from weather import Weather, Unit

# speaks audio passed as argument
def talkToMe(audio):
	
	print(audio)
	for line in audio.splitlines():
		os.system("say " + audio)

# listens for commands
def myCommand():
	r = sr.Recognizer()

	with sr.Microphone() as source:
		print('I am ready for your next command')
		r.pause_threshold = 1
		r.adjust_for_ambient_noise(source, duration = 1)
		audio = r.listen(source)

	try:
		command = r.recognize_google(audio)
		print('You said: ' + command + '\n')

	#loop back to continue to listen for commands

	except sr.UnknownValueError:
		print('Your last command couldn\'t be heard')
		command = myCommand()

		# assistant(myCommand())

	return command

#if statements for executing commands
def assistant(command):

	# chat
	if 'what\'s up' in command:
		talkToMe('Nothing much, how are you?')
		return False

	#opens application
	if 'open Google' in command:
		reg_ex = re.search('open google (.*)', command)
		url = 'https://www.google.com/'
		webbrowser.get(reg_ex).open(url)
		print('Done!')
		return False

	#searches weather by city name
	if 'what is the weather' in command:
		weather = Weather(unit=Unit.FAHRENHEIT)

		talkToMe('What city do you want to know about')
		c_answ = myCommand()

		city = c_answ #input("City Name: ")

		# looks up using name
		location = weather.lookup_by_location(city)
		forecasts = location.forecast

		for forecast in forecasts:
			talkToMe(forecast.date)
			talkToMe(forecast.text)
			talkToMe("High: " + forecast.high)
			talkToMe("Low: " + forecast.low)
		return False

	#sends email to Grace
	if 'email' in command:
		talkToMe('Who is the recipient')
		recipient = myCommand()

		if 'grace' in recipient:
			talkToMe('What should I say')
			content = myCommand()

			#init gmail SMTP
			mail = smtplib.SMTP('smtp.gmail.com', 587)

			#identify to server
			mail.ehlo()

			#encrypt session
			mail.starttls()

			#login
			mail.login('gstenger12', 'dorriseaton')

			#send message
			mail.sendmail('Bro', 'gstenger19@deerfield.edu', 'Hello!')

			#close connection
			mail.close()

			talkToMe('Email sent')

		return False

	#opens Spotify
	if 'play my music' in command:
		talkToMe('Opening spotify')

		# (720, 794)
		os.system("open -a Spotify")

		print(pyautogui.position())

		time.sleep(5)

		pyautogui.click(720, 794)

		return False

	# connects to AirPlay
	if 'Connect to airplay' in command:
		talkToMe('opening airplay')

		from subprocess import Popen, PIPE

		script = '''
			tell application "System Events"
			tell process "SystemUIServer"
				click (menu bar item 1 of menu bar 1 whose description contains "Displays")
				click menu item 4 of menu 1 of result
			end tell
		end tell'''
		args = ['2', '2']

		p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
		stdout, stderr = p.communicate(script)
		print(p.returncode, stdout, stderr)
		return False

	if 'goodbye' in command:
		print('Good bye!')
		return True


if __name__ == "__main__":

	talkToMe('I am ready for your command')

	quit = False

	while not quit:
		quit = assistant(myCommand())
