from re import findall

def turtleToFunction(commands: str, functionName: str) -> str:
    '''#### Creates function for Turtle commands that supports transformations.

    ---

    ### Paramaters::

        commands (str)          Multiline string of all commands used.
        functionName (str)      Name of function.

    ### Returns::

        function (str)      String containing function that allows transformations.
    '''
    commands = commands.splitlines()
    newCommands = [None] * len(commands)

    matches = [":", "#", "="] 

    for i in range(len(commands)):
        if any(x in commands[i] for x in matches) or commands[i].isspace() or commands[i] == "":
            # structures, comments, assignments, whitespaces, empty strings
            newCommands[i] = commands[i]
        else:
            # everything else
            indentation, command, value = findall("([\s]*)([A-Za-z\.]+)(?:\()([-\d\w,\s()\[\]]*)(?:\))", commands[i])[0]

            if "forward" in command:
                # forward gets scaled
                newCommands[i] = f"{indentation}{command}(scale * ({value}))"
            elif "goto" in command:
                # goto gets transformed and shifted
                x, y = value.split(",") 
                newCommands[i] = f"{indentation}{command}(scale * ({x}) + xShift, scale * ({y}) + yShift)"
            elif "setposition" in command or "setpos" in command:
                # setposition gets transformed and shifted
                x, y = value.split(",")
                # remove whitespace
                y = y.strip() 
                newCommands[i] = f"{indentation}{command}(scale * ({x}) + xShift, scale * ({y}) + yShift)"
            else:
                # Any other rotation
                newCommands[i] = f"{indentation}{command}({value})"
        
    functionList = [None] * (len(commands) + 2)

    # Function definition
    functionList[0] = f"def {functionName}(scale, xShift, yShift):"
    
    # Initial goto()
    functionList[1] = "    goto(xShift, yShift)"

    for i in range(len(functionList) - 2):
        functionList[i + 2] = "    " + newCommands[i]

    return "\n".join(functionList)

if __name__ == "__main__":
    # test commands
    listOfCommands = '''
for i in range(180):
    forward(100)
    right(30)
    forward(20)
    left(60)
    forward(50)
    right(30)
    
    penup()
    setposition(0, 0)
    pendown()
    
    right(2)
'''

    print(turtleToFunction(listOfCommands, "transformedTurtle"))
