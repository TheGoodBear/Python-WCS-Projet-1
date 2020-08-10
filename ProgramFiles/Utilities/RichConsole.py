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
    MoveUpSuffix = "A"
    MoveDownSuffix = "B"
    MoveRightSuffix = "C"
    MoveLeftSuffix = "D"
    ClearScreen = "2J"
    CursorVisible = "?25h"
    CursorInvisible = "?25l"

class Style(Enum):
    Bold = {"Tag" : "SB", "Format" : "1"}         # note that this is very subtle to see...
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

class Justify(Enum):
    Left = 0
    Center = 1
    Right = 2

class PrintSpeed(Enum):     # in ms
    Instant = 0
    UltraFast = .01
    VeryFast = .02
    Fast = .04
    Medium = .08
    Slow = .15
    VerySlow = .3


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


def ShowCursor(
    IsVisible = True):
    """
        Show or hide cursor
    """

    print(
        f"{Format.Prefix.value}{Format.CursorVisible.value if IsVisible else Format.CursorInvisible.value}", 
        end = "", 
        flush = True)

    time.sleep(.01)


def _ManageTags(
    Text):
    """
        Create a list of formatting tags
        Returns Text without formatting and a dictionary of formats
    """

    RawText = ""
    NumberOfCharactersToJump = 0
    FormatDict = {}

    # for each character in text
    for Index, Character in enumerate(Text):
        
        if NumberOfCharactersToJump > 0:
            # jump the characters forming the last tag
            NumberOfCharactersToJump -= 1
            continue

        if Character == "[":
            # possible tag start

            TagEnd = Text.find("]", Index) + 1
            TagInString = Text[Index:TagEnd].upper()
            TagValues = TagInString.replace("[","").replace("]","").split(";")

            # possible tag detected
            if (TagEnd >= 1 
                and ((len(TagValues) == 2 and len(TagInString) >= 3 and len(TagInString) <= 5)
                    or (len(TagValues) == 3 and len(TagInString) >= 6 and len(TagInString) <= 8))):
                # tag seems valid

                # get colors
                ForegroundColor = TagValues[0]
                BackgroundColor = TagValues[1]
                # get style if provided
                FormatStyle = TagValues[2] if len(TagValues) == 3 else ""

                # get format string                
                FormatString = None
                if ((ForegroundColor == "" or ForegroundColor in [MyColor.value["Tag"] for MyColor in Color]) 
                and (BackgroundColor == "" or BackgroundColor in [MyColor.value["Tag"] for MyColor in Color])):
                    # colors are valid
                    if ForegroundColor == "" and BackgroundColor == "":
                        # reset to default
                        FormatString = f"{Format.Prefix.value}{Format.Reset.value}"
                    elif ForegroundColor == "":
                        # change only background color
                        FormatString = f"{Format.Prefix.value}{Format.BackgroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == BackgroundColor][0]}{Format.StyleAndColorSuffix.value}"
                    elif BackgroundColor == "":
                        # change only foreground color
                        FormatString = f"{Format.Prefix.value}{Format.ForegroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == ForegroundColor][0]}{Format.StyleAndColorSuffix.value}"
                    else:
                        # change both colors
                        FormatString = f"{Format.Prefix.value}{Format.ForegroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == ForegroundColor][0]};{Format.BackgroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == BackgroundColor][0]}{Format.StyleAndColorSuffix.value}"

                if FormatStyle in [MyStyle.value["Tag"] for MyStyle in Style]:
                    # add style
                    FormatString += f"{Format.Prefix.value}{[MyStyle.value['Format'] for MyStyle in Style if MyStyle.value['Tag'] == FormatStyle][0]}{Format.StyleAndColorSuffix.value}"

                if FormatString != "":
                    # add formatting to dictionary with position as key
                    FormatDict[len(RawText)] = FormatString
                    NumberOfCharactersToJump = len(TagInString) - 1

            else:
                # not a valid tag
                # add character to raw text
                RawText += Character

        else:
            # not tag
            # add character to raw text
            RawText += Character
    
    return (RawText, FormatDict)


