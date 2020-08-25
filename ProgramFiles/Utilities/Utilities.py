# coding: utf-8

# Imports modules
import os
import sys
import time
import random
import json
import ProgramFiles.Utilities.RichConsole as RC

# Import application code


# functions
def GetUserInput(
    Message, 
    ValueType = "str",
    Minimum = None, 
    Maximum = None, 
    PossibleValues = None,
    DefaultValue = None,
    Trim = True,
    StringCaseSensitive = False,
    SpecificErrorMessage = None,
    ErrorMessageLineOffset = 1,
    RichConsoleParameters = None):
    """
        Get an input from the user
        Entry must be of ValueType (str for any)

        Parameters :
            Message : the message to show to the user
            ValueType : type of expected value ("int", "float", "bool", "str")
            Minimum : the minimum acceptable value (for int and float) or length (for str)
            Maximum : the maximum acceptable value (for int and float) or length (for str)
            PossibleValues : the predefined possible values (superseeds Minimum and Maximum) (for int, float and str)
            DefaultValue : 
                - if None : there is no default value
                - if "Random" : draw a random value in PossibleValues or between Minimum and Maximum (for int and float) or between True and False (for bool)
                - if integer or other string set as default value
            Trim : if yes, input is trimmed (no spaces before and after) before managing
            StringCaseSensitive : if false, string comparison on lists are not case sensitive
            ErrorMessage can be defined (else default is used) with LineOffset from input

            Can optionally use RichConsole with 3 parameters in list [Line, Column, MaxColumns]
    """

    MyData = None

    # Do until user entry is valid (and encounter a return)
    while True:
        # ask for user entry

        ErrorMessage = ""

        if RichConsoleParameters is None:
            MyData = input(Message) 
        else: 
            (NbLines, LineLength) = RC.Print(
                Message, 
                RichConsoleParameters[0], 
                RichConsoleParameters[1],
                RC.Justify.Left, 
                RichConsoleParameters[2])
            RC.PlaceCursorAt(
                RichConsoleParameters[0], 
                RichConsoleParameters[1] + LineLength)
            MyData = input()

        # trim input if specified
        if Trim:
            MyData = MyData.strip()

        if ValueType.lower() == "int" or ValueType.lower() == "integer":
            # expect integer
            if (MyData.isdigit() or 
                (len(MyData) > 1 and MyData.startswith("-") and MyData[1:].isdigit())):
                # user entry is of expected type
                if PossibleValues is not None:
                    # check in possible values
                    if int(MyData) in PossibleValues:
                        # value is in possible values
                        return int(MyData)
                    elif str(DefaultValue).lower() == "random":
                        # return random value in possible values
                        return PossibleValues[random.randint(0, len(PossibleValues)-1)]
                    elif DefaultValue is not None:
                        # return default value
                        return DefaultValue
                    else:
                        # ask again
                        ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer un nombre parmi les suivants : {PossibleValues}")
                elif ((Minimum is not None and int(MyData) < Minimum) 
                    or (Maximum is not None and int(MyData) > Maximum)):
                    # not between min and max
                    if str(DefaultValue).lower() == "random":
                        # return a random number between Min and Max
                        return random.randint(Minimum, Maximum)
                    elif DefaultValue is not None:
                        # return default value
                        return DefaultValue
                    else:
                        # ask again
                        ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer un nombre entier compris entre {'- infini' if Minimum is None else Minimum} et {'infini' if Maximum is None else Maximum}")
                else:
                    # return value
                    return int(MyData)
            else:
                # user entry is not of expected type
                if PossibleValues is not None:
                    # check in possible values
                    if str(DefaultValue).lower() == "random":
                        # return random value in possible values
                        return PossibleValues[random.randint(0, len(PossibleValues)-1)]
                    elif DefaultValue is not None:
                        # return default value
                        return DefaultValue
                    else:
                        # ask again
                        ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer un nombre parmi les suivants : {PossibleValues}")
                elif Minimum is not None and Maximum is not None:
                    # if min and max
                    if str(DefaultValue).lower() == "random":
                        # return a random number between Min and Max
                        return random.randint(Minimum, Maximum)
                    elif DefaultValue is not None:
                        # return default value
                        return DefaultValue
                    else:
                        # ask again
                        ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer un nombre entier compris entre {'- infini' if Minimum is None else Minimum} et {'infini' if Maximum is None else Maximum}")
                else:
                    # ask again
                    ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer un nombre entier")

        if ValueType.lower() == "float":
            # expect any number
            if MyData.isnumeric():
                # user entry is of expected type
                if PossibleValues is not None:
                    # check in possible values
                    if float(MyData) in PossibleValues:
                        # value is in possible values
                        return float(MyData)
                    elif str(DefaultValue).lower() == "random":
                        # return random value in possible values
                        return PossibleValues[random.randint(0, len(PossibleValues)-1)]
                    elif DefaultValue is not None:
                        # return default value
                        return DefaultValue
                    else:
                        # ask again
                        ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer un nombre parmi les suivants : {PossibleValues}")
                elif ((Minimum is not None and int(MyData) < Minimum) 
                    or (Maximum is not None and int(MyData) > Maximum)):
                    # not between min and max
                    if str(DefaultValue).lower() == "random":
                        # return a random number between Min and Max
                        return random.randint(Minimum, Maximum)
                    elif DefaultValue is not None:
                        # return default value
                        return DefaultValue
                    else:
                        # ask again
                        ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer un nombre compris entre {'- infini' if Minimum is None else Minimum} et {'infini' if Maximum is None else Maximum}")
                else:
                    # return value
                    return float(MyData)
            else:
                # user entry is not of expected type
                if PossibleValues is not None:
                    # check in possible values
                    if str(DefaultValue).lower() == "random":
                        # return random value in possible values
                        return PossibleValues[random.randint(0, len(PossibleValues)-1)]
                    elif DefaultValue is not None:
                        # return default value
                        return DefaultValue
                    else:
                        # ask again
                        ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer un nombre parmi les suivants : {PossibleValues}")
                elif Minimum is not None and Maximum is not None:
                    # if min and max
                    if str(DefaultValue).lower() == "random":
                        # return a random number between Min and Max
                        return random.randint(Minimum, Maximum)
                    elif DefaultValue is not None:
                        # return default value
                        return DefaultValue
                    else:
                        # ask again
                        ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer un nombre compris entre {'- infini' if Minimum is None else Minimum} et {'infini' if Maximum is None else Maximum}")
                else:
                    # ask again
                    ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer un nombre")

        if ValueType.lower() == "bool" or ValueType.lower() == "boolean":
            # expect a boolean 
            if MyData.lower() == "true" or MyData.lower() == "vrai" or MyData.lower() == "t" or  MyData == "v" or MyData.lower() == "oui" or MyData.lower() == "o" or MyData == "1":
                # user entry is True
                # return value
                return True
            elif MyData.lower() == "false" or MyData.lower() == "faux" or MyData.lower() == "f" or MyData.lower() == "non" or MyData.lower() == "n" or MyData == "0":
                # user entry is False
                # return value
                return False
            else:
                # user entry is not an expected value
                if DefaultValue == None:
                    # no default value specified, so ask again
                    ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer un booléen (oui/vrai ou non/faux)")
                elif str(DefaultValue).lower() == "random" :
                    # draw random between True and False
                    MyData = random.randint(1, 2)
                    # return value
                    if MyData == 1:
                        return True
                    else:
                        return False
                else:
                    # return default value
                    return DefaultValue

        if  ValueType.lower() == "str" or ValueType.lower() == "string":
            # expect anything
            if PossibleValues is not None:
                # manage case sensitivity
                MyDataToCompare = MyData if StringCaseSensitive else MyData.lower()
                MyPossibleValues = (
                    [str(PossibleValue) for PossibleValue in PossibleValues] 
                    if StringCaseSensitive 
                    else [str(PossibleValue).lower() for PossibleValue in PossibleValues])
                if not MyDataToCompare in MyPossibleValues:
                    if DefaultValue == None:
                        # no default value specified, so ask again
                        ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer une valeur parmi les suivantes : {PossibleValues}")
                    elif str(DefaultValue).lower() == "random" :
                        # draw an random value in possible values
                        MyData = PossibleValues[random.randint(0, len(PossibleValues)-1)]
                        # return random value
                        return MyData
                    # else:
                    #     # return default value
                    #     return MyData
                else:
                    # value is in possible values
                    return MyData
            elif Minimum is not None or Maximum is not None:
                if ((Minimum is not None and len(MyData) < Minimum) 
                    or (Maximum is not None and len(MyData) > Maximum)):
                    # check between min and max
                    ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer une chaine de caractères de {Minimum} à {Maximum} caractères de long.")
                else:
                    # return value
                    return MyData
            elif MyData == "":
                if DefaultValue == None:
                    # no default value specified, so ask again
                    ErrorMessage = SpecificErrorMessage if SpecificErrorMessage is not None else (f"Merci de rentrer quelque chose.")
                else:
                    # return default value
                    return DefaultValue
            else:
                # return value
                return MyData

        # prints error message if any
        if ErrorMessage is not None:
            if RichConsoleParameters is None:
                print(ErrorMessage)
            else: 
                RC.Print(
                    ErrorMessage, 
                    RichConsoleParameters[0] + ErrorMessageLineOffset, 
                    RichConsoleParameters[1],
                    RC.Justify.Left, 
                    RichConsoleParameters[2])
                # if error message print on same line as input, wait 2s before asking again
                if ErrorMessageLineOffset == 0:
                    time.sleep(2)



