# coding: utf-8

# Imports modules

# Import application code
import ProgramFiles.Variables as Var
import ProgramFiles.Utilities.Utilities as Util
import ProgramFiles.Utilities.RichConsole as RC


# Functions
def Initialization():
    """
        Initialize game data
    """

    # load general game data
    Var.GameData = Util.LoadJSONFile(Var.ResourcesFolder, "GameData")
    # load views data
    Var.ViewsData = Util.LoadViews(Var.ResourcesFolder, "Views")
    # load messages (text) data matching language
    Var.MessagesData = Util.LoadJSONFile(Var.ResourcesFolder, "Messages-" + Var.GameData["Game"]["Language"])
    # load characters data
    Var.CharactersData = Util.LoadJSONFile(Var.ResourcesFolder, "Characters")
    # load map data
    Var.MapLayer = Util.LoadMap(Var.ResourcesFolder, "Map")
    # load map elements data
    Var.MapElementsData = Util.LoadJSONFile(Var.ResourcesFolder, "MapElements")
    # load objects data
    Var.ObjectsData = Util.LoadJSONFile(Var.ResourcesFolder, "Objects")

    # initialize window
    # InitializeWindow()

    # game run
    Run()



def Run():
    """
        Game main loop
    """

    ShowView(Var.GameData["Game"]["CurrentView"])
    Var.GameData["Game"]["CurrentView"] = "Main"
    ShowView(Var.GameData["Game"]["CurrentView"])
    ShowMap()
    # while Var.GameRunning:
    #     pass



def InitializeWindow():
    """
        Show a splash screen with console configuration instructions
    """
    
    RC.ClearConsole()
    Message = (Var.MessagesData["Game"]["SplashScreen"]
        .replace("{Title}", Var.MessagesData["Game"]["Title"])
        .replace("{VersionNumber}", Var.GameData["Game"]["VersionNumber"])
        .replace("{VersionDate}", Var.GameData["Game"]["VersionDate"]))
    RC.Print(
        f"{Message}", 
        1, 1,
        MaxColumns = 100,
        JustifyText = RC.Justify.Left)
    input()



def ShowView(
    ViewName):
    """
        Show specific view
    """

    # show view template
    RC.ClearConsole()
    LineOffset = 0
    for Index, Line in enumerate(Var.ViewsData[ViewName]):
        RC.Print(Line, 
            Var.GameData["Views"][ViewName]["WindowViewPort"]["Y"] + Index, 1, 
            JustifyText = RC.Justify.Center, 
            MaxColumns = Var.GameData["Game"]["WindowWidth"])

    # show view content
    if ViewName == "Start":

        # title
        Message = (Var.MessagesData["Game"]["FullTitle"]
            .replace("{Title}", Var.MessagesData["Game"]["Title"])
            .replace("{VersionNumber}", Var.GameData["Game"]["VersionNumber"])
            .replace("{VersionDate}", Var.GameData["Game"]["VersionDate"]))
        RC.Print(f"{Message}",
            Var.GameData["Views"][ViewName]["TitleViewPort"]["Y"], Var.GameData["Views"][ViewName]["TitleViewPort"]["X"],
            JustifyText = RC.Justify.Center,
            MaxColumns = Var.GameData["Views"][ViewName]["TitleViewPort"]["Width"],
            Speed = RC.PrintSpeed.UltraFast)

        # viewports data
        TextY = Var.GameData["Views"][ViewName]["TextViewPort"]["Y"]
        TextX = Var.GameData["Views"][ViewName]["TextViewPort"]["X"]
        TextWidth = Var.GameData["Views"][ViewName]["TextViewPort"]["Width"]
        TextHeight = Var.GameData["Views"][ViewName]["TextViewPort"]["Height"]
        AskY = Var.GameData["Views"][ViewName]["AskViewPort"]["Y"]
        AskX = Var.GameData["Views"][ViewName]["AskViewPort"]["X"]
        AskWidth = Var.GameData["Views"][ViewName]["AskViewPort"]["Width"]
        AskHeight = Var.GameData["Views"][ViewName]["AskViewPort"]["Height"]

        # text page 1
        LineOffset = 0
        if Var.MessagesData["Game"]["Image"] is not None:
            LineOffset += RC.Print(Var.MessagesData["Game"]["Image"],
                TextY, TextX,
                JustifyText = RC.Justify.Center,
                MaxColumns = TextWidth,
                Speed = RC.PrintSpeed.UltraFast)

        RC.Print(Var.MessagesData["Game"]["History"],          
            TextY + LineOffset, TextX,
            JustifyText = RC.Justify.Left, 
            MaxColumns = TextWidth)
        RC.Print(Var.MessagesData["Game"]["AskContinue"],          
            AskY, AskX,
            JustifyText = RC.Justify.Left, 
            MaxColumns = AskWidth,
            Speed = RC.PrintSpeed.Fast)
        RC.PlaceCursorAt(AskY, AskX + len(Var.MessagesData["Game"]["AskContinue"]))
        input("")

        # clear text between pages
        RC.ClearConsole(TextY, TextX, TextWidth, TextHeight)
        RC.ClearConsole(AskY, AskX, AskWidth, AskHeight)

        # text page 2
        LineOffset = 0
        LineOffset += 1 + RC.Print(Var.MessagesData["Game"]["Rules"],          
            TextY + LineOffset, TextX,
            JustifyText = RC.Justify.Left, 
            MaxColumns = TextWidth)
        
        RC.PlaceCursorAt(TextY + LineOffset, TextX)
        Var.CharactersData["Player"]["Name"] = Util.GetUserInput(
            Var.MessagesData["Game"]["AskName"])
        Message = (Var.MessagesData["Game"]["Hello"]
            .replace("{Name}", Var.CharactersData["Player"]["Name"]))
        LineOffset += 1 + RC.Print(Message,
            TextY + LineOffset, TextX,
            JustifyText = RC.Justify.Left, 
            MaxColumns = TextWidth)

        LineOffset += 1 + RC.Print(Var.MessagesData["Game"]["AskSex1"], 
            TextY + LineOffset, TextX,
            JustifyText = RC.Justify.Left, 
            MaxColumns = TextWidth)
        RC.PlaceCursorAt(TextY + LineOffset, TextX)
        Var.CharactersData["Player"]["Sex"] = Util.GetUserInput(
            Var.MessagesData["Game"]["AskSex2"], 
            PossibleValues = list(Var.GameData["Game"]["SexPossibleValues"].keys())).upper()
        Message = (Var.MessagesData["Game"]["Hello2"]
            .replace("{ColoredName}", 
                Var.GameData["Game"]["SexPossibleValues"][Var.CharactersData["Player"]["Sex"]] + Var.CharactersData["Player"]["Name"] + "[;]")
            .replace("{Symbol}", 
                Var.GameData["Game"]["SexPossibleValues"][Var.CharactersData["Player"]["Sex"]] + Var.CharactersData["Player"]["Image"] + "[;]"))
        LineOffset += RC.Print(Message,          
            TextY + LineOffset, TextX,
            JustifyText = RC.Justify.Left, 
            MaxColumns = TextWidth)

        RC.Print(Var.MessagesData["Game"]["AskReady"],          
            AskY, AskX,
            JustifyText = RC.Justify.Left, 
            MaxColumns = AskWidth,
            Speed = RC.PrintSpeed.Fast)
        RC.PlaceCursorAt(AskY, AskX + len(Var.MessagesData["Game"]["AskReady"]))
        input("")
   
    elif ViewName == "Main":
        pass

    elif ViewName == "Challenge":
        pass
