from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys
import re

# Java
# Python

class Parameter():
    name = "default"
    desc = "default parameter description"
    tag = "-p"
    value = None
    already_set = False
    def __init__(self, name, desc, tag, value):
        self.name = name
        self.desc = desc
        self.tag = tag
        self.value = value
    def set_value(self, value):
        if self.already_set == False:
            self.value = value
            self.already_set = True
        else:
            error("Cannot set the same parameter twice")
def get_file():
    #Tk().withdraw()
    #filename = askopenfilename()
    filename = "D:/CLIner/test.txt"
    return filename

def read_lines(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    return lines

def write_lines(filename, lines, parameters):
    filename = filename.replace(".txt", "-new.txt")
    file = open(filename, "w")
    for line in lines:
        # Replace regex items
        line = re.sub(r"\s*==\s*", " == ", line) # ==
        line = re.sub(r"\s*(?<![^a-zA-Z0-9 \)])\=(?![^a-zA-Z0-9 \(])\s*", " = ", line) # =
        line = re.sub(r"\s*\>\=(?![^a-zA-Z0-9 \(])\s*", " >= ", line) # >=
        line = re.sub(r"\s*\<\=(?![^a-zA-Z0-9 \(])\s*", " <= ", line) # <=
        line = re.sub(r"\s*\>(?![^a-zA-Z0-9 \(])\s*", " > ", line) # >
        line = re.sub(r"\s*\<(?![^a-zA-Z0-9 \(])\s*", " < ", line) # <
        line = re.sub(r"\s*\!\=(?![^a-zA-Z0-9 \(])\s*", " != ", line) # !=
        line = re.sub(r"\s*&&\s*", " && ", line) # &&
        line = re.sub(r"\s*\|\|\s*", " || ", line) # ||
        line = re.sub(r"\s*and\s*", " and ", line) # and
        line = re.sub(r"\s*or\s*", " or ", line) # or
        line = re.sub(r"(\( )", "(", line) # (
        line = re.sub(r"( \))", ")", line) # )
        line = re.sub(r"\s*\+\+\s*", " ++ ", line) # ++
        line = re.sub(r"\s*--\s*", " -- ", line) # --
        line = re.sub(r"\s*\*\*\s*", " ** ", line) # **
        line = re.sub(r"\s*(?<![^a-zA-Z0-9 \)])\+(?![^a-zA-Z0-9 \(])\s*", " + ", line) # +
        line = re.sub(r"\s*(?<![^a-zA-Z0-9 \)])-(?![^a-zA-Z0-9 \(])\s*", " - ", line) # -
        line = re.sub(r"\s*/\s*", " / ", line) # /
        line = re.sub(r"\s*(?<![^a-zA-Z0-9 \)])\*(?![^a-zA-Z0-9 \(])\s*", " * ", line) # *
        line = re.sub(r"\s*%\s*", " % ", line) # %
    
        # If last digit is a newline and the line is 2 characters (newline and another)
        if line[-1] == '\n' and len(line) >= 2:
            # remove the spaces between the text and the newline
            line = line[0:-1].rstrip(" ") + "\n"
        #line.replace("\t", " " * parameters["tab_count"].value)
        file.write(line)
    file.close()

def check_arguments():
    args = sys.argv
    parameters = {"snakecase" : Parameter("snakecase",
                                          "Converts all variables to variable_name form",
                                          "-s",
                                          False),
                  "camelcase" : Parameter("camelcase",
                                          "Converts all variables to variableName form",
                                          "-c",
                                          False),
                  "tab_count" : Parameter("tab count",
                                          "How many spaces to replace each tab with",
                                          "-t",
                                          3)
                 }
    # for each argument
    for i in range(len(args)):
        for parameter in parameters:
            param = parameters[parameter]
            # check to see if its a parameter
            if param.tag == args[i]:
                # if it is a boolean and you have the tag, enable the option
                if type(param.value) == bool:
                    param.set_value(True)
                # if it is an integer and you have the tag, change the value to the next argument
                if type(param.value) == int:
                    # if there is an argument after the current argument
                    if (i + 1) < len(args):
                        if args[i+1].isdigit():
                            if args[i+1] <= 0:
                                param.set_value(int(args[i+1]))
                            else:
                                error("Parameter '" + param.name + "' must be a positive integer")
                        else:
                            error("Parameter '" + param.name + "' must be a positive integer")
                    else:
                        error("No value specified for parameter '" + param.name + "'")
    if parameters["snakecase"].value and parameters["camelcase"].value:
        error("Snake case and camel case cannot be used at the same time")
    return parameters
def error(message : str) -> None:
    print("ERROR: " + message)
    sys.exit()

def main():
    parameters = check_arguments()
    filename = get_file()
    lines = read_lines(filename)
    write_lines(filename, lines, parameters)

main()