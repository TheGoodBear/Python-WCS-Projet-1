# coding: utf-8

"""
    Rich Console
    Inspired by http://www.jchr.be/python/ecma-48.htm
    Allows basic formatting of console text (via print) based on ECMA-48 standard
    
    You can :
        - print a text with foreground and background color tags at a specific line/column position
        - clears the screen
        - show and hide cursor
    
        Possible enhancements :
        - place cursor at specific line/column
        - move cursor up, down, left or right n times
        - insert or remove n lines at cursor position
        - define scroll area from line start to line end
        - save and recall cursor position
"""

# import modules
import os
import sys
import time
from enum import Enum

# protected variables, constants and enums
# _RichConsoleEnabled = False

class Format(Enum):
    Prefix = "\033["
    ForegroundPrefix = "3"
    BackgroundPrefix = "4"
    Reset = "0m"
    StyleAndColorSuffix = "m"
    PositionSuffix = "H"
    ClearScreen = "2J"
    CursorVisible = "?25h"
    CursorInvisible = "?25l"

class Style(Enum):
    Bold = {"Tag" : "SB", "Format" : "1"}         # note that this is very subtile to see...
    Underline = {"Tag" : "SU", "Format" : "4"}
    Inverse = {"Tag" : "SI", "Format" : "7"}

class Color(Enum):
    Black = {"Tag" : "B", "Format" : "0"}
    Red = {"Tag" : "R", "Format" : "1"}
    Green = {"Tag" : "G", "Format" : "2"}
    Yellow = {"Tag" : "Y", "Format" : "3"}
    Blue = {"Tag" : "U", "Format" : "4"}
    Magenta = {"Tag" : "M", "Format" : "5"}
    Cyan = {"Tag" : "C", "Format" : "6"}
    White = {"Tag" : "W", "Format" : "7"}

class PrintSpeed(Enum):     # in ms
    Instant = 0
    VeryFast = .02
    Fast = .05
    Normal = .1
    Slow = .2
    VerySlow = .4


# functions
def ClearConsole():
    """
        Clear the console depending on OS
    """

    if "win" in sys.platform.lower():
        # for windows
        os.system("cls")
    elif "linux" in sys.platform.lower():
        # for linux
        os.system("clear")


# def _EnableRichconsole():
#     """
#         Enable rich console formatting
#         If not done before applying formatting it does not work (at least on windows)
#     """
#     global _RichConsoleEnabled
#     _RichConsoleEnabled = True
#     os.system("color 00")   # change console background color (in hexa)


def ShowCursor(
    IsVisible = True):
    """
        Show or hide cursor
    """
    # if (not _RichConsoleEnabled):
    #     _EnableRichconsole()

    print(
        f"{Format.Prefix.value}{Format.CursorVisible.value if IsVisible else Format.CursorInvisible.value}", 
        end = "", 
        flush = True)


def _ManageColorTags(
    Text):
    """
        Replaces color tags with appropriate formatting syntax in text

        Tags have following syntax
            [Foreground color tag;Background color tag;Style]
            ; between foreground color and background color is mandatory
            ; before style is optional if style is omitted
            if one color is ommited it remains the same
            if both colors are omitted, they reset to console default
            possible tags for colors are :
            B - Black
            R - Red
            G - Green
            Y - Yellow
            U - Blue
            M - Magenta
            C - Cyan
            W - White
            possible tags for styles are :
            SB - Bold (this is very subtile to see)
            SU - Underline
            SI - Inverted (foreground and background colors)
    """

    NextTag = _FindTagInString(Text)
    while (NextTag[0] >= 0):
        if (NextTag[1] != "" and NextTag[2] != ""):
            # Replace tag
            # Text = Text[0:NextTag[0]] + NextTag[2] + Text[0:NextTag[0]+len(NextTag[1])]
            Text = Text.replace(NextTag[1], NextTag[2])
        NextTag = _FindTagInString(Text, NextTag[0])

    return Text


