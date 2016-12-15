# -*- coding: UTF-8 -*-

import string, socket
from Command import *

global CHAT_URL
CHAT_URL = "irc.chat.twitch.tv"
global CHAT_PORT
CHAT_PORT = 6667
global CHAT_PASS
CHAT_PASS = "oauth:0q7u6p0p4zlus5wgn0sw244xc65nh3"
CHANNEL = "savedbygrace251"
# ******************************************
# Socket Functions
# ******************************************
def openSocket():
	s = socket.socket()
	s.connect((CHAT_URL, CHAT_PORT))
	s.send("USER xx_testingbot_xx\r\n")
	s.send("PASS "+CHAT_PASS+"\r\n")
	s.send("NICK xX_TestingBot_Xx\r\n")
	s.send("CAP REQ :twitch.tv/membership\r\n")
	s.send("CAP REQ :twitch.tv/commands\r\n")
	s.send("JOIN #savedbygrace251\r\n")
	return s

def joinRoom(s):
	print("Attempting join")
	readbuffer = ""
	Loading = True
	while Loading:
		readbuffer = readbuffer + s.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)
			Loading = loadingComplete(line)
	sendMessage("Hello Chat!")
	
def loadingComplete(line):
	if("End of /NAMES list" in line):
		return False
	else:
		return True

# ******************************************
# Chat Functions
# ******************************************
def getUser(line):
	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user

def getMessage(line):
	separate = line.split(":", 2)
	message = separate[2]
	return message

def sendMessage(message):
	messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
	SOCKET.send(messageTemp + "\r\n")
	print("Sent: " + messageTemp)

# ******************************************
# Main
# ******************************************

print("here now")
SOCKET = openSocket()
joinRoom(SOCKET)
readbuffer = ""
while True:
		readbuffer = readbuffer + SOCKET.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		for line in temp:
			print(line)
			if "PING" in line:
				SOCKET.send(line.replace("PING", "PONG"))
				break
			user = getUser(line)
			message = getMessage(line)
			print(user + ": " + message)
			if message[0] == '!':
				command = message[1:].split()[0]
				commandStr = message[1:].split()
				output = runCommand(command)
				if output != "##NAC##":
					sendMessage(output)
				if output == "##NAC##":
					output = builtInFunc(user, commandStr)
					if output != "":
						sendMessage(output)







