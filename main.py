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
    value = False
    def __init__(self, name, desc, tag, value):
        self.name = name
        self.desc = desc
        self.tag = tag
        self.value = value

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

def write_lines(filename, lines):
    filename = filename.replace(".txt", "-new.txt")
    file = open(filename, "w")
    for line in lines:
        # Replace regex items
        line = re.sub(r"\s*==\s*", " == ", line) # ==
        line = re.sub(r"\s*(?<![\!\>\<\=])\=(?![\!\>\<\=])\s*", " = ", line) # =
        line = re.sub(r"\s*\>\=(?![\!\>\<\=])\s*", " >= ", line) # >=
        line = re.sub(r"\s*\<\=(?![\!\>\<\=])\s*", " <= ", line) # <=
        line = re.sub(r"\s*\>(?![\!\>\<\=])\s*", " > ", line) # >
        line = re.sub(r"\s*\<(?![\!\>\<\=])\s*", " < ", line) # <
        line = re.sub(r"\s*\!\=(?![\!\>\<\=])\s*", " != ", line) # !=
        
        
        # If last digit is a newline and the line is 2 characters (newline and another)
        if line[-1] == '\n' and len(line) >= 2:
            # remove the spaces between the text and the newline
            line = line[0:-1].rstrip(" ") + "\n"
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
                                          False)
                 }
    for arg in args:
        for parameter in parameters:
            if parameters[parameter].tag == arg:
                parameters[parameter].value = True
    if parameters["snakecase"].value and parameters["camelcase"].value:
        error("Snake-Case and Camel-Case cannot be used at the same time")

def error(message : str) -> None:
    print("ERROR: " + message)
    sys.exit()

def main():
    check_arguments()
    filename = get_file()
    lines = read_lines(filename)
    write_lines(filename, lines)

main()