def _FindTagInString(
    OriginalString,
    SearchStart = 0):
    """
        Replaces color tags in OriginalString by appropriate formattings

        Tags have following syntax
            [Foreground color tag;Background color tag;Style]
            ; between foreground color and background color is mandatory
            ; before style is optional if style is omitted
            if one color is ommited it remains the same
            if both colors are omitted, they reset to console default
            possible tags for colors are :
            B - Black
            R - Red
            G - Green
            Y - Yellow
            U - Blue
            M - Magenta
            C - Cyan
            W - White
            possible tags for styles are :
            SB - Bold (this is very subtile to see)
            SU - Underline
            SI - Inverted (foreground and background colors)
    """
    
    TagInString = ""
    TagReplacement = ""

    TagStart = OriginalString.find("[", SearchStart)
    TagEnd = OriginalString.find("]", TagStart) + 1
    TagInString = OriginalString[TagStart:TagEnd].upper()
    TagValues = TagInString.replace("[","").replace("]","").split(";")

    if (TagStart >= 0):
        # Possible tag detected
        if (TagStart >= 0 and TagEnd >= TagStart 
            and ((len(TagValues) == 2 and len(TagInString) >= 3 and len(TagInString) <= 5)
                or (len(TagValues) == 3 and len(TagInString) >= 6 and len(TagInString) <= 8))):
            # Tag seems valid

            # Get colors
            ForegroundColor = TagValues[0]
            BackgroundColor = TagValues[1]
            # Get style if provided
            FormatStyle = TagValues[2] if len(TagValues) == 3 else ""
            
            # Apply formatting
            if ((ForegroundColor == "" or ForegroundColor in [MyColor.value["Tag"] for MyColor in Color]) 
               and (BackgroundColor == "" or BackgroundColor in [MyColor.value["Tag"] for MyColor in Color])):
                # Colors are valid
                if (ForegroundColor == "" and BackgroundColor == ""):
                    # Reset to default
                    TagReplacement = f"{Format.Prefix.value}{Format.Reset.value}"
                elif (ForegroundColor == ""):
                    # Change only background color
                    TagReplacement = f"{Format.Prefix.value}{Format.BackgroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == BackgroundColor][0]}{Format.StyleAndColorSuffix.value}"
                elif(BackgroundColor == ""):
                    # Change only foreground color
                    TagReplacement = f"{Format.Prefix.value}{Format.ForegroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == ForegroundColor][0]}{Format.StyleAndColorSuffix.value}"
                else:
                    # Change both colors
                    TagReplacement = f"{Format.Prefix.value}{Format.ForegroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == ForegroundColor][0]};{Format.BackgroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == BackgroundColor][0]}{Format.StyleAndColorSuffix.value}"

            if (FormatStyle in [MyStyle.value["Tag"] for MyStyle in Style]):
                # Style is valid
                TagReplacement += f"{Format.Prefix.value}{[MyStyle.value['Format'] for MyStyle in Style if MyStyle.value['Tag'] == FormatStyle][0]}{Format.StyleAndColorSuffix.value}"

            if (TagReplacement != ""):
                # return formatting
                return (TagStart, TagInString, TagReplacement)

            return (TagStart + 1, "", "")

        return (TagStart + 1, "", "")
    else:
        return (-1, "", "")


