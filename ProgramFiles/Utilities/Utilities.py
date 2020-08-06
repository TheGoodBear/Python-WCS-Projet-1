# coding: utf-8

# import modules
import random
import os
import sys

# additional code


# functions
def GetUserInput(
    Message, 
    ValueType = "str",
    Minimum = None, 
    Maximum = None, 
    PossibleValues = None,
    DefaultValue = None,
    Trim = True,
    StringCaseSensitive = False):
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
    """

    # Do until user entry is valid (and encounter a return)
    while True:
        # ask for user entry
        MyData = input(Message)    

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
                        print(f"Merci de rentrer un nombre parmi les suivants : {PossibleValues}")
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
                        print(f"Merci de rentrer un nombre entier compris entre {'- infini' if Minimum is None else Minimum} et {'infini' if Maximum is None else Maximum}")
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
                        print(f"Merci de rentrer un nombre parmi les suivants : {PossibleValues}")
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
                        print(f"Merci de rentrer un nombre entier compris entre {'- infini' if Minimum is None else Minimum} et {'infini' if Maximum is None else Maximum}")
                else:
                    # ask again
                    print(f"Merci de rentrer un nombre entier")

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
                        print(f"Merci de rentrer un nombre parmi les suivants : {PossibleValues}")
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
                        print(f"Merci de rentrer un nombre compris entre {'- infini' if Minimum is None else Minimum} et {'infini' if Maximum is None else Maximum}")
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
                        print(f"Merci de rentrer un nombre parmi les suivants : {PossibleValues}")
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
                        print(f"Merci de rentrer un nombre compris entre {'- infini' if Minimum is None else Minimum} et {'infini' if Maximum is None else Maximum}")
                else:
                    # ask again
                    print(f"Merci de rentrer un nombre")

        if ValueType.lower() == "bool" or ValueType.lower() == "boolean":
            # expect a boolean 
            if MyData.lower() == "true" or MyData.lower() == "vrai" or MyData.lower() == "t" or  MyData == "v" or MyData.lower() == "oui" or MyData == "1":
                # user entry is True
                # return value
                return True
            elif MyData.lower() == "false" or MyData.lower() == "faux" or MyData.lower() == "f" or MyData.lower() == "non" or MyData == "0":
                # user entry is False
                # return value
                return False
            else:
                # user entry is not an expected value
                if DefaultValue == None:
                    # no default value specified, so ask again
                    print(f"Merci de rentrer un booléen (oui/vrai ou non/faux)")
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
                if not MyData in MyPossibleValues:
                    if DefaultValue == None:
                        # no default value specified, so ask again
                        print(f"Merci de rentrer une valeur parmi les suivantes : {PossibleValues}")
                    elif str(DefaultValue).lower() == "random" :
                        # draw an random value in possible values
                        MyData = PossibleValues[random.randint(0, len(PossibleValues)-1)]
                        # return value
                        return MyData
                else:
                    # value is in possible values
                    return MyData
            elif Minimum is not None or Maximum is not None:
                if ((Minimum is not None and len(MyData) < Minimum) 
                    or (Maximum is not None and len(MyData) > Maximum)):
                    # check between min and max
                    print(f"Merci de rentrer une chaine de caractères de {Minimum} à {Maximum} caractères de long")
                else:
                    # return value
                    return MyData
            elif MyData == "":
                if DefaultValue == None:
                    # no default value specified, so ask again
                    print(f"Merci de rentrer quelque chose")
                else:
                    # return default value
                    return DefaultValue
            else:
                # return value
                return MyData


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
    print(Message)
    # add to history
    MessagePrefix = ""
    if CountMessage:
        MessagePrefix = "(" + str(len(MessageList) + 1) + ") "
    # return MessageList
    return MessageList.append(MessagePrefix + Message)


# def GetSymbolName(Symbol):
#     """
#         This function retrieve the name matching the symbol
#     """
#     ReturnValue = ""

#     # check for each possible symbol
#     # should be done in a better way (dictionary ?)
#     if Symbol == Variables.RailroadSymbol[1]:
#         ReturnValue = Variables.RailroadSymbol[0]
#     elif Symbol == Variables.GarageSymbol[1]:
#         ReturnValue = Variables.GarageSymbol[0]
#     elif Symbol == Variables.WarehouseSymbol[1]:
#         ReturnValue = Variables.WarehouseSymbol[0]
#     elif Symbol.isdigit():
#         ReturnValue = Variables.CrateSymbol[0].replace("{NbCrates}", Symbol)
#     elif Symbol == Variables.EnergyPodSymbol[1]:
#         ReturnValue = Variables.EnergyPodSymbol[0]

#     return ReturnValue


# program main entry (for example to check the functions)
if __name__ == "__main__":
    ClearConsole()
    print("Test de saisie utilisateur:")
    # print(GetData("Saisir une chaine de caractères de 5 à 10 de longueur : ", Minimum=5, Maximum=10))
    # print(GetData("Saisir une chaine de caractères (avec défaut='Vide') : ", DefaultValue="Vide"))
    # print(GetData("Saisir une chaine de caractères (parmi liste) : ", PossibleValues=["Un", 2, "Trois", 4, "Cinq"]))
    # print(GetData("Saisir une chaine de caractères (parmi liste avec random) : ", PossibleValues=["Un", 2, "Trois", 4, "Cinq"], DefaultValue="random"))
    # print(GetData("Saisir un nombre entier (parmi liste) : ", ValueType="int", Minimum=5, PossibleValues=[2,4,6,8,10]))
    # print(GetData("Saisir un nombre entier > 5 : ", ValueType="int", Minimum=5))
    # print(GetData("Saisir un nombre entier entre 5 et 10 (avec défaut=8) : ", ValueType="int", Minimum=5, Maximum=10, DefaultValue=8))
    # print(GetData("Saisir un nombre entier : ", ValueType="int"))
    # print(GetData("Saisir un booléen : ", ValueType="bool"))
    # print(GetData("Saisir un booléen (avec random) : ", ValueType="bool", DefaultValue="random"))
