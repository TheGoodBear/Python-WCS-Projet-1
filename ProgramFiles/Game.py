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

    # initialize window
    # InitializeWindow()

    # game run
    Run()



def Run():
    """
        Game main loop
    """

    ShowView(Var.CurrentView)
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
    RC.Print(f"{Message}")
    input()



def ShowView(
    ViewName):
    """
        Show specific view
    """

    RC.ClearConsole()
    LineOffset = Var.GameData["Views"][ViewName]["LineOffset"]
    for Index, Line in enumerate(Var.ViewsData[ViewName]):
        RC.Print(Line, LineOffset + Index, 1, 
            JustifyText = RC.Justify.Center, 
            MaxColumns = Var.GameData["Game"]["WindowWidth"])

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

        if Var.MessagesData["Game"]["Image"] is not None:
            RC.Print(Var.MessagesData["Game"]["Image"],
                Var.GameData["Views"][ViewName]["ImageY"], Var.GameData["Views"][ViewName]["ImageX"],
                JustifyText = RC.Justify.Center,
                MaxColumns = Var.GameData["Views"][ViewName]["ImageMaxWidth"],
                Speed = RC.PrintSpeed.UltraFast)
        else:
            RC.Print("",
                Var.GameData["Views"][ViewName]["ImageY"], Var.GameData["Views"][ViewName]["ImageX"])

        RC.Print(Var.MessagesData["Game"]["History"],          
            Var.GameData["Views"][ViewName]["HistoryY"], Var.GameData["Views"][ViewName]["HistoryX"],
            MaxColumns = Var.GameData["Views"][ViewName]["HistoryMaxWidth"])


    elif ViewName == "Main":
        pass

    elif ViewName == "Challenge":
        pass