def _WrapText(
    Text,
    FormatDict,
    JustifyText,
    MaxColumns,
    MaxLines):
    """
        Split text in lines so it fits in specified area (MaxColumns and MaxLines)
        while keeping formatting (via FormatDict)
    """

    TextLines = []
    CurrentCharacterIndex = 0
    CurrentLine = ""
    RemainingText = Text

    while len(RemainingText) > 0:

        if MaxColumns is not None:
            # a square is specified

            WrapPosition = RemainingText.rfind(" ", 0, MaxColumns + 1) 
            if WrapPosition == -1:
                # no more wrapping
                CurrentLine = RemainingText
                RemainingText = ""
            else:
                # line wrapped
                CurrentLine = RemainingText[:WrapPosition]
                RemainingText = RemainingText[WrapPosition:].lstrip()
                # adjust format indexes to compensate previous lstrip
                FormatDict = {
                    (Index - 1 
                    if Index > CurrentCharacterIndex + len(CurrentLine)
                    else Index)
                    :Value
                    for Index, Value 
                    in FormatDict.items() 
                    }
        else:
            # no wrapping
            CurrentLine = RemainingText
            RemainingText = ""

        if MaxColumns is not None:
            # justify text
            CharactersBefore = 0
            CharactersAfter = 0
            if JustifyText == Justify.Left:
                CharactersAfter = MaxColumns - len(CurrentLine)
                # adjust format indexes to compensate justifying
                FormatDict = {
                    (Index + CharactersAfter 
                    if Index > CurrentCharacterIndex
                    else Index)
                    :Value
                    for Index, Value 
                    in FormatDict.items() 
                    }
                CurrentLine = CurrentLine.ljust(MaxColumns)
            if JustifyText == Justify.Right:
                CharactersBefore = MaxColumns - len(CurrentLine)
                # adjust format indexes to compensate justifying
                FormatDict = {
                    (Index + CharactersBefore 
                    if Index > CurrentCharacterIndex + CharactersBefore
                    else Index)
                    :Value
                    for Index, Value 
                    in FormatDict.items() 
                    }
                CurrentLine = CurrentLine.rjust(MaxColumns)
            elif JustifyText == Justify.Center:
                Characters = (MaxColumns - len(CurrentLine)) // 2
                CharactersBefore = Characters if Characters % 2 == 0 else Characters + 1
                CharactersAfter = Characters
                # adjust format indexes to compensate justifying
                FormatDict = {
                    (Index + CharactersBefore 
                    if Index > CurrentCharacterIndex
                    else Index)
                    :Value
                    for Index, Value 
                    in FormatDict.items() 
                    }
                FormatDict = {
                    (Index + CharactersAfter 
                    if Index > CurrentCharacterIndex + len(CurrentLine) + CharactersBefore
                    else Index)
                    :Value
                    for Index, Value 
                    in FormatDict.items() 
                    }
                CurrentLine = CurrentLine.center(MaxColumns)

        TextLines.append(CurrentLine)
        CurrentCharacterIndex += len(CurrentLine)

    return (TextLines, FormatDict)


def Print(
    Text = "", 
    Line = None, 
    Column = None, 
    JustifyText = Justify.Left,
    MaxColumns = None,
    MaxLines = 1,
    Speed = PrintSpeed.Instant,
    ClearScreenBefore = False, 
    JumpLineAfter = True,
    MakeBeep = False):
    """
        Print rich text
        
        Absolute line and/or column position can be specified
        Can be justify in a square (MaxColumns/MaxLines) with word wrap (from Justify enum)
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
            SB - Bold (this is very subtle to see)
            SU - Underline
            SI - Inverted (foreground and background colors)
    """
    # if (not _RichConsoleEnabled):
    #     _EnableRichconsole()

    if ClearScreenBefore:
        ClearConsole()
        # print(
        #     f"{__FormatPrefix}{__ClearScreen}",
        #     end = "")

    # to make a beep
    BeepString = "" if not MakeBeep else "\a"

    # remove tags from text and get format dictionary
    (Text, FormatDict) = _ManageTags(Text)

    # wrap text to fit in specified area
    (TextLines, FormatDict) = _WrapText(Text, FormatDict, JustifyText, MaxColumns, MaxLines)

    CurrentCharacterIndex = 0
    for LineIndex, CurrentLine in enumerate(TextLines):
        if LineIndex == 0:
            # absolute positioning
            if Line is None and Column is None:
                # no positioning
                pass
            elif not str(int(Line)).isdigit() or not str(int(Column)).isdigit():
                # position error
                print("*** PrintAt : line and/or column have invalid values")
                return ""
            else:
                # define position
                print(
                    f"{Format.Prefix.value}{int(Line)};{int(Column)}{Format.PositionSuffix.value}",
                    end = "")
            LastLineLength = len(CurrentLine)
        else:
            # move cursor 1 line below
            MoveCursorString = f"{Format.Prefix.value}1{Format.MoveDownSuffix.value}"
            # move cursor left is appropriate
            if Column is not None and str(int(Column)).isdigit():
                MoveCursorString += f"{Format.Prefix.value}{LastLineLength}{Format.MoveLeftSuffix.value}"
            print(MoveCursorString, end = "")

        # print text
        # if Speed == PrintSpeed.Instant:
        #     print(BeepString + Text, end = "", flush = True)
        # else:
        for Letter in CurrentLine:
            # print formatting if any at this position
            
            if CurrentCharacterIndex in FormatDict:
                print(
                    FormatDict.pop(CurrentCharacterIndex), 
                    end = "", flush = True)
            # print letter
            print(BeepString + Letter, end = "", flush = True)
            CurrentCharacterIndex += 1
            # wait
            time.sleep(Speed.value)
            
        print("", end = "", flush = True)

        # exit loop if text exceeds square
        if LineIndex + 1 == MaxLines:
            if len(FormatDict) > 0:
                # reset format if any formatting
                print(
                    f"{Format.Prefix.value}{Format.Reset.value}", 
                    end = "", 
                    flush = True)
            break

    # jump line after printing if needed
    if JumpLineAfter:
        print()



