#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "b@cafebeep.com"
__company__ = "BEEP BEEP Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2019-05-12"
__doc__ =     "Logic to run cafeBEEP Flask kiosk GUI front-end"

# Useful web IDE to test Flask programs on https://repl.it/
# OLD DRIVER CODE https://github.com/ROBO-BEV/CafeBeep/blob/2d04e4e298290e4dc736326b1a889be227587155/CafeBeepKiosk-0.1/CafeBeepDriver.py

# BEEP BEEP Technologies Inc code
import Drink		# Store valid BEEP BEEP drink configurations
import UserData 	# Store user name, ID, and drink preferences
import Actuator		# Modular plug and play control of motors, servos, and relays
import CafeBeepDriver	# Back-end logic connected to GUI

# Useful system jazz
import sys, time, traceback, argparse, string

# Allow keyboard to control program flow and typing to terminal window
#import pynput.keyboard
#from pynput.keyboard import Key, Controller

# Allows for the creation of a GUI web app that communicates with python backend code
# Save HTML file in a folder called "templates" in the same folder as your Flask code.
# Save user state / data across page refreshes and crashes, by using browser cookies.
from flask import Flask, render_template, session

# Useful Constants

# Current plan for cafeBEEP is to build 4 different kiosk
MAX_CONFIG_NUM = 4

# No kiosk should sell more then 4 different drink type https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2864034/
MAX_DRINK_NUM = 4


VEND_SCREEN = 0                 # Front screen to display ready orders and direct users on steps to vend
ORDER_SCREEN_1 = 1              # Right side order screen use to order beverage on kiosk (i.e. Not on phone)
ORDER_SCREEN_2 = 2              # Left side order screen use to order beverage on kiosk (i.e. Not on phone)


# Make a Flask application and start running code from __main__
app = Flask(__name__)
app.secret_key = 'BeepBeep@42'            #TODO: Select STRONG key for production code
app.config['SESSION_TYPE'] = 'filesystem' #

###
# Adding @app.route('/') line on top of a function definition turns it into a “route.”
# Basically, it means if you go to your website with a slash at the end and nothing else,
# the code in the HomeScreen() function will be run, and whatever is returned will be shown in your browser.
###
@app.route('/')
def HomeScreen():
	drinkID0_VendCount = session.get('drinkID0_VendCount', None)

	return 'Hello World, this is the cafeBEEP robotic coffee kiosk!'

###
# GUI for front facing vend screen that shows logo and location of cup pick up
#
# @userID - 10 digit integer variable assign to each user (North America phone number)
#
# @return String variable to display to user on kiosk touchscreen
###
@app.route('/VendScreen/<int:userID>')
def VendScreen(userID):
	firstName = GetUserFirstName(userID)
	drinkName = GetUserDrinkName(userID)
	return 'Morning ' + firstName + ', one cold brew coffee with half & half coming right up.'

###
# GUI for two side facing menu screens that display coffee options available for order
#
# @drinkConfiguration - Setup config to use from franchise database. (e.g. Congfig #0 is two drinks; 1 Hot Brew & 1 Cold Brew)
#
# @return HTML template to display with dymanic variables loaded
###
#TODO: TypeError: MenuScreen() got an unexpected keyword argument 'drinkConfiguration'
@app.route('/MenuScreen/<int:pageNum>/<int:drinkConfiguration>/<int:userID>')
def MenuScreen(pageNum, drinkConfiguration, userID):
	if(drinkConfiguration > MAX_CONFIG_NUM):
		print("INVALID DRINK CONFIGURATION SELECTED - TRY A NUMBER LESS THAN 4.")
		return

	kioskConfig = [[0]*MAX_DRINK_NUM for _ in range(MAX_DRINK_NUM-1)] # Initialise 2D array with all ZEROs
	for colNum in range(len(kioskConfig[drinkConfiguration])):	  # Load 2D array with data from Configuration Database dictionary
        	kioskConfig[drinkConfiguration][colNum] = SearchConfigurationDatabase(drinkConfiguration, colNum)

	HTMLtoDisplay = "INVALID"
	if (pageNum ==  -1):
		HTMLtoDisplay = "MenuGUI_DrinkPage.html"
	elif (pageNum == -2):
		HTMLtoDisplay = "MenuGUI_PhoneDialerPage.html"
	elif (pageNum ==  -3):
		HTMLtoDisplay = "MenuGUI_CustomizePage.html"
	elif (pageNum ==  -4):
		HTMLtoDisplay = "MenuGUI_HomePage.html"
	elif (pageNum ==  -5):
		HTMLtoDisplay = "MenuGUI_???Page.html"

	menuUser = UserData("TBD", "TBD", userID)

	return render_template(
		HTMLtoDisplay, # Name of HTML template to use
		# Load 2D array that holds current kiosk configuration (row) and drink name (column) to set HTML GUI variables
		# TODO: Add global variable to track drink percentage for each drinkID "drinkPercentage0"
		userFirstName = menuUser.GetUserFirstName(userID),
		drinkID0 = kioskConfig[drinkConfiguration][0],
		drinkPercentage0 = 100,
		drinkID1 = kioskConfig[drinkConfiguration][1],
		drinkPercentage1 = 100,
		drinkID2 = kioskConfig[drinkConfiguration][2],
		drinkPercentage2 = 100,
		drinkID3 = kioskConfig[drinkConfiguration][3],  # NOTE: drinkID? = MAX_DRINK_NUM - 1 = 3
		drinkPercentage3 = 100

	)

@app.route('/Bulma_Sample')
def MenuScreen_Murali():
	HTMLtoDisplay = "Bulma_Sample.html"
	return render_template(HTMLtoDisplay)

def SearchConfigurationDatabase(configNum, drinkNum):
	if(configNum == 0):
		configurationDatabase = {
			0: "Cold Brew",
			1: "Hot Brew"
		}
	elif(configNum == 1): #TODO: Can we have two dictionaries with same name in same function? YES each local to if statement
		configurationDatabase = {
			0: "Espresso",
			1: "Hot Brew",
			2: "Cold Brew"
		}
	else:
		print("PRINT CONFIGURATION /#" + configNum + " DOES NOT EXIST IN BEEP BEEP FRANCHISE SYSTEM")

	return configurationDatabase.get(drinkNum, "INVALID DRINK CONFIGURATION")



###
# Code starts execution from here
###
if __name__ == '__main__':
	app.run(host='0.0.0.0')
