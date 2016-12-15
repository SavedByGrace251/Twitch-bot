import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_app.settings")

from twitchbot.models import User, UserClass, Class, Item, Inventory, ChatCommand, ActivityCommand
from CommandBuilder import buildCommand

chatCommands = ChatCommand.objects.all()
actCommands = ActivityCommand.objects.all()

def updateClasses():
	AvailClasses = {}
	for i in Class.objects.all():
		AvailClasses[i.id] = i
	return AvailClasses

def updateItems():
	AvailItems = {}
	print(Item.objects.all())
	for i in Item.objects.all():
		AvailItems[i.name] = i
	return AvailItems

def DefaultFunc():
	return

def runCommand(comName):
	cCommand = ""
	try:
		cCommand = ChatCommand.objects.filter(name=comName)[0]
	except IndexError:
		pass
	aCommand = ""
	try:
		aCommand = ActivityCommand.objects.filter(name=comName)[0]
	except IndexError:
		pass
	if cCommand != "":
		return str(runChatCommand(cCommand))
	elif aCommand != "":
		return str(runActCommand(aCommand))
	else:
		print(comName + " is not a function")
		return "##NAC##"

def builtInFunc(user, commandStr):
	print(commandStr)
	dbuser = []
	dbuser = User.objects.filter(name=user)
	if len(dbuser) > 0:
		print(dbuser[0])
		dbuser = dbuser[0]
	if commandStr[0] == "buy":
		AvailItems = updateItems()
		if len(commandStr) < 3:
			return "[ERROR] The \"buy\" command syntax is: !buy [item] [quantity]"
		print(AvailItems)
		try:
			AvailItems[commandStr[1]]
		except KeyError:
			return "[ERROR] The item \""+commandStr[1]+"\" does not exist"
		else:
			return "[ERROR] The item \""+commandStr[1]+"\" does exist"
		return "[ERROR] Sorry, the command \"buy\" is not implemented yet, BTW, you have "+money+" test bits"
	if commandStr[0] == "addCommand":
		AvailClasses = updateClasses()
		commandName = commandStr[1]
		commandResponse = ""
		for i in commandStr[2:]:
			commandResponse += " "+i
		# Build the Command	
		newCommand = ChatCommand()
		newCommand.name = commandName
		newCommand.response = commandResponse
		newCommand.descriptions = "Command created by "+user
		newCommand.group = AvailClasses["V"]
		newCommand.save()
		print(newCommand)
		return "[Admin] command "+commandName+" created"
	return ""

def runChatCommand(command):
	return command.response

def runActCommand(command):
	exec(buildCommand(command.code))
	output = func()
	func = DefaultFunc
	return output