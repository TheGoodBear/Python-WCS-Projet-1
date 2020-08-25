# coding: utf-8

# Imports modules
import time
import random

# Import application code
import ProgramFiles.Variables as Var
import ProgramFiles.Utilities.Utilities as Util
import ProgramFiles.Utilities.RichConsole as RC
import ProgramFiles.Game as Game


# Functions
def StartChallenge():
    """
        Manage challenge 2 (Cesar code)
    """

    TextVP = Var.GameData["ViewPorts"]["Challenge"]["Text"]
    AskVP = Var.GameData["ViewPorts"]["Challenge"]["Ask"]

    # # activate random letter
    # SwitchLetter(chr(97 + random.randint(0, 25)))

    # clean text area
    RC.ClearConsole(
        TextVP["Y"], TextVP["X"], 
        TextVP["Width"], TextVP["Height"])
    LineOffset = 0

    # print start message
    Message = (
        "\n\n[;;SI]" 
        + Var.CurrentChallengeData["EncryptedCredo"]
        + "[;]\n\n" 
        + Var.MessagesData["Challenge2"]["Start"] 
        + "\n\n")
    LineOffset += RC.Print(Message,          
        TextVP["Y"] + LineOffset, TextVP["X"],
        JustifyText = RC.Justify.Center, 
        MaxColumns = TextVP["Width"])[0]
        
    # ask crypted name
    RC.ShowCursor()
    ProposedName = Util.GetUserInput(
        Var.MessagesData["Challenge2"]["AskUser"],
        SpecificErrorMessage = Var.MessagesData["Challenge2"]["UserAnswerEmpty"],
        RichConsoleParameters = [TextVP["Y"] + LineOffset, TextVP["X"], TextVP["Width"]])
    RC.ShowCursor(False)

    Message = ""

    # check answer
    if ProposedName.lower() == Var.CurrentChallengeData["EncryptedPlayerName"]:
        # good answer
        # challenge won

        RC.ClearConsole(
            TextVP["Y"], TextVP["X"], 
            TextVP["Width"], TextVP["Height"])
        LineOffset = 0
        # show message
        Message += "\n\n" + Var.MessagesData["Challenge2"]["Success"] + "\n\n"
        LineOffset += RC.Print(Message,          
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = TextVP["Width"])[0]

        # switch off letter
        SwitchLetter(Var.CurrentChallengeData["CurrentLetter"], False)
        # change grid data
        for LineNumber, Line in enumerate(Var.MapLayer):
            for ColumnNumber in range(len(Line)):
                if Var.MapLayer[LineNumber][ColumnNumber] == "6":
                    # replace grid by land
                    Var.MapLayer[LineNumber][ColumnNumber] = " "
                    # refresh map
                    Game.ShowMap(LineNumber, ColumnNumber)
        # change letters message and event
        for AsciiCode in range(97, 123):
            Var.MapElementsData[chr(AsciiCode)]["Behaviors"]["Event"] = None
            Var.MessagesData[chr(AsciiCode)]["CantMoveOn"] = Var.MessagesData["Challenge2"]["DeactivatedLetter"]
        # free key
        Var.ObjectsData["SilverKey"]["Behaviors"]["Pickable"] = True
        # close challenge
        Var.CurrentChallengeData["Won"] = True

        # show credo
        Message += Var.MessagesData["Challenge2"]["Credo"]
        LineOffset += RC.Print(Message,          
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = TextVP["Width"],
            Speed = RC.PrintSpeed.Fast)[0]


    else:
        # wrong answer
        RC.ClearConsole(
            TextVP["Y"], TextVP["X"], 
            TextVP["Width"], TextVP["Height"])
        LineOffset = 0
        # show message
        Message += (
            "\n\n[;;SI]" 
            + Var.CurrentChallengeData["EncryptedCredo"]
            + "[;]\n\n" 
            + Var.MessagesData["Challenge2"]["Failure"])
        LineOffset += RC.Print(Message,          
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = TextVP["Width"])[0]

            

def SwitchLetter(
    Letter = None,
    SwitchOn = True):
    """
        Switch on/off specified letter
        Define it as current if on
    """

    # find letter position in map
    CurrentLetterPosition = None
    for LineIndex, Line in enumerate(Var.MapLayer):
        if Letter in Line:
            CurrentLetterPosition = (LineIndex, Line.index(Letter))
            break
        
    # get map element data for current letter
    # MapElement = Var.MapElementsData[CurrentLetterPosition[0]][CurrentLetterPosition[1]]
    MapElement = Var.MapElementsData[Letter]
    Style = (
        Var.CurrentChallengeData["SelectedLetterStyle"] 
        if SwitchOn 
        else MapElement["Style"])

    # draw
    RC.Print(
        f"{Style}{MapElement['Image']}[;]",
        Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["Y"] + CurrentLetterPosition[0],
        Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["X"] + CurrentLetterPosition[1],
        JumpLineAfter = False)

    if SwitchOn:
        # save new letter
        Var.GameData["Challenge2"]["CurrentLetter"] = Letter

        # encrypt credo and player name
        Var.CurrentChallengeData["EncryptedCredo"] = Encrypt(
            Var.MessagesData["Challenge2"]["OriginalCredo"],
            ord(Letter) - 96).replace(",", "\n")
        Var.CurrentChallengeData["EncryptedPlayerName"] = Encrypt(
            Var.Player["Name"],
            ord(Letter) - 96).lower()



def Encrypt(
    Message,
    Offset):
    """
        Encrypt specified message with specified offset on ASCII code
        and return result
    """

    EncryptedMessage = ""

    # for each character in message
    for Char in Message:
        EncryptedChar = ""
        
        if ord(Char) >= 65 and ord(Char) <= 90:
            # upper case letter
            EncryptedChar = (
                chr(ord(Char) + Offset) 
                if ord(Char) + Offset <= 90 
                else chr(ord(Char) + Offset - 26))
        elif ord(Char) >= 97 and ord(Char) <= 122:
            # upper case letter
            EncryptedChar = (
                chr(ord(Char) + Offset) 
                if ord(Char) + Offset <= 122 
                else chr(ord(Char) + Offset - 26))
        else:
            # other character, keep it
            EncryptedChar = Char

        # updated encrypted message
        EncryptedMessage += EncryptedChar

    # return encrypted message
    return EncryptedMessage
