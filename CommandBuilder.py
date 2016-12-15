def buildCommand(codeString):
	defString = 'def func():\r\n'
	codeLines = codeString.split('\n')
	commandString = defString
	for i in range(len(codeLines)):
		commandString += '\n\t'+codeLines[i]
	return commandString