def ManageMessageHistory(
    Message, 
    MessageList, 
    CountMessage = True):
    """
        Show a message and save it to message history
        
        Parameters :
            Message : the message to show
            MessageList : the list of all messages
            CountMessage : if true, prefix message with its order number
    """

    # print message
    # print(Message)
    # add to history
    MessagePrefix = ""
    if CountMessage:
        MessagePrefix = str(len(MessageList) + 1).rjust(4) + ") "
    # return MessageList
    return MessageList.append(MessagePrefix + Message)



def LoadJSONFile(
    Path,
    FileName):
    """
        Load a json file a return a dictionary
        .json extension is optional
    """

    MyDict = None

    # add extension if needed
    if not FileName.endswith(".json"):
        FileName += ".json"

    try:

        with open(Path + FileName, "r", encoding = "utf-8") as MyFile:
            MyDict = json.load(MyFile)

        # print(MyDict)
        return MyDict

    except FileNotFoundError:
        print(f"\nLe fichier {Path}{FileName} n'existe pas.\n")



def LoadMaps(
    Path,
    FileName):
    """
        Load map from a text file
        and return a dictionnary of 2D lists for map and blank layers

        Blank layer (for example for objects and characters) is initialized matching map dimensions
    """

    MapsData = {}
    MapData = []

    try:

        with open(Path + FileName, "r", encoding="utf-8") as MyFile:

            MapName = None
            NumberOfLines = 0
            NumberOfColumns = 0
            for Line in MyFile:
                if Line.startswith("###"):
                    # comment
                    continue
                elif Line.startswith("# "):
                    # new map
                    if MapName is not None:
                        # initialize dictionary for map
                        MapsData[MapName] = {}
                        # save current map in dictionary
                        MapsData[MapName]["Map"] = MapData
                        # initialize current map blank layer
                        BlankLayer = [["" for X in range(NumberOfColumns)] for Y in range(NumberOfLines)]
                        # add current map blank layer to dictionary
                        MapsData[MapName]["Objects"] = BlankLayer
                    # reset map data
                    MapName = Line[2:].strip()
                    MapData = []
                    NumberOfLines = 0
                    NumberOfColumns = 0
                else:
                    Columns = []
                    NumberOfColumnsInThisLine = 0
                    for Character in Line:
                        # ignore line ends
                        if Character == "\n":
                            continue
                        # add character to map
                        Columns.append(Character)
                        NumberOfColumnsInThisLine += 1
                                        
                    # add line to map
                    MapData.append(Columns)
                    # update counters
                    NumberOfLines += 1
                    NumberOfColumns = max(NumberOfColumns, NumberOfColumnsInThisLine)

        if MapName is not None:
            # initialize dictionary for map
            MapsData[MapName] = {}
            # save current map in dictionary
            MapsData[MapName]["Map"] = MapData
            # initialize blank layer
            BlankLayer = [["" for X in range(NumberOfColumns)] for Y in range(NumberOfLines)]
            # add blank layer to dictionary
            MapsData[MapName]["Objects"] = BlankLayer

        # print(MapsData)
        return MapsData
            
    except FileNotFoundError:
        print(f"\nLe fichier {Path}{FileName} n'existe pas.\n")