# code to test rich console functions
if __name__ == "__main__":

    import timeit

    # variables
    PosX = 10
    PosY = 17
    Shape = "<-O->"
    ShapeColor = "[G;]"
    FullShape = ShapeColor + Shape + "[;]"

    # functions
    def TestIntro():
        Print(
            "[C;U] Test des fonctionnalités de RichConsole [;]",
            1, 1,
            Speed = PrintSpeed.VeryFast,
            ClearScreenBefore = True,
            MakeBeep = True)
        time.sleep(1)

    def CursorTest():
        ShowCursor(True)
        Print(
            "Curseur visible",
            3, 1,
            Speed = PrintSpeed.Medium)
        ShowCursor(False)
        time.sleep(1)
        Print(
            "Curseur invisible",
            3, 30,
            Speed = PrintSpeed.Medium)

    def SquareTest():
        Print(
            "Texte dans un rectangle : 'Ce texte s'imprime centré dans un rectangle de 15x5 (avec une marge de 1 caractère à gauche et à droite).",
            5, 0)
        Print(
            "┌─────────────────┐ │                 │ │                 │ │                 │ │                 │ │                 │ └─────────────────┘",
            6, 5,
            MaxColumns = 19,
            MaxLines = 7)
        Print(
            "Ce texte s'imprime [Y;]justifié à gauche[;] dans un rectangle de 15x5 (avec une marge de 1 caractère à gauche et à droite).",
            7, 7,
            JustifyText = Justify.Left,
            MaxColumns = 15,
            MaxLines = 5,
            Speed = PrintSpeed.UltraFast)

        Print(
            "┌─────────────────┐ │                 │ │                 │ │                 │ │                 │ │                 │ └─────────────────┘",
            6, 25,
            MaxColumns = 19,
            MaxLines = 7)
        ShowCursor()
        Print(
            "[M;]Ce texte s'imprime [Y;]centré[M;] dans un rectangle de 15x5 (avec une marge de 1 caractère à gauche et à droite).[;]",
            7, 27,
            JustifyText = Justify.Center,
            MaxColumns = 15,
            MaxLines = 5,
            Speed = PrintSpeed.UltraFast)
        ShowCursor(False)

        Print(
            "┌─────────────────┐ │                 │ │                 │ │                 │ │                 │ │                 │ └─────────────────┘",
            6, 45,
            MaxColumns = 19,
            MaxLines = 7)
        Print(
            "Ce texte s'imprime [Y;]justifié à droite[;] dans un rectangle de 15x5 (avec une marge de 1 caractère à gauche et à droite).",
            7, 47,
            JustifyText = Justify.Right,
            MaxColumns = 15,
            MaxLines = 5,
            Speed = PrintSpeed.UltraFast)


    def AnimationTest():
        Print(
            f"\nUn {FullShape} va se déplacer sur l'écran",
            13, 0)
        PrintShape()
        Print("[B;Y;SU] Entrée pour démarrer [;]", 15, 0)
        Print("---------------------------------------------------", 28, 0)
        input()
        while PosX <= 40:
            MoveShape(1, 0)
        while PosY <= 25:
            MoveShape(0, 1)
        while PosX >= 3:
            MoveShape(-1, 0)
        while PosY >= 18:
            MoveShape(0, -1)
        while PosY <= 25:
            MoveShape(1, .5)

    def TestEnd():
        Print(
            "[;]Et voilà, [U;]un [G;]petit [R;]tour[;] et c'est fini [Y;]:-)[;]",
            Line = 29, Column = 1)
        Print("À [U;]pluche[;] !")
        ShowCursor()
        print("...\n")

    def PrintShape():
        Print(
            FullShape, 
            PosY, PosX, 
            JumpLineAfter = False)

    def MoveShape(DeltaX, DeltaY, XMoveSleep = .01, YMoveSleep = .05):
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
        if DeltaY != 0:
            SleepTime = YMoveSleep
        time.sleep(SleepTime)

    # code
    input("\nTaper Entrée pour démarrer la démo... ")
    TestIntro()
    CursorTest()
    # ClearConsole()
    # StartTime = time.time()
    SquareTest()
    # EndTime = time.time()
    # print("\n\nTemps pour le test Square : ", EndTime - StartTime)
    AnimationTest()
    TestEnd()