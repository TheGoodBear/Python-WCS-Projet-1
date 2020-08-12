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
    LineOffset = Var.GameData["Views"][ViewName]["LineOffset"]
    for Index, Line in enumerate(Var.ViewsData[ViewName]):
        RC.Print(Line, LineOffset + Index, 1, 
            JustifyText = RC.Justify.Center, 
            MaxColumns = Var.GameData["Game"]["WindowWidth"])

    # show view content
    if ViewName == "Start":

        Title = (Var.MessagesData["Game"]["FullTitle"]
            .replace("{Title}", Var.MessagesData["Game"]["Title"])
            .replace("{VersionNumber}", Var.GameData["Game"]["VersionNumber"])
            .replace("{VersionDate}", Var.GameData["Game"]["VersionDate"]))
        RC.Print(f"{Title}",
            Var.GameData["Views"][ViewName]["TitleY"], Var.GameData["Views"][ViewName]["TitleX"],
            JustifyText = RC.Justify.Center,
            MaxColumns = Var.GameData["Views"][ViewName]["TitleMaxWidth"],
            Speed = RC.PrintSpeed.UltraFast)

        LineOffset = 0
        if Var.MessagesData["Game"]["Image"] is not None:
            LineOffset += RC.Print(Var.MessagesData["Game"]["Image"],
                Var.GameData["Views"][ViewName]["ImageY"], Var.GameData["Views"][ViewName]["ImageX"],
                JustifyText = RC.Justify.Center,
                MaxColumns = Var.GameData["Views"][ViewName]["ImageMaxWidth"],
                Speed = RC.PrintSpeed.UltraFast)

        RC.Print(Var.MessagesData["Game"]["History"],          
            Var.GameData["Views"][ViewName]["HistoryY"] + LineOffset, Var.GameData["Views"][ViewName]["HistoryX"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = Var.GameData["Views"][ViewName]["HistoryMaxWidth"])
        RC.Print(Var.MessagesData["Game"]["AskContinue"],          
            Var.GameData["Views"][ViewName]["AskContinueY"], Var.GameData["Views"][ViewName]["AskContinueX"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = Var.GameData["Views"][ViewName]["AskContinueMaxWidth"])
        RC.PlaceCursorAt(
            Var.GameData["Views"][ViewName]["AskContinueY"],
            Var.GameData["Views"][ViewName]["AskContinueX"] + len(Var.MessagesData["Game"]["AskContinue"]))
        input("")
        LineOffset = 0

        RC.ClearConsole(
            Var.GameData["Views"][ViewName]["MainViewPort"]["Y"],
            Var.GameData["Views"][ViewName]["MainViewPort"]["X"],
            Var.GameData["Views"][ViewName]["MainViewPort"]["Width"],
            Var.GameData["Views"][ViewName]["MainViewPort"]["Height"])

        LineOffset += 1 + RC.Print(Var.MessagesData["Game"]["Rules"],          
            Var.GameData["Views"][ViewName]["RulesY"] + LineOffset, Var.GameData["Views"][ViewName]["RulesX"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = Var.GameData["Views"][ViewName]["RulesMaxWidth"])
        
        RC.PlaceCursorAt(
            LineOffset + Var.GameData["Views"][ViewName]["AskNameY"],
            Var.GameData["Views"][ViewName]["AskNameX"])
        Var.CharactersData["Player"]["Name"] = Util.GetUserInput(Var.MessagesData["Game"]["AskName"])
        LineOffset += 1 + RC.Print(Var.MessagesData["Game"]["Hello"].replace("{Name}", Var.CharactersData["Player"]["Name"]),
            Var.GameData["Views"][ViewName]["HelloY"] + LineOffset, Var.GameData["Views"][ViewName]["HelloX"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = Var.GameData["Views"][ViewName]["HelloMaxWidth"])

        LineOffset += 1 + RC.Print(Var.MessagesData["Game"]["AskSex1"], 
            Var.GameData["Views"][ViewName]["AskSex1Y"] + LineOffset, Var.GameData["Views"][ViewName]["AskSex1X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = Var.GameData["Views"][ViewName]["AskSex1MaxWidth"])
        RC.PlaceCursorAt(
            LineOffset + Var.GameData["Views"][ViewName]["AskSex2Y"],
            Var.GameData["Views"][ViewName]["AskSex2X"])
        Var.CharactersData["Player"]["Sex"] = Util.GetUserInput(Var.MessagesData["Game"]["AskSex2"], PossibleValues = Var.GameData["Game"]["SexPossibleValues"].keys())
        LineOffset += RC.Print(Var.MessagesData["Game"]["Hello2"],          
            Var.GameData["Views"][ViewName]["Hello2Y"] + LineOffset, Var.GameData["Views"][ViewName]["Hello2X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = Var.GameData["Views"][ViewName]["Hello2MaxWidth"])

        RC.Print(Var.MessagesData["Game"]["AskReady"],          
            Var.GameData["Views"][ViewName]["AskReadyY"], Var.GameData["Views"][ViewName]["AskReadyX"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = Var.GameData["Views"][ViewName]["AskReadyMaxWidth"])
        input("")
   
    elif ViewName == "Main":
        pass

    elif ViewName == "Challenge":
        pass