def Print(
    Text = "", 
    Line = None, 
    Column = None, 
    Speed = PrintSpeed.Instant,
    ClearScreenBefore = False, 
    JumpLineAfter = True,
    MakeBeep = False):
    """
        Print rich text
        
        Absolute line and/or column position can be specified
        Speed can be specified (from PrintSpeed enum)
        Optionally clears screen before printing
        
        Text can contain tags to change colors during printing with following syntax
        Tags have following syntax
            [Foreground color tag;Background color tag;Style]
            ; between foreground color and background color is mandatory
            ; before style is optional if style is omitted
            if one color is ommited it remains the same
            if both colors are omitted, they reset to console default
            possible tags for colors are :
            B - Black
            R - Red
            G - Green
            Y - Yellow
            U - Blue
            M - Magenta
            C - Cyan
            W - White
            possible tags for styles are :
            SB - Bold (this is very subtile to see)
            SU - Underline
            SI - Inverted (foreground and background colors)
    """
    # if (not _RichConsoleEnabled):
    #     _EnableRichconsole()

    if (ClearScreenBefore):
        ClearConsole()
        # print(
        #     f"{__FormatPrefix}{__ClearScreen}",
        #     end = "")

    # define jumping lines after printing
    PrintEnd = "\n" if JumpLineAfter else ""

    # replace tags by appropriate color codes
    Text = _ManageColorTags(Text)

    if (Line is None and Column is None):
        # no positioning
        pass
    elif (not str(int(Line)).isdigit() or not str(int(Column)).isdigit()):
        # position error
        print("*** PrintAt : line and/or column have invalid values")
        return ""
    else:
        # define position
        print(
            f"{Format.Prefix.value}{int(Line)};{int(Column)}{Format.PositionSuffix.value}",
            end = "")

    # print text
    PrintText(Text, Speed, PrintEnd, MakeBeep)


def PrintText(
    Text,
    Speed,
    PrintEnd = "\n",
    MakeBeep = False):
    """
        Print specified text at defined speed (from PrintSpeed enum)
    """
    
    # make a beep
    BeepString = "" if not MakeBeep else "\a"

    # print text
    if(Speed == PrintSpeed.Instant):
        print(BeepString + Text, end = PrintEnd, flush = True)
    else:
        for Letter in list(Text):
            print(BeepString + Letter, end = "", flush = True)
            time.sleep(Speed.value)
        print("", end = PrintEnd, flush = True)



# code to test rich console functions
if __name__ == "__main__":

    # variables
    PosX = 10
    PosY = 7
    Shape = "<-O->"
    ShapeColor = "[G;]"
    FullShape = ShapeColor + Shape + "[;]"

    # functions
    def PrintData():
        Print(
            "[C;U] Test des fonctionnalités de RichConsole [;]",
            1, 1,
            PrintSpeed.VeryFast,
            ClearScreenBefore = True,
            MakeBeep = True)
        Print(
            f"\nUn {FullShape} va se déplacer sur l'écran")

    def PrintShape():
        Print(
            FullShape, 
            PosY, PosX, 
            JumpLineAfter = False)

    def MoveShape(DeltaX, DeltaY, XMoveSleep = .02, YMoveSleep = .07):
        global PosX, PosY
        # delete shape at previous position
        Print(
            "".ljust(len(Shape)), 
            PosY, PosX, 
            JumpLineAfter = False)
        # calculate new shape position
        PosX += DeltaX
        PosY += DeltaY
        # draw shape at new position
        PrintShape()
        # wait
        SleepTime = XMoveSleep
        if (DeltaY != 0):
            SleepTime = YMoveSleep
        time.sleep(SleepTime)

    # code
    input("\nTaper Entrée... ")

    PrintData()
    PrintShape()
    ShowCursor(False)
    Print("[;Y;SU]Entrée pour démarrer[;]", 5, 1)
    Print("-----------------------------------------", 28, 1)
    input()

    while (PosX <= 50):
        MoveShape(1, 0)
    while (PosY <= 25):
        MoveShape(0, 1)
    while (PosX >= 11):
        MoveShape(-1, 0)
    while (PosY >= 8):
        MoveShape(0, -1)
    while (PosY <= 20):
        MoveShape(1, .5)

    Print(
        "[;]Et voilà, [U;]un [G;]petit [R;]tour[;] et c'est fini [Y;]:-)[;]",
        Line = 29, Column = 1)
    Print("À [U;]pluche[;] !")
    ShowCursor()

    print("...\n")