def LoadViews(
    Path,
    FileName):
    """
        Load views from a text file
        and return a dictionary of views with list of lines

        # <ViewName> marks a new view
        ### marks a comment (ignore line)
    """

    Views = {}

    try:
        
        with open(Path + FileName, "r", encoding="utf-8") as MyFile:
            ViewName = ""
            ViewLines = []
        
            for Line in MyFile:
                if Line.startswith("###"):
                    # comment
                    continue
                elif Line.startswith("# "):
                    # new view
                    if ViewName != "":
                        # save current view in dictionary
                        Views[ViewName] = ViewLines
                    # reset view data
                    ViewName = Line[2:].strip()
                    ViewLines = []
                else:
                    # add line to ViewLines
                    ViewLines.append(Line.replace("\n", ""))         

        if ViewName != "":
            # save last view
            Views[ViewName] = ViewLines
        
        # print(Views)
        return Views

    except FileNotFoundError:
        print(f"\nLe fichier {Path}{FileName} n'existe pas.\n")



# program main entry (for example to check the functions)
if __name__ == "__main__":
    ClearConsole()
    print("Test de saisie utilisateur:")
    print(GetData("Saisir une chaine de caractères de 5 à 10 de longueur : ", Minimum=5, Maximum=10))
    print(GetData("Saisir une chaine de caractères (avec défaut='Vide') : ", DefaultValue="Vide"))
    print(GetData("Saisir une chaine de caractères (parmi liste) : ", PossibleValues=["Un", 2, "Trois", 4, "Cinq"]))
    print(GetData("Saisir une chaine de caractères (parmi liste avec random) : ", PossibleValues=["Un", 2, "Trois", 4, "Cinq"], DefaultValue="random"))
    print(GetData("Saisir un nombre entier (parmi liste) : ", ValueType="int", Minimum=5, PossibleValues=[2,4,6,8,10]))
    print(GetData("Saisir un nombre entier > 5 : ", ValueType="int", Minimum=5))
    print(GetData("Saisir un nombre entier entre 5 et 10 (avec défaut=8) : ", ValueType="int", Minimum=5, Maximum=10, DefaultValue=8))
    print(GetData("Saisir un nombre entier : ", ValueType="int"))
    print(GetData("Saisir un booléen : ", ValueType="bool"))
    print(GetData("Saisir un booléen (avec random) : ", ValueType="bool", DefaultValue="random"))
