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

            if "forward" in command or "fd" in command:
                # forward gets scaled
                newCommands[i] = f"{indentation}{command}(scale * ({value}))"
            if "backward" in command or "bk" in command or "back" in command:
                # forward gets scaled
                newCommands[i] = f"{indentation}{command}(scale * ({value}))"
            elif "goto" in command:
                # goto gets scaled and shifted
                x, y = value.split(",") 
                newCommands[i] = f"{indentation}{command}(scale * ({x}) + xShift, scale * ({y}) + yShift)"
            elif "setposition" in command or "setpos" in command:
                # setposition gets scaled and shifted
                x, y = value.split(",")
                # remove whitespace
                y = y.strip() 
                newCommands[i] = f"{indentation}{command}(scale * ({x}) + xShift, scale * ({y}) + yShift)"
            elif "circle" in command:
                # circle gets scaled 
                args = value.split(",")

                if len(args) == 1:
                    # only radius was provided
                    newCommands[i] = f"{indentation}{command}(scale * ({args[0]}))"
                elif len(args) == 2:
                    # radius and extent were provided
                    # remove whitespace
                    args[1] = args[1].strip()
                    newCommands[i] = f"{indentation}{command}(scale * ({args[0]}), {args[1]})"
                elif len(args) == 3:
                    # radius, extent and steps were provided
                    # remove whitespace
                    args[1] = args[1].strip()
                    args[2] = args[2].strip()
                    newCommands[i] = f"{indentation}{command}(scale * ({args[0]}), {args[1]}, {args[2]})"
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
circle(40)
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
