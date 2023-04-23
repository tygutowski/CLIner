import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import sys
import re

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
    
class Application:
    parameters = {}
    filename = ""
    def __init__(self):
        self.check_arguments()
    def read_lines(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        return lines
    def error(self, message : str) -> None:
        print("ERROR: " + message)
        sys.exit()


    def write_lines(self, filename, lines, parameters):
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
    def check_arguments(self):
        args = sys.argv
        self.parameters = {"snakecase" : Parameter("snakecase",
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
            for parameter in self.parameters:
                param = self.parameters[parameter]
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
        if self.parameters["snakecase"].value and self.parameters["camelcase"].value:
            error("Snake case and camel case cannot be used at the same time")
        
    
    
    def get_file(self):
        tk.Tk().withdraw()
        self.filename = filedialog.askopenfilename()
    
    def clean_file(self):
        if self.filename:
            lines = self.read_lines(self.filename)
            self.write_lines(self.filename, lines, self.parameters)
        else:
            print("no file defined")

    def gui(self):
        root = tk.Tk()
        root.geometry("300x200") # Set the window size
        root.configure(bg="gray") # Set the background color to gray

        # Create a label and text box
        label = ttk.Label(root, text="Enter text:")
        label.pack()
        textbox = ttk.Entry(root)
        textbox.pack()
        
        
        
        custom_theme = ttk.Style()
        custom_theme.theme_create("custom_theme", parent="alt", settings={
            "TButton": {
                "configure": {"background": "#36393e", "foreground": "#ffffff", "font": ('Consolas', 12)},
                "map": {"background": [("active", "#424549"), ("disabled", "#999999")], "foreground": [("disabled", "#ffffff")]}
            }
        })
        custom_theme.theme_use("custom_theme")


        
        # Create two buttons
        button1 = ttk.Button(root, text="Button 1", command=self.get_file, style = "TButton", takefocus = False)
        button1.pack(side=tk.LEFT, padx=5, pady=10)
        button2 = ttk.Button(root, text="Button 2", command=self.clean_file, style = "TButton", takefocus = False)
        button2.pack(side=tk.RIGHT, padx=5, pady=10)

        root.mainloop()

def main():
    app = Application()
    app.gui()

main()