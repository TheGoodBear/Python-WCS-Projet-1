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
    MoveLeftSuffix = "C"
    MoveRightSuffix = "D"
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

class Justify(Enum):
    Left = 0
    Center = 1
    Right = 2

class PrintSpeed(Enum):     # in ms
    Instant = 0
    VeryFast = .02
    Fast = .05
    Normal = .1
    Slow = .2
    VerySlow = .4

class _TagAction(Enum):
    Replace = 0
    Remove = 1


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
    Text,
    Action = _TagAction.Replace):
    """
        Replaces (or remove) color tags with appropriate formatting syntax in text

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
    # while they are tags in text
    while NextTag[0] >= 0:
        
        if NextTag[1] != "" and NextTag[2] != "":
            # replace or remove tag
            if Action == _TagAction.Remove:
                Text = Text.replace(NextTag[1], "")
            elif Action == _TagAction.Replace:
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

    if TagStart >= 0:
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
                if ForegroundColor == "" and BackgroundColor == "":
                    # Reset to default
                    TagReplacement = f"{Format.Prefix.value}{Format.Reset.value}"
                elif ForegroundColor == "":
                    # Change only background color
                    TagReplacement = f"{Format.Prefix.value}{Format.BackgroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == BackgroundColor][0]}{Format.StyleAndColorSuffix.value}"
                elif BackgroundColor == "":
                    # Change only foreground color
                    TagReplacement = f"{Format.Prefix.value}{Format.ForegroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == ForegroundColor][0]}{Format.StyleAndColorSuffix.value}"
                else:
                    # Change both colors
                    TagReplacement = f"{Format.Prefix.value}{Format.ForegroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == ForegroundColor][0]};{Format.BackgroundPrefix.value}{[MyColor.value['Format'] for MyColor in Color if MyColor.value['Tag'] == BackgroundColor][0]}{Format.StyleAndColorSuffix.value}"

            if FormatStyle in [MyStyle.value["Tag"] for MyStyle in Style]:
                # Style is valid
                TagReplacement += f"{Format.Prefix.value}{[MyStyle.value['Format'] for MyStyle in Style if MyStyle.value['Tag'] == FormatStyle][0]}{Format.StyleAndColorSuffix.value}"

            if TagReplacement != "":
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
    JustifyText = Justify.Left,
    MaxColumns = None,
    MaxLines = None,
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
            SB - Bold (this is very subtile to see)
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

    # split text according to square
    TextLines = []
    RemainingText = Text
    while len(RemainingText) > 0:
        if MaxColumns is not None:
            RemainingTextWithoutTags = _ManageColorTags(RemainingText, _TagAction.Remove)
            WrapPosition = (RemainingTextWithoutTags.rfind(" ", 0, MaxColumns + 1) 
                + (len(RemainingText) - len(RemainingTextWithoutTags)))
            if WrapPosition == -1:
                TextLines.append(RemainingText)
                RemainingText = ""
            else:
                TextLines.append(RemainingText[:WrapPosition])
                RemainingText = RemainingText[WrapPosition + 1:]
        else:
            TextLines.append(RemainingText) 
            RemainingText = ""

    # for each line
    for LineNumber, Text in enumerate(TextLines):
        # exit if text is too long
        if LineNumber > 0 and LineNumber >= MaxLines :
            # reset color and exit loop
            print(
                f"{Format.Prefix}{Format.Reset}", 
                end = "", 
                flush = True)
            break

        # replace tags by appropriate color codes
        Text = _ManageColorTags(Text)

        if LineNumber == 0:
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
        else:
            # move cursor 1 line below
            MoveCursorString = f"{Format.Prefix.value}1{Format.MoveDownSuffix.value}"
            # move cursor right is appropriate
            if Column is not None and str(int(Column)).isdigit():
                MoveCursorString += f"{Format.Prefix.value}{MaxColumns}{Format.MoveRightSuffix.value}"
            print(MoveCursorString, end = "")

        if MaxColumns is not None:
            # justify text
            if JustifyText == Justify.Left:
                Text = Text.ljust(MaxColumns)
            elif JustifyText == Justify.Right:
                Text = Text.rjust(MaxColumns)
            elif JustifyText == Justify.Center:
                Text = Text.center(MaxColumns)

        # print text
        if Speed == PrintSpeed.Instant:
            print(BeepString + Text, end = "", flush = True)
        else:
            for Letter in list(Text):
                print(BeepString + Letter, end = "", flush = True)
                time.sleep(Speed.value)
            print("", end = "", flush = True)

    # jump line after printing if needed
    if JumpLineAfter:
        print()



# code to test rich console functions
if __name__ == "__main__":

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
            ClearScreenBefore = True,
            MakeBeep = True)

    def SquareTest():
        Print(
            "┌─────────────────┐ │                 │ │                 │ │                 │ │                 │ │                 │ └─────────────────┘",
            3, 5,
            MaxColumns = 19,
            MaxLines = 7)
        Print(
            "[G;]Ce texte s'imprime [Y;]centré[G;] dans un rectangle de 15x5 (avec une marge de 1 caractère à gauche et à droite).[;]",
            4, 7,
            JustifyText = Justify.Center,
            MaxColumns = 15,
            MaxLines = 5,
            Speed = PrintSpeed.Fast)

    def AnimationTest():
        Print(
            f"\nUn {FullShape} va se déplacer sur l'écran",
            10, 0)
        PrintShape()
        ShowCursor(False)
        Print("[B;Y;SU] Entrée pour démarrer [;]", 12, 0)
        Print("---------------------------------------------------", 28, 0)
        input()
        while PosX <= 40:
            MoveShape(1, 0)
        while PosY <= 25:
            MoveShape(0, 1)
        while PosX >= 3:
            MoveShape(-1, 0)
        while PosY >= 15:
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
    input("\nTaper Entrée... ")
    TestIntro()
    # ClearConsole()
    SquareTest()
    AnimationTest()
    TestEnd()