# coding: utf-8

# Imports modules
import time
import random

# Import application code
import ProgramFiles.Variables as Var
import ProgramFiles.Utilities.Utilities as Util
import ProgramFiles.Utilities.RichConsole as RC
import ProgramFiles.Challenge1 as Chal1
import ProgramFiles.Challenge2 as Chal2
import ProgramFiles.Challenge3 as Chal3


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
    # get player
    Var.Player = [Character for Character in Var.CharactersData if Character["Category"] == "Player"][0]
    # load map data and prepare layers
    Var.MapsData = Util.LoadMaps(Var.ResourcesFolder, "Maps")
    GetMapLayersAndViewPort()
    # load map elements data
    Var.MapElementsData = Util.LoadJSONFile(Var.ResourcesFolder, "MapElements")
    # load objects data
    Var.ObjectsData = Util.LoadJSONFile(Var.ResourcesFolder, "Objects")
    # place objects with a start position in the corresponding map layer
    StartObjects = {ObjectKey : ObjectValue for (ObjectKey, ObjectValue) in Var.ObjectsData.items() if ObjectValue["StartPosition"] is not None}
    for ObjectKey, ObjectValue in StartObjects.items():
        Var.MapsData[ObjectValue["StartPosition"]["Map"]]["Objects"][ObjectValue["StartPosition"]["Y"]][ObjectValue["StartPosition"]["X"]] = ObjectKey

    # initialize window
    # InitializeWindow()

    # game run
    Run()



def Run():
    """
        Game main loop
    """

    # show start view
    # ShowView(Var.GameData["Game"]["CurrentView"], ClearScreen = True)

    # show main view
    Var.GameData["Game"]["CurrentView"] = "Main"
    ShowView(ClearScreen = True)

    # main loop
    while Var.GameRunning:
        (ActionName, ActionArgument) = AskPlayerAction()
        ExecutePlayerAction(ActionName, ActionArgument)
    
    # exit program
    RC.ClearConsole()
    print("AU REVOIR !")
    input()
    return



def InitializeWindow():
    """
        Show a splash screen with console configuration instructions
    """
    
    RC.ClearConsole()
    Message = (Var.MessagesData["Game"]["SplashScreen"]
        .replace("{Title}", Var.MessagesData["Game"]["Title"])
        .replace("{VersionNumber}", Var.GameData["Game"]["VersionNumber"])
        .replace("{VersionDate}", Var.GameData["Game"]["VersionDate"])
        .replace("{WindowWidth}", str(Var.GameData["Game"]["WindowWidth"] + 1))
        .replace("{WindowHeight}", str(Var.GameData["Game"]["WindowHeight"])))
    RC.Print(
        f"{Message}", 
        1, 1,
        MaxColumns = 100,
        JustifyText = RC.Justify.Left)
    input()



def ShowView(
    ViewName = None,
    ViewParts = None,
    ClearScreen = False):
    """
        Show specified view with associated data
        Only update specific viewparts (list) if specified
        Optionally clears screen before
    """

    # show view template
    if ClearScreen:
        RC.ClearConsole()

    # get challenge number and view name
    ChallengeNumber = (
        int(Var.Player["CurrentMap"][-1:]) 
        if Var.Player["CurrentMap"][-1:].isdigit() 
        else 0)
    if ViewName is None:
        ViewName = (
            Var.Player["CurrentMap"] 
            if not Var.Player["CurrentMap"][-1:].isdigit() 
            else Var.Player["CurrentMap"][:-1])
        Var.GameData["Game"]["CurrentView"] = ViewName

    LineOffset = 0
    if ClearScreen:
        # draw view template
        for Index, Line in enumerate(Var.ViewsData[ViewName]):
            RC.Print(Line, 
                Var.GameData["ViewPorts"][ViewName]["Window"]["Y"] + Index, 
                Var.GameData["ViewPorts"][ViewName]["Window"]["X"], 
                JustifyText = RC.Justify.Center, 
                MaxColumns = Var.GameData["ViewPorts"][ViewName]["Window"]["Width"])

    # show view content
    if ViewName == "StartEnd":

        RC.ShowCursor(False)

        # viewports data
        TitleVP = Var.GameData["ViewPorts"][ViewName]["Title"]
        TextVP = Var.GameData["ViewPorts"][ViewName]["Text"]
        AskVP = Var.GameData["ViewPorts"][ViewName]["Ask"]

        # title
        Message = (Var.MessagesData["Game"]["FullTitle"]
            .replace("{Title}", Var.MessagesData["Game"]["Title"])
            .replace("{VersionNumber}", Var.GameData["Game"]["VersionNumber"])
            .replace("{VersionDate}", Var.GameData["Game"]["VersionDate"]))
        RC.Print(f"{Message}",
            TitleVP["Y"], TitleVP["X"],
            JustifyText = RC.Justify.Center,
            MaxColumns = TitleVP["Width"],
            Speed = RC.PrintSpeed.UltraFast)

        # show start data
        if ViewParts is None or "Start" in ViewParts:

            # text page 1
            LineOffset = 0
            if Var.MessagesData["Game"]["Image"] is not None:
                LineOffset += RC.Print(Var.MessagesData["Game"]["Image"],
                    TextVP["Y"], TextVP["X"],
                    JustifyText = RC.Justify.Center,
                    MaxColumns = TextVP["Width"],
                    Speed = RC.PrintSpeed.UltraFast)[0]

            RC.Print(Var.MessagesData["Game"]["Story"],          
                TextVP["Y"] + LineOffset, TextVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = TextVP["Width"])

            # ask continue
            AskContinue(AskVP)

            # clear text between pages
            RC.ClearConsole(
                TextVP["Y"], TextVP["X"], 
                TextVP["Width"], TextVP["Height"])
            RC.ClearConsole(
                AskVP["Y"], AskVP["X"], 
                AskVP["Width"], AskVP["Height"])

            # text page 2
            LineOffset = 0
            Message = (Var.MessagesData["Game"]["Rules"]
                .replace("{HealthColor}", Var.GameData["Game"]["VitalSigns"]["Health"]["Color"])
                .replace("{HydrationColor}", Var.GameData["Game"]["VitalSigns"]["Hydration"]["Color"])
                .replace("{SatietyColor}", Var.GameData["Game"]["VitalSigns"]["Satiety"]["Color"]))
            LineOffset += 1 + RC.Print(Message,          
                TextVP["Y"] + LineOffset, TextVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = TextVP["Width"])[0]
            
            RC.ShowCursor()
            Var.Player["Name"] = Util.GetUserInput(
                Var.MessagesData["Game"]["AskName"],
                Minimum = 3,
                Maximum = 20,
                SpecificErrorMessage = Var.MessagesData["Game"]["WrongName"],
                RichConsoleParameters = [TextVP["Y"] + LineOffset, TextVP["X"], TextVP["Width"]])
            RC.ShowCursor(False)
            RC.ClearConsole(
                TextVP["Y"] + LineOffset, TextVP["X"], 
                TextVP["Width"], 2)

            Message = (Var.MessagesData["Game"]["Hello"]
                .replace("{Name}", Var.Player["Name"]))
            LineOffset += 1 + RC.Print(Message,
                TextVP["Y"] + LineOffset, TextVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = TextVP["Width"])[0]

            # check if a game already exists for this name


            LineOffset += 1 + RC.Print(Var.MessagesData["Game"]["AskSex1"], 
                TextVP["Y"] + LineOffset, TextVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = TextVP["Width"])[0]

            Sex = Util.GetUserInput(
                Var.MessagesData["Game"]["AskSex2"],
                PossibleValues = list(Var.MessagesData["Game"]["Sex"].keys()),
                SpecificErrorMessage = Var.MessagesData["Game"]["WrongAnswer"],
                RichConsoleParameters = [TextVP["Y"] + LineOffset, TextVP["X"], TextVP["Width"]]).upper()
            Var.Player["Sex"] = Var.MessagesData["Game"]["Sex"][Sex]
            Var.Player["Style"] = Var.GameData["Game"]["Sex"][Var.Player["Sex"]]["Color"]
            RC.ShowCursor(False)
            RC.ClearConsole(
                TextVP["Y"] + LineOffset, TextVP["X"], 
                TextVP["Width"], 2)
            
            Message = (Var.MessagesData["Game"]["Hello2"]
                .replace("{ColoredName}", 
                    Var.Player["Style"] + Var.Player["Name"] + "[;]")
                .replace("{Symbol}", 
                    Var.Player["Style"] + " ".join(set(Var.Player["Images"].values())) + "[;]"))
            LineOffset += RC.Print(Message,          
                TextVP["Y"] + LineOffset, TextVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = TextVP["Width"])[0]

            RC.Print(Var.MessagesData["Game"]["AskReady"],          
                AskVP["Y"], AskVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = AskVP["Width"],
                Speed = RC.PrintSpeed.Fast)
            RC.PlaceCursorAt(
                AskVP["Y"], 
                AskVP["X"] + len(Var.MessagesData["Game"]["AskReady"]))
            input("")

        # show end data
        if ViewParts is not None and "End" in ViewParts:

            LineOffset = 0

            if "Win" in ViewParts:
                if Var.MessagesData["Game"]["WinImage"] is not None:
                    LineOffset += RC.Print(Var.MessagesData["Game"]["WinImage"],
                        TextVP["Y"], TextVP["X"],
                        JustifyText = RC.Justify.Center,
                        MaxColumns = TextVP["Width"],
                        Speed = RC.PrintSpeed.UltraFast)[0]

                Message = (Var.MessagesData["Game"]["WinGame"]
                    .replace("{Name}", 
                        Var.Player["Style"] + Var.Player["Name"] + "[;]")
                    .replace("{Title}", 
                        Var.MessagesData["Game"]["Title"])
                    .replace("{TotalMovements}", 
                        str(Var.Player["TotalMovements"]))
                    .replace("{TotalActions}", 
                        str(Var.Player["TotalActions"])))
                RC.Print(Message,          
                    TextVP["Y"] + LineOffset, TextVP["X"],
                    JustifyText = RC.Justify.Left, 
                    MaxColumns = TextVP["Width"])

            elif "Loose" in ViewParts:
                if Var.MessagesData["Game"]["LooseImage"] is not None:
                    LineOffset += RC.Print(Var.MessagesData["Game"]["LooseImage"],
                        TextVP["Y"], TextVP["X"],
                        JustifyText = RC.Justify.Center,
                        MaxColumns = TextVP["Width"],
                        Speed = RC.PrintSpeed.UltraFast)[0]

                Message = (Var.MessagesData["Game"]["LooseGame"]
                    .replace("{Name}", 
                        Var.Player["Style"] + Var.Player["Name"] + "[;]")
                    .replace("{Title}", 
                        Var.MessagesData["Game"]["Title"]))
                RC.Print(Message,          
                    TextVP["Y"] + LineOffset, TextVP["X"],
                    JustifyText = RC.Justify.Left, 
                    MaxColumns = TextVP["Width"])

            # ask quit
            AskContinue(AskVP, Quit = True)


    elif ViewName == "Main":

        Var.CurrentChallengeData = None
        RC.ShowCursor(False)

        # show map if specified
        if ViewParts is None or "Map" in ViewParts:
            ShowMap(ViewName = ViewName)

        # show dashboard
        ShowDashboard(ViewParts)

    elif ViewName == "Challenge":

        Var.CurrentChallengeData = Var.GameData[Var.Player["CurrentMap"]]
        RC.ShowCursor(False)

        # viewports data
        ChallengeVP = Var.GameData["ViewPorts"][ViewName]["Window"]
        MapVP = Var.GameData["ViewPorts"][ViewName]["Map"]
        TitleVP = Var.GameData["ViewPorts"][ViewName]["Title"]
        TextVP = Var.GameData["ViewPorts"][ViewName]["Text"]
        AskVP = Var.GameData["ViewPorts"][ViewName]["Ask"]

        # show map if specified
        if ViewParts is None or "Map" in ViewParts:
            ShowMap(ViewName = ViewName)

        # show dashboard
        ShowDashboard(ViewParts)

        CurrentMap = Var.Player["CurrentMap"]

        if ViewParts is None or "ChallengeTitle" in ViewParts:
            # challenge title
            RC.Print(f"{Var.MessagesData[CurrentMap]['Title']}",
                TitleVP["Y"], TitleVP["X"],
                JustifyText = RC.Justify.Center,
                MaxColumns = TitleVP["Width"],
                Speed = RC.PrintSpeed.Instant)

        if ((ViewParts is None or "ChallengeText1" in ViewParts)
            and not Var.CurrentChallengeData["Won"]):
            # challenge text
            RC.ClearConsole(
                TextVP["Y"], TextVP["X"], 
                TextVP["Width"], TextVP["Height"])
            LineOffset = 0

            Message = (Var.MessagesData[CurrentMap]["Story1"]
                .replace("{Name}", 
                    Var.Player["Style"] + Var.Player["Name"] + "[;]"))
            LineOffset += RC.Print(Message,          
                TextVP["Y"] + LineOffset, TextVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = TextVP["Width"])[0]

            if ChallengeNumber == 2:
                # activate random letter
                Chal2.SwitchLetter(chr(97 + random.randint(0, 25)))
                # update stoty with encrypted credo
                Var.MessagesData[CurrentMap]["Story2"] = (
                    "\n\n[;;SI]"
                    + Var.CurrentChallengeData["EncryptedCredo"]
                    + "[;]")

            if Var.MessagesData[CurrentMap]["Story2"] is not None:
                # ask continue (if story continues)
                AskContinue(AskVP)

        if ((ViewParts is None or "ChallengeText2" in ViewParts)
            and Var.MessagesData[CurrentMap]["Story2"] is not None
            and not Var.CurrentChallengeData["Won"]):

            if ChallengeNumber == 1:
                # light eyes
                Chal1.SphinxEyes()

            # challenge text
            RC.ClearConsole(
                TextVP["Y"], TextVP["X"], 
                TextVP["Width"], TextVP["Height"])
            LineOffset = 0

            Message = (Var.MessagesData[CurrentMap]["Story2"]
                .replace("{Name}", 
                    Var.Player["Style"] + Var.Player["Name"] + "[;]"))
            
            TextJustify = RC.Justify.Left
            if ChallengeNumber == 1:
                Message = (Message
                    .replace("{Rounds}", 
                        str(Var.CurrentChallengeData["Rounds"]))
                    .replace("{MinimumNumber}", 
                        str(Var.CurrentChallengeData["MinimumNumber"]))
                    .replace("{MaximumNumber}", 
                        str(Var.CurrentChallengeData["MaximumNumber"]))
                    .replace("{MaxTries}", 
                        str(Var.CurrentChallengeData["MaxTries"])))
            elif ChallengeNumber == 2:
                TextJustify = RC.Justify.Center
            elif ChallengeNumber == 3:
                Message = (Message
                    .replace("{PlayerChance}", 
                        str(Var.CurrentChallengeData["PlayerChance"])))

            LineOffset += RC.Print(Message,          
                TextVP["Y"] + LineOffset, TextVP["X"],
                JustifyText = TextJustify, 
                MaxColumns = TextVP["Width"])[0]

        if ViewParts is not None and "EncryptedCredo" in ViewParts:
            # challenge 2 encrypted credo

            Message = (
                "\n\n[;;SI]"
                + Var.CurrentChallengeData["EncryptedCredo"]
                + "[;]\n\n"
                + Var.MessagesData["Challenge2"]["Switch"])

            LineOffset += RC.Print(Message,          
                TextVP["Y"] + LineOffset, TextVP["X"],
                JustifyText = RC.Justify.Center, 
                MaxColumns = TextVP["Width"])[0]


def AskContinue(
    ViewPortData,
    Quit = False,
    ClearViewPort = False):
    """
        Ask player to continue story
        and/or clear viewport
    """

    if not ClearViewPort:
        Message = (
            Var.MessagesData["Game"]["AskContinue"]
            if not Quit
            else Var.MessagesData["Game"]["AskQuit"])

        # ask continue
        RC.Print(Message,          
            ViewPortData["Y"], ViewPortData["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = ViewPortData["Width"],
            Speed = RC.PrintSpeed.Instant)
        RC.PlaceCursorAt(
            ViewPortData["Y"], 
            ViewPortData["X"] + len(Message))
        # wait for user entry
        input("")
        # clear viewport
        RC.ClearConsole(
            ViewPortData["Y"], ViewPortData["X"], 
            ViewPortData["Width"], ViewPortData["Height"])
    else:
        # clear viewport
        RC.ClearConsole(
            ViewPortData["Y"], ViewPortData["X"], 
            ViewPortData["Width"], ViewPortData["Height"])



def GetMapLayersAndViewPort():
    """
        Get current map layers and viewport
    """

    # layers
    Var.MapLayer = Var.MapsData[Var.Player["CurrentMap"]]["Map"]
    Var.ObjectsLayer = Var.MapsData[Var.Player["CurrentMap"]]["Objects"]
    
    # viewport (from player current map, remove last character if a digit for viewport name)
    CurrentMap = Var.Player["CurrentMap"]
    Var.MapViewPortName = (CurrentMap 
        if not CurrentMap[-1:].isdigit() 
        else CurrentMap[:-1])
    MapViewPort = Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]
    # update map viewport so it matches map size
    DeltaWidth = MapViewPort["Width"] - len(Var.MapLayer[0])
    DeltaHeight = MapViewPort["Height"] - len(Var.MapLayer)
    MapViewPort["X"] += DeltaWidth // 2 
    MapViewPort["Y"] += DeltaHeight // 2 
    MapViewPort["Width"] -= DeltaWidth
    MapViewPort["Height"] -= DeltaHeight



def ShowMap(
    Y = None, 
    X = None,
    ViewName = None):
    """
        Show current map on view with all layers (map → objects → characters)

        Full map if no coordinates specified,
        or only refresh map on specified coordinates
    """

    if X == None or Y == None:
        # clear main viewport
        MainMapViewPort = Var.GameData["ViewPorts"][ViewName]["Map"] 
        RC.ClearConsole(
            MainMapViewPort["Y"], MainMapViewPort["X"], 
            MainMapViewPort["Width"], MainMapViewPort["Height"])
        # draw full map
        for Line in range(len(Var.MapLayer)):
            for Column in range(len(Var.MapLayer[Line])):
                _PrintMapLayersAtPosition(Line, Column)

    else:
        # refresh specified position
        _PrintMapLayersAtPosition(Y, X)



def _PrintMapLayersAtPosition(
    Y, X):
    """
        Print map and object layer as specified position
    """

    # map layer
    # get map element data for current element
    MapElement = Var.MapElementsData[Var.MapLayer[Y][X]]
    # draw
    RC.Print(
        f"{MapElement['Style']}{MapElement['Image']}[;]",
        Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["Y"] + Y,
        Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["X"] + X,
        JumpLineAfter = False)

    # object layer
    if Var.ObjectsLayer[Y][X] != "":
        # get object element data for current object
        MapObject = Var.ObjectsData[Var.ObjectsLayer[Y][X]]
        # draw
        RC.Print(
            f"{MapObject['Style']}{MapObject['Image']}[;]",
            Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["Y"] + Y,
            Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["X"] + X,
            JumpLineAfter = False)

    # character layer
    # check if a character is at this position
    CharacterHere = [
        CharacterHere for CharacterHere in Var.CharactersData 
            if CharacterHere["CurrentMap"] == Var.Player["CurrentMap"] 
            and CharacterHere["Position"]["X"] == X and CharacterHere["Position"]["Y"] == Y]
    if len(CharacterHere) == 1:
        CharacterHere = CharacterHere[0]
        # draw
        RC.Print(
            f"{CharacterHere['Style']}{CharacterHere['Images'][CharacterHere['Position']['Direction']]}[;]",
            Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["Y"] + Y,
            Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["X"] + X,
            JumpLineAfter = False)



def ShowDashboard(ViewParts = None):
    """
        Show dashboard
        Only update specific viewparts if specified
    """

    # dashboard viewports data
    DashboardVP = Var.GameData["ViewPorts"]["Dashboard"]["Window"]
    GameTitleVP = Var.GameData["ViewPorts"]["Dashboard"]["Title"]
    PlayerVP = Var.GameData["ViewPorts"]["Dashboard"]["Player"]
    VitalSignsVP = Var.GameData["ViewPorts"]["Dashboard"]["VitalSigns"]
    CountersVP = Var.GameData["ViewPorts"]["Dashboard"]["Counters"]
    BackpackTitleVP = Var.GameData["ViewPorts"]["Dashboard"]["BackpackTitle"]
    BackpackItemsVP = Var.GameData["ViewPorts"]["Dashboard"]["BackpackItems"]
    EnvironmentVP = Var.GameData["ViewPorts"]["Dashboard"]["Environment"]
    AskActionVP = Var.GameData["ViewPorts"]["Dashboard"]["AskAction"]
    ActionHistoryTitleVP = Var.GameData["ViewPorts"]["Dashboard"]["ActionHistoryTitle"]
    ActionHistoryVP = Var.GameData["ViewPorts"]["Dashboard"]["ActionHistory"]
    MessageVP = Var.GameData["ViewPorts"]["Dashboard"]["Message"]
    
    # dashboard
    # title view part
    if ViewParts is None or "Title" in ViewParts:
        LineOffset = 0
        LineOffset += RC.Print(f"[B;W]{Var.MessagesData['Game']['Title']}",
            GameTitleVP["Y"], GameTitleVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = GameTitleVP["Width"])[0]
        Message = (Var.MessagesData["Dashboard"]["FullVersion"]
            .replace("{VersionNumber}", Var.GameData["Game"]["VersionNumber"])
            .replace("{VersionDate}", Var.GameData["Game"]["VersionDate"]))
        RC.Print(f"{Message}",
            GameTitleVP["Y"] + LineOffset, GameTitleVP["X"],
            JustifyText = RC.Justify.Center,
            MaxColumns = GameTitleVP["Width"])
    
    # player view part
    if ViewParts is None or "Player" in ViewParts:
        LineOffset = 0
        Message = (Var.GameData["Game"]["Sex"][Var.Player["Sex"]]["Color"] + 
            Var.MessagesData["Dashboard"]["PlayerFullName"]
                .replace("{ColoredName}", Var.Player["Name"])
                .replace("{SexSymbol}", Var.GameData["Game"]["Sex"][Var.Player["Sex"]]["Symbol"]))
        RC.Print(Message,          
            PlayerVP["Y"] + LineOffset, PlayerVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = PlayerVP["Width"])
    
    # vital signs view part
    if ViewParts is None or "VitalSigns" in ViewParts:
        LineOffset = 0
        HealthLength = (Var.GameData["Game"]["VitalSigns"]["BarLength"] * 
            (Var.Player["Health"] * 100 // Var.Player["MaxHealth"])
            // 100)
        Message = (Var.MessagesData["Dashboard"]["PlayerHealth"]
            .replace(
                "{HealthCounter}", 
                f"{Var.GameData['Game']['VitalSigns']['Health']['Color']}{''.ljust(HealthLength, Var.GameData['Game']['VitalSigns']['Health']['Symbol'])}[;]"))
        LineOffset += RC.Print(Message,          
            VitalSignsVP["Y"] + LineOffset, VitalSignsVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = VitalSignsVP["Width"])[0]
        HydrationLength = (Var.GameData["Game"]["VitalSigns"]["BarLength"] * 
            (Var.Player["Hydration"] * 100 // Var.Player["MaxHydration"])
            // 100)
        Message = (Var.MessagesData["Dashboard"]["PlayerHydration"]
            .replace(
                "{HydrationCounter}", 
                f"{Var.GameData['Game']['VitalSigns']['Hydration']['Color']}{''.ljust(HydrationLength, Var.GameData['Game']['VitalSigns']['Hydration']['Symbol'])}[;]"))
        LineOffset += RC.Print(Message,          
            VitalSignsVP["Y"] + LineOffset, VitalSignsVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = VitalSignsVP["Width"])[0]
        SatietyLength = (Var.GameData["Game"]["VitalSigns"]["BarLength"] * 
            (Var.Player["Satiety"] * 100 // Var.Player["MaxSatiety"])
            // 100)
        Message = (Var.MessagesData["Dashboard"]["PlayerSatiety"]
            .replace(
                "{SatietyCounter}", 
                f"{Var.GameData['Game']['VitalSigns']['Satiety']['Color']}{''.ljust(SatietyLength, Var.GameData['Game']['VitalSigns']['Satiety']['Symbol'])}[;]"))
        LineOffset += RC.Print(Message,          
            VitalSignsVP["Y"] + LineOffset, VitalSignsVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = VitalSignsVP["Width"])[0]
    
    # counters view part
    if ViewParts is None or "Counters" in ViewParts:
        LineOffset = 0
        Message = (Var.MessagesData["Dashboard"]["CounterMovements"]
            .replace(
                "{TotalMovements}", 
                f"{Var.Player['TotalMovements']}"))
        RC.Print(Message,          
            CountersVP["Y"], CountersVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = CountersVP["Width"] // 2)
        Message = (Var.MessagesData["Dashboard"]["CounterActions"]
            .replace(
                "{TotalActions}", 
                f"{Var.Player['TotalActions']}"))
        RC.Print(Message,          
            CountersVP["Y"], CountersVP["X"] + CountersVP["Width"] // 2,
            JustifyText = RC.Justify.Left, 
            MaxColumns = CountersVP["Width"] // 2)
    
    # backpack title view part
    if ViewParts is None or "BackpackTitle" in ViewParts:
        LineOffset = 0
        Message = (Var.MessagesData["Dashboard"]["BackpackTitle"]
            .replace(
                "{ItemsInBackpack}", 
                f"{len(Var.ObjectsData['Backpack']['Behaviors']['Contains'])}")
            .replace(
                "{BackpackCapacity}", 
                f"{Var.ObjectsData['Backpack']['Behaviors']['Capacity']}"))
        RC.Print(Message,          
            BackpackTitleVP["Y"] + LineOffset, BackpackTitleVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = BackpackTitleVP["Width"])
    
    # backpack items view part
    if ViewParts is None or "BackpackItems" in ViewParts:
        RC.ClearConsole(
            BackpackItemsVP["Y"], BackpackItemsVP["X"], 
            BackpackItemsVP["Width"], BackpackItemsVP["Height"])
        LineOffset = 0
        for Index, Item in enumerate(Var.ObjectsData["Backpack"]["Behaviors"]["Contains"]):
            Message = f"{Var.ObjectsData[Item]['Style']}{str(Index + 1).rjust(2)}) {Var.MessagesData[Item]['Name']}"
            # add empty of contents remaining if appropriate
            if Var.ObjectsData[Item]["Behaviors"]["Contains"] is not None:
                Message += (
                    f" ({Var.ObjectsData[Item]['Behaviors']['Contains']}/{Var.ObjectsData[Item]['Behaviors']['Capacity']})"
                    if Var.ObjectsData[Item]["Behaviors"]["Contains"] > 0
                    else f" ({Var.MessagesData['Dashboard']['Empty']})")
            RC.Print(Message,          
                BackpackItemsVP["Y"] + LineOffset + Index, BackpackItemsVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = BackpackItemsVP["Width"])
    
    # environment view part
    if ViewParts is None or "Environment" in ViewParts:
        RC.ClearConsole(
            EnvironmentVP["Y"], EnvironmentVP["X"], 
            EnvironmentVP["Width"], EnvironmentVP["Height"])
        LineOffset = 0
        Message = (Var.MessagesData["Dashboard"]["PlayerOrientation"]
            .replace(
                "{DirectionName}", 
                f"{Var.MessagesData['Dashboard']['Directions'][Var.Player['Position']['Direction']]}")
            .replace(
                "{DirectionSymbol}", 
                f"{Var.GameData['Game']['Directions'][Var.Player['Position']['Direction']]['Symbol']}"))
        LineOffset += RC.Print(Message,          
            EnvironmentVP["Y"] + LineOffset, EnvironmentVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = EnvironmentVP["Width"])[0]
        # on element
        OnElement = (Var.MapLayer
            [Var.Player["Position"]["Y"]]
            [Var.Player["Position"]["X"]])
        SymbolString = ("" if Var.MapElementsData[OnElement]["Image"].strip() == ""
            else f" ({Var.MapElementsData[OnElement]['Style']}{Var.MapElementsData[OnElement]['Image']}[;])")
        Message = (Var.MessagesData["Dashboard"]["PlayerMovesOn"]
            .replace(
                "{Element}", 
                f"{Var.MapElementsData[OnElement]['Style']}{str(Var.MessagesData[OnElement]['Name']).lower()}[;]{SymbolString}"))
        LineOffset += RC.Print(Message,          
            EnvironmentVP["Y"] + LineOffset, EnvironmentVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = EnvironmentVP["Width"])[0]
        # seen element
        Var.SeenCoordinates["Y"] = (
            Var.Player["Position"]["Y"] 
            + Var.GameData["Game"]["Directions"][Var.Player["Position"]["Direction"]]["DeltaY"])
        Var.SeenCoordinates["X"] = (
            Var.Player["Position"]["X"] 
            + Var.GameData["Game"]["Directions"][Var.Player["Position"]["Direction"]]["DeltaX"])
        Var.SeenElement = None
        try:
            Var.SeenElement = (
                Var.MapLayer[Var.SeenCoordinates["Y"]][Var.SeenCoordinates["X"]])
            SymbolString = ("" if Var.MapElementsData[Var.SeenElement]["Image"].strip() == ""
                else f" ({Var.MapElementsData[Var.SeenElement]['Style']}{Var.MapElementsData[Var.SeenElement]['Image']}[;])")
            Message = (Var.MessagesData["Dashboard"]["PlayerSees"]
                .replace(
                    "{Element}", 
                    f"{Var.MapElementsData[Var.SeenElement]['Style']}{str(Var.MessagesData[Var.SeenElement]['Name']).lower()}[;]{SymbolString}"))
        except IndexError:
            Message = (Var.MessagesData["Dashboard"]["PlayerSees"]
                .replace(
                    "{Element}", 
                    f"{Var.MapElementsData[OnElement]['Style']}{str(Var.MessagesData[OnElement]['Name']).lower()}[;]{SymbolString}"))
        LineOffset += RC.Print(Message,          
            EnvironmentVP["Y"] + LineOffset, EnvironmentVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = EnvironmentVP["Width"])[0]
        # seen object
        Var.SeenObject = None
        try:
            Var.SeenObject = (
                Var.ObjectsLayer[Var.SeenCoordinates["Y"]][Var.SeenCoordinates["X"]])
            if Var.SeenObject.strip() != "":
                # there is an object in front of player
                SymbolString = ("" if Var.ObjectsData[Var.SeenObject]["Image"].strip() == ""
                    else f" ({Var.ObjectsData[Var.SeenObject]['Style']}{Var.ObjectsData[Var.SeenObject]['Image']}[;])")
                Message = (Var.MessagesData["Dashboard"]["PlayerSeesObject"]
                    .replace(
                        "{Object}", 
                        f"{Var.ObjectsData[Var.SeenObject]['Style']}{str(Var.MessagesData[Var.SeenObject]['Name']).lower()}[;]{SymbolString}"))
                LineOffset += RC.Print(Message,          
                    EnvironmentVP["Y"] + LineOffset, EnvironmentVP["X"],
                    JustifyText = RC.Justify.Center, 
                    MaxColumns = EnvironmentVP["Width"])[0]
        except IndexError:
            pass

    # action history title view part
    if ViewParts is None or "ActionHistoryTitle" in ViewParts:
        LineOffset = 0
        RC.Print(Var.MessagesData["Dashboard"]["ActionHistoryTitle"],          
            ActionHistoryTitleVP["Y"] + LineOffset, ActionHistoryTitleVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = ActionHistoryTitleVP["Width"])

    # action history view part
    if ViewParts is None or "ActionHistory" in ViewParts:
        RC.ClearConsole(
            ActionHistoryVP["Y"], ActionHistoryVP["X"], 
            ActionHistoryVP["Width"], ActionHistoryVP["Height"])
        LineOffset = 0
        # get last ActionHistoryVP["Height"] (reversed)
        for Index, Action in enumerate(Var.ActionsHistory[:-(ActionHistoryVP["Height"] + 1):-1]):
            RC.Print(f"{Action}",          
                ActionHistoryVP["Y"] + LineOffset + Index, ActionHistoryVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = ActionHistoryVP["Width"])
    
    # message/story view part
    if ViewParts is None or "Message" in ViewParts:
        RC.ClearConsole(
            MessageVP["Y"], MessageVP["X"], 
            MessageVP["Width"], MessageVP["Height"])
        LineOffset = 0
        RC.Print(Var.CurrentMessage,          
            MessageVP["Y"] + LineOffset, MessageVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = MessageVP["Width"])



def AskPlayerAction():
    """
        Ask player action
    """

    # get possible actions
    PossibleActions = [Actions["Command"] for Actions in Var.MessagesData["Dashboard"]["Actions"].values()]

    # get player input
    AskActionVP = Var.GameData["ViewPorts"]["Dashboard"]["AskAction"]
    
    while True:
        IsCommandOK = True

        RC.ShowCursor()
        NewCommand = Util.GetUserInput(
            Var.MessagesData["Dashboard"]["AskAction"],
            DefaultValue = "",
            RichConsoleParameters = [AskActionVP["Y"], AskActionVP["X"], AskActionVP["Width"]]).strip().upper()

        # get default command if empty
        Command = NewCommand if (NewCommand != "" or Var.LastPlayerCommand is None) else Var.LastPlayerCommand

        # extract action and number argument
        Action = Command[:1]
        ActionArgument = Command[1:]

        if Action not in PossibleActions:

            # action is not valid, show error message and wait          
            IsCommandOK = False
            RC.ShowCursor(False)
            RC.Print(Var.MessagesData["Dashboard"]["AskActionUnknown"],
                AskActionVP["Y"], AskActionVP["X"], 
                MaxColumns = AskActionVP["Width"],
                JustifyText = RC.Justify.Left)
            time.sleep(Var.GameData["Game"]["WaitOnActionError"])

        else:

            # get action name
            ActionName = [ActionName for ActionName, ActionValues in Var.MessagesData["Dashboard"]["Actions"].items() if ActionValues["Command"] == Action][0]
            # check if action argument is valid
            if (Var.GameData["Game"]["Actions"][ActionName]["NumberParameter"] == "Mandatory"
                and ActionArgument == ""):
                # action parameter is not valid, show error message and wait          
                IsCommandOK = False
                RC.ShowCursor(False)
                RC.Print(Var.MessagesData["Dashboard"]["AskActionNoItem"],
                    AskActionVP["Y"], AskActionVP["X"], 
                    MaxColumns = AskActionVP["Width"],
                    JustifyText = RC.Justify.Left)
                time.sleep(Var.GameData["Game"]["WaitOnActionError"])
            elif (Var.GameData["Game"]["Actions"][ActionName]["NumberParameter"] == "Optional"
                and ActionArgument == ""):
                # optional argument missing, set 1 for default
                ActionArgument = 1
            elif (Var.GameData["Game"]["Actions"][ActionName]["NumberParameter"] is not None
                and not ActionArgument.isdigit()):
                # action argument is not valid, show error message and wait          
                IsCommandOK = False
                RC.ShowCursor(False)
                RC.Print(Var.MessagesData["Dashboard"]["AskActionUnknown"],
                    AskActionVP["Y"], AskActionVP["X"], 
                    MaxColumns = AskActionVP["Width"],
                    JustifyText = RC.Justify.Left)
                time.sleep(Var.GameData["Game"]["WaitOnActionError"])
            elif ActionArgument.isdigit():
                # convert action argument to integer
                ActionArgument = int(ActionArgument)

            if IsCommandOK:
                # save last action
                Var.LastPlayerCommand = Command
                # return action
                return ActionName, ActionArgument



def ExecutePlayerAction(
    ActionName, 
    ActionArgument):
    """
        Execute player action with specified argument 
    """

    ActionMessage = ""
    
    if ActionName == "Quit":
        ActionOK = True
        # save game
        Var.CurrentMessage = Var.MessagesData["Dashboard"]["Actions"]["Quit"]["Success"]
        # refresh view
        ShowView(ViewParts = ["Message"])
        SaveGame()
        # wait for last Enter
        AskActionVP = Var.GameData["ViewPorts"]["Dashboard"]["AskAction"]
        RC.Print(Var.MessagesData["Dashboard"]["ConfirmQuit"],
            AskActionVP["Y"], AskActionVP["X"], 
            MaxColumns = AskActionVP["Width"],
            JustifyText = RC.Justify.Center)
        input()
        # stop main loop
        Var.GameRunning = False
            
    elif ActionName == "Move":
        ActionOK = True
        for Index in range(ActionArgument):
            (IsSuccess, Var.CurrentMessage, Event) = Move(Var.Player)
            MoveOtherCharacters()
            # refresh view
            ShowView(ViewParts = ["VitalSigns", "Counters", "Environment", "Message"])
            # check event
            CheckEvent(Event)
            # stop loop if movement is not possible
            if not IsSuccess:
                ActionArgument = Index
                if Index == 0:
                    ActionOK = False
                break

        # get action message
        ActionMessage = (
            Var.MessagesData["Dashboard"]["Actions"]["Move"]["Success"]
                .replace("{Steps}", str(ActionArgument)))

    elif ActionName == "TurnLeft":
        ActionOK = True
        # update direction
        Var.Player["Position"]["Direction"] = Var.GameData["Game"]["Directions"][Var.Player["Position"]["Direction"]]["NextLeft"]
        ActionMessage = Var.MessagesData["Dashboard"]["Actions"][ActionName]["Success"]
        # refresh view
        ShowMap(Var.Player["Position"]["Y"], Var.Player["Position"]["X"])
        ShowView(ViewParts = ["Environment"])

    elif ActionName == "TurnRight":
        ActionOK = True
        # update direction
        Var.Player["Position"]["Direction"] = Var.GameData["Game"]["Directions"][Var.Player["Position"]["Direction"]]["NextRight"]
        ActionMessage = Var.MessagesData["Dashboard"]["Actions"][ActionName]["Success"]
        # refresh view
        ShowMap(Var.Player["Position"]["Y"], Var.Player["Position"]["X"])
        ShowView(ViewParts = ["Environment"])

    elif ActionName == "UseObject":
        ActionOK = False
        if ActionArgument == 0 or ActionArgument > len(Var.ObjectsData["Backpack"]["Behaviors"]["Contains"]):
            # no object here
            Var.CurrentMessage = Var.MessagesData["Dashboard"]["Actions"]["UseObject"]["Failure"]
        else:
            # get object data
            CurrentObjectID = Var.ObjectsData["Backpack"]["Behaviors"]["Contains"][ActionArgument - 1]
            CurrentObjectData = Var.ObjectsData[CurrentObjectID]
            
            if CurrentObjectData["Behaviors"]["Usable"]:
                # object is usable
                if CurrentObjectData["Behaviors"]["RequiredMapElementsToUse"] is not None:
                    # object needs a specific map element to be used
                    if not Var.SeenElement in CurrentObjectData["Behaviors"]["RequiredMapElementsToUse"]:
                        # the element is not here
                        Var.CurrentMessage = (
                            Var.MessagesData["Dashboard"]["Actions"]["UseObject"]["Failure3"]
                                .replace("{Object}", 
                                    CurrentObjectData["Style"] 
                                    + Var.MessagesData[CurrentObjectID]["Name"] 
                                    + "[;]")
                            + "\n\n"
                            + Var.MessagesData[CurrentObjectID]["CantUse"])
                    else:
                        # the element is here
                        ActionOK = True
                        Var.Player["TotalActions"] += 1
                        Var.CurrentMessage = (
                            Var.MessagesData["Dashboard"]["Actions"]["UseObject"]["Success"]
                                .replace("{Object}", 
                                    CurrentObjectData["Style"] 
                                    + Var.MessagesData[CurrentObjectID]["Name"] 
                                    + "[;]")
                            + "\n\n"
                            + Var.MessagesData[CurrentObjectID]["Use"])
                        # remove prerequisite from map element and backpack if specified
                        if Var.MapElementsData[Var.SeenElement]["Behaviors"]["RemovePrerequisiteAfterUse"]:
                            # remove from map element
                            Var.MapElementsData[Var.SeenElement]["Behaviors"]["Prerequisites"].remove(CurrentObjectID)
                            # remove from backpack
                            Var.ObjectsData["Backpack"]["Behaviors"]["Contains"].remove(CurrentObjectID)
                        # update CanMoveOn for map element if specified
                        if (CurrentObjectData["Behaviors"]["CanMoveOnRequiredMapElementAfterUseIfNoMorePrerequisites"]
                            and (Var.MapElementsData[Var.SeenElement]["Behaviors"]["Prerequisites"] == None
                            or Var.MapElementsData[Var.SeenElement]["Behaviors"]["Prerequisites"] == []
                            or CurrentObjectID in Var.MapElementsData[Var.SeenElement]["Behaviors"]["Prerequisites"])):
                            Var.MapElementsData[Var.SeenElement]["Behaviors"]["CanMoveOn"] = True
                            if Var.SeenElement == "0":
                                # check if final door prerequisites are completed
                                Var.MapElementsData[Var.SeenElement]["Behaviors"]["Event"] = "WinGame"
                        # refresh view
                        ShowView(ViewParts = ["BackpackItems"])

                else:
                    Var.CurrentMessage = (
                        Var.MessagesData["Dashboard"]["Actions"]["UseObject"]["Success"]
                            .replace("{Object}", 
                                CurrentObjectData["Style"] 
                                + Var.MessagesData[CurrentObjectID]["Name"]
                                + "[;]"))
                    
                    # check and update item capacity if any
                    if CurrentObjectData["Behaviors"]["Capacity"] is not None:
                        # object has a capacity
                        if CurrentObjectData["Behaviors"]["Contains"] > 0:
                            # object still has charges
                            ActionOK = True
                            Var.Player["TotalActions"] += 1
                            CurrentObjectData["Behaviors"]["Contains"] -= 1
                            Var.CurrentMessage += (
                                    "\n\n" + 
                                    Var.MessagesData[CurrentObjectID]["Use"]
                                        .replace("{Contains}", 
                                            str(CurrentObjectData["Behaviors"]["Contains"])) 
                                    + "\n")
                            ShowView(ViewParts = ["BackpackItems"])
                        else:
                            # object is empty
                            Var.CurrentMessage += (
                                    "\n\n" + Var.MessagesData[CurrentObjectID]["CantUse"])
                    else:
                        # object has no capacity
                        ActionOK = True
                        Var.Player["TotalActions"] += 1
                        Var.CurrentMessage += (
                            "\n\n" + Var.MessagesData[CurrentObjectID]["Use"] + "\n")

                    # check if object is a charger
                    if CurrentObjectData["Behaviors"]["ChargeObjects"] is not None:
                        # object is a charger
                        ActionOK = True
                        Var.Player["TotalActions"] += 1
                        Var.CurrentMessage += "\n"
                        # get each object to charge
                        for ObjectToCharge in CurrentObjectData["Behaviors"]["ChargeObjects"]:
                            if ObjectToCharge in Var.ObjectsData["Backpack"]["Behaviors"]["Contains"]:
                                # object is in backpack
                                # charge it to maximum capacity
                                Var.ObjectsData[ObjectToCharge]["Behaviors"]["Contains"] = Var.ObjectsData[ObjectToCharge]["Behaviors"]["Capacity"]
                                Var.CurrentMessage += (
                                    Var.MessagesData["Dashboard"]["Actions"][ActionName]["Charged"]
                                        .replace("{Object}", 
                                            Var.ObjectsData[ObjectToCharge]["Style"] 
                                            + Var.MessagesData[ObjectToCharge]["Name"] 
                                            + "[;]")
                                    + "\n")
                            ShowView(ViewParts = ["BackpackItems"])

                if ActionOK:
                    # use action is possible, show message
                    ActionMessage = (
                        Var.MessagesData["Dashboard"]["Actions"]["UseObject"]["Success"]
                            .replace("{Object}", 
                                CurrentObjectData["Style"] 
                                + Var.MessagesData[CurrentObjectID]["Name"]
                                + "[;]"))
                    # update vital signs
                    Var.CurrentMessage += UpdateVitalSign("Health", CurrentObjectData)
                    Var.CurrentMessage += UpdateVitalSign("Hydration", CurrentObjectData)
                    Var.CurrentMessage += UpdateVitalSign("Satiety", CurrentObjectData)
            
            else:
                # object is not usable
                Var.CurrentMessage = (
                    Var.MessagesData["Dashboard"]["Actions"]["UseObject"]["Failure2"]
                        .replace("{Object}", 
                            CurrentObjectData["Style"] 
                            + Var.MessagesData[CurrentObjectID]["Name"]
                            + "[;]"))

        # refresh view
        ShowView(ViewParts = ["VitalSigns", "Message"])

    elif ActionName == "FillObject":
        ActionOK = False
        if ActionArgument == 0 or ActionArgument > len(Var.ObjectsData["Backpack"]["Behaviors"]["Contains"]):
            # no object here
            Var.CurrentMessage = Var.MessagesData["Dashboard"]["Actions"]["UseObject"]["Failure"]
        else:
            # get object data
            CurrentObjectID = Var.ObjectsData["Backpack"]["Behaviors"]["Contains"][ActionArgument - 1]
            CurrentObjectData = Var.ObjectsData[CurrentObjectID]
            
            if CurrentObjectData["Behaviors"]["RequiredMapElementsToFill"] is not None:
                # object needs a specific map element to be filled
                if not Var.SeenElement in CurrentObjectData["Behaviors"]["RequiredMapElementsToFill"]:
                    # the element is not here
                    ElementList = ""
                    # get all possible elements
                    for NeededElement in CurrentObjectData["Behaviors"]["RequiredMapElementsToFill"]:
                        ElementList += ( 
                            Var.MapElementsData[NeededElement]["Style"] 
                            + Var.MessagesData[NeededElement]["Name"].lower() 
                            + "[;], ")
                    Var.CurrentMessage = (
                        Var.MessagesData["Dashboard"]["Actions"]["FillObject"]["Failure"]
                            .replace("{Elements}", 
                                ElementList[:len(ElementList) - len(", ")]) 
                            .replace("{Object}", 
                                CurrentObjectData["Style"] 
                                + Var.MessagesData[CurrentObjectID]["Name"]
                                + "[;]") 
                        + "\n\n"
                        + Var.MessagesData[CurrentObjectID]["CantFill"])
                else:
                    # the element is here
                    ActionOK = True
                    Var.Player["TotalActions"] += 1
                    Var.CurrentMessage = (
                        Var.MessagesData["Dashboard"]["Actions"]["FillObject"]["Success"]
                            .replace("{Object}", 
                                CurrentObjectData["Style"] 
                                + Var.MessagesData[CurrentObjectID]["Name"] 
                                + "[;]") 
                            .replace("{Element}", 
                                Var.MapElementsData[Var.SeenElement]["Style"] 
                                + Var.MessagesData[Var.SeenElement]["Name"]
                                + "[;]") 
                        + "\n\n"
                        + Var.MessagesData[CurrentObjectID]["Fill"])
                    # charge object to maximum capacity
                    CurrentObjectData["Behaviors"]["Contains"] = CurrentObjectData["Behaviors"]["Capacity"]
                    # update objects vital signs
                    CurrentObjectData["Behaviors"]["Health"] = Var.MapElementsData[Var.SeenElement]["Behaviors"]["GiveWater"]["Health"]
                    CurrentObjectData["Behaviors"]["Hydration"] = Var.MapElementsData[Var.SeenElement]["Behaviors"]["GiveWater"]["Hydration"]
                    # refresh view
                    ShowView(ViewParts = ["BackpackItems"])

            else:
                # object is not fillable
                Var.CurrentMessage = (
                    Var.MessagesData["Dashboard"]["Actions"]["FillObject"]["Failure2"]
                        .replace("{Object}", 
                            CurrentObjectData["Style"] 
                            + Var.MessagesData[CurrentObjectID]["Name"]
                            + "[;]"))
                
            if ActionOK:
                # use action is possible, show message
                ActionMessage = (
                    Var.MessagesData["Dashboard"]["Actions"]["FillObject"]["Success"]
                        .replace("{Object}", 
                            CurrentObjectData["Style"] 
                                + Var.MessagesData[CurrentObjectID]["Name"] 
                                + "[;]") 
                        .replace("{Element}", 
                            Var.MapElementsData[Var.SeenElement]["Style"] 
                                + Var.MessagesData[Var.SeenElement]["Name"].lower() 
                                + "[;]"))
            
        # refresh view
        ShowView(ViewParts = ["VitalSigns", "Message"])

    elif ActionName == "DropObject":
        ActionOK = False
        if ActionArgument == 0 or ActionArgument > len(Var.ObjectsData["Backpack"]["Behaviors"]["Contains"]):
            # no object here
            Var.CurrentMessage = Var.MessagesData["Dashboard"]["Actions"]["DropObject"]["Failure"]
        elif Var.SeenObject.strip() != "" or not Var.MapElementsData[Var.SeenElement]["Behaviors"]["CanMoveOn"]:
            # there is already an object here or map element is not appropriate
            Var.CurrentMessage = Var.MessagesData["Dashboard"]["Actions"]["DropObject"]["Failure2"]
        else:
            # get object data
            CurrentObjectID = Var.ObjectsData["Backpack"]["Behaviors"]["Contains"][ActionArgument - 1]
            CurrentObjectData = Var.ObjectsData[CurrentObjectID]
            if not CurrentObjectData["Behaviors"]["Dropable"]:
                # object cannot be dropped
                Var.CurrentMessage = Var.MessagesData[CurrentObjectID]["Drop"]
            else:
                # drop object
                ActionOK = True
                Var.Player["TotalActions"] += 1
                # remove object from backpack
                Var.ObjectsData["Backpack"]["Behaviors"]["Contains"].remove(CurrentObjectID)
                # add object to objects layer
                Var.ObjectsLayer[Var.SeenCoordinates["Y"]][Var.SeenCoordinates["X"]] = CurrentObjectID
                # refresh map and view
                ShowMap(Var.SeenCoordinates["Y"], Var.SeenCoordinates["X"])
                ShowView(ViewParts = ["BackpackItems", "Environment"])
                # get message
                Var.CurrentMessage = (
                    Var.MessagesData["Dashboard"]["Actions"]["DropObject"]["Success"]
                        .replace("{Object}", 
                            CurrentObjectData["Style"] 
                                + Var.MessagesData[CurrentObjectID]["Name"] 
                                + "[;]") 
                    + "\n\n"
                    + Var.MessagesData[CurrentObjectID]["Drop"])           
                
            if ActionOK:
                # drop action is possible, show message
                ActionMessage = (
                    Var.MessagesData["Dashboard"]["Actions"]["DropObject"]["Success"]
                        .replace("{Object}", CurrentObjectData["Style"] 
                            + Var.MessagesData[CurrentObjectID]["Name"] 
                            + "[;]")) 
            
        # refresh view
        ShowView(ViewParts = ["Message"])

    elif ActionName == "PickUp":
        ActionOK = False
        if Var.ObjectsLayer[Var.SeenCoordinates["Y"]][Var.SeenCoordinates["X"]].strip() == "":
            # no object here
            Var.CurrentMessage = Var.MessagesData["Dashboard"]["Actions"]["PickUp"]["Failure"]
        else:
            # get object data
            CurrentObjectID = Var.SeenObject
            CurrentObjectData = Var.ObjectsData[CurrentObjectID]
            if not CurrentObjectData["Behaviors"]["Pickable"]: 
                # object is not pickable
                Var.CurrentMessage = (
                    Var.MessagesData["Dashboard"]["Actions"]["PickUp"]["Failure2"]
                        .replace("{Object}", 
                            CurrentObjectData["Style"] 
                                + Var.MessagesData[CurrentObjectID]["Name"] 
                                + "[;]")) 
            elif len(Var.ObjectsData["Backpack"]["Behaviors"]["Contains"]) == Var.ObjectsData["Backpack"]["Behaviors"]["Capacity"]:
                # backpack is already full
                Var.CurrentMessage = (
                    Var.MessagesData["Dashboard"]["Actions"]["PickUp"]["Failure2"]
                        .replace("{Object}", 
                            CurrentObjectData["Style"] 
                                + Var.MessagesData[CurrentObjectID]["Name"] 
                                + "[;]"))
            else:
                # pick up object
                ActionOK = True
                Var.Player["TotalActions"] += 1
                # add object to backpack
                Var.ObjectsData["Backpack"]["Behaviors"]["Contains"].append(CurrentObjectID)
                # remove object from objects layer
                Var.ObjectsLayer[Var.SeenCoordinates["Y"]][Var.SeenCoordinates["X"]] = ""
                # refresh map and view
                ShowMap(Var.SeenCoordinates["Y"], Var.SeenCoordinates["X"])
                ShowView(ViewParts = ["BackpackItems", "Environment"])
                # get message
                Var.CurrentMessage = (
                    Var.MessagesData["Dashboard"]["Actions"]["PickUp"]["Success"]
                        .replace("{Object}", 
                            CurrentObjectData["Style"] 
                                + Var.MessagesData[CurrentObjectID]["Name"] 
                                + "[;]") 
                    + "\n\n"
                    + Var.MessagesData[CurrentObjectID]["PickUp"])           
                
                if ActionOK:
                    # pick up action is possible, show message
                    ActionMessage = (
                        Var.MessagesData["Dashboard"]["Actions"]["PickUp"]["Success"]
                            .replace("{Object}", CurrentObjectData["Style"] 
                                + Var.MessagesData[CurrentObjectID]["Name"] 
                                + "[;]")) 
            
        # refresh view
        ShowView(ViewParts = ["Message"])

    elif ActionName == "Rest":
        ActionOK = False
        OnElement = Var.MapLayer[Var.Player["Position"]["Y"]][Var.Player["Position"]["X"]]
        OnElementData = Var.MapElementsData[OnElement]
        if not OnElementData["Behaviors"]["CanRest"]:
            # cannot rest here
            Var.CurrentMessage = (
                Var.MessagesData["Dashboard"]["Actions"]["Rest"]["Failure"]
                    .replace("{Element}", 
                        OnElementData["Style"] 
                        + Var.MessagesData[OnElement]["Name"].lower()
                        + "[;]"))
        else:
            # rest for appropriate time
            ActionOK = True
            Var.Player["TotalActions"] += 1
            # get messages
            ActionMessage = (
                Var.MessagesData["Dashboard"]["Actions"]["Rest"]["Success"]
                    .replace("{Hours}", str(ActionArgument)))
            Var.CurrentMessage = ActionMessage + "\n"

            RestData = Var.GameData["Game"]["Actions"]["Rest"]
            # update vital signs
            Var.CurrentMessage += UpdateVitalSign("Health", Value = RestData["Health"] * ActionArgument)
            Var.CurrentMessage += UpdateVitalSign("Hydration", Value = RestData["Hydration"] * ActionArgument)
            Var.CurrentMessage += UpdateVitalSign("Satiety", Value = RestData["Satiety"] * ActionArgument)

        # refresh view
        ShowView(ViewParts = ["VitalSigns", "Message"])

    elif ActionName == "GetHelp":
        # show help screen
        pass

    # else:
    #     # other known action
    #     ActionMessage = f"Faire {ActionArgument} fois l'action {ActionName}"
    
    # update messages and action counter
    if ActionOK and ActionMessage != "":
        Util.ManageMessageHistory(ActionMessage, Var.ActionsHistory)
    
    # refresh view
    ShowView(ViewParts = ["Counters", "ActionHistory", "Message"])



def Move(
    Character):
    """
        Try to move character in current direction
        If possible update its coordinates
        Returns true/false matching mouvement success, appropriate message and event if any
    """

    Event = None
    ElementAtCurrentPosition = Var.MapElementsData[Var.MapLayer[Character["Position"]["Y"]][Character["Position"]["X"]]]

    # define new position
    NewX = Character["Position"]["X"] + Var.GameData["Game"]["Directions"][Character["Position"]["Direction"]]["DeltaX"]
    NewY = Character["Position"]["Y"] + Var.GameData["Game"]["Directions"][Character["Position"]["Direction"]]["DeltaY"]

    # check if no map element obstacle
    try:
        ElementAtNewPosition = Var.MapElementsData[Var.MapLayer[NewY][NewX]]
    except IndexError:
        # player is going out of map (exit to main)
        # return message and current position event
        return (True,
            (Var.MessagesData[Var.MapLayer[Character["Position"]["Y"]][Character["Position"]["X"]]]["MoveOn"]
                .replace("{Element}", ElementAtCurrentPosition["Style"] + Var.MessagesData[Var.MapLayer[Character["Position"]["Y"]][Character["Position"]["X"]]]["Name"].lower() + "[;]")), 
            ElementAtCurrentPosition["Behaviors"]["Event"])

    if not ElementAtNewPosition["Behaviors"]["CanMoveOn"]:
        # move is not possible
        Prerequisites = ""
        # check for missing prerequisites if any
        if ElementAtNewPosition["Behaviors"]["Prerequisites"] is not None:
            for Prereq in ElementAtNewPosition["Behaviors"]["Prerequisites"]:
                if Prerequisites != "":
                    Prerequisites += ", "
                Prerequisites += Var.ObjectsData[Prereq]["Style"] + Var.MessagesData[Prereq]["Name"] + "[;]"
        Message = (
            f"{Var.MessagesData['Dashboard']['Actions']['Move']['Failure']}\n\n{Var.MessagesData[Var.MapLayer[NewY][NewX]]['CantMoveOn']}"
            .replace("{Prerequisites}", Prerequisites))
        return (
            False, 
            Message, 
            ElementAtNewPosition["Behaviors"]["Event"])
    else:
        # get other character at new position
        CharacterHere = [
            CharacterHere for CharacterHere in Var.CharactersData 
            if CharacterHere["Name"] != Character["Name"]
                and CharacterHere["CurrentMap"] == Var.Player["CurrentMap"] 
                and CharacterHere["Position"]["X"] == NewX and CharacterHere["Position"]["Y"] == NewY]
        if len(CharacterHere) == 1:
            # other character is blocking movement
            CharacterHere = CharacterHere[0]
            return (False,
                f"{Var.MessagesData[CharacterHere['Name']]['Name']}.\n\n{Var.MessagesData[CharacterHere['Name']]['Talk']}", 
                CharacterHere["Event"])
    
    # movement possible
    # update character position
    OldX = Character["Position"]["X"]
    OldY = Character["Position"]["Y"]
    Character["Position"]["X"] = NewX
    Character["Position"]["Y"] = NewY
    # remove character from previous position
    ShowMap(OldY, OldX)
    # place character at new position
    ShowMap(NewY, NewX)
    # get message
    Message = (
        Var.MessagesData[Var.MapLayer[NewY][NewX]]["MoveOn"]
        .replace("{Element}", ElementAtNewPosition["Style"] + Var.MessagesData[Var.MapLayer[NewY][NewX]]["Name"].lower() + "[;]")
        + "\n")
    # update character vital signs
    Message += UpdateVitalSign("Health", ElementAtNewPosition)
    Message += UpdateVitalSign("Hydration", ElementAtNewPosition)
    Message += UpdateVitalSign("Satiety", ElementAtNewPosition)
    # update counters
    Character["TotalMovements"] += 1
    # return message and event
    return (True,
        Message,
        ElementAtNewPosition["Behaviors"]["Event"])



def MoveOtherCharacters():
    """
        Move other characters if any on the map
    """
    pass



def CheckEvent(Event):
    """
        Check and execute event if appropriate
    """
    
    if Event is not None:
        
        if type(Event) is dict:
            # event is a dictionnary (map change)
            Var.Player["CurrentMap"] = Event["Map"]
            Var.Player["Position"]["X"] = Event["X"]
            Var.Player["Position"]["Y"] = Event["Y"]
            Var.Player["Position"]["Direction"] = Event["Direction"]
            GetMapLayersAndViewPort()
            ShowView()

        elif Event == "StartChallenge1":
            # start Challenge 1
            Chal1.StartChallenge()

        elif Event == "StartChallenge2":
            # start Challenge 2
            Chal2.StartChallenge()

        elif Event == "SwitchLetter":
            # switch letter in temple
            Chal2.SwitchLetter(Var.CurrentChallengeData["CurrentLetter"], False)
            Chal2.SwitchLetter(Var.SeenElement)
            ShowView(ViewParts = ["EncryptedCredo"])

        elif Event == "StartChallenge3":
            # start Challenge 3
            Chal3.StartChallenge()

        elif Event == "WinGame":
            # game won
            # stop main loop
            Var.GameRunning = False
            # show end screen
            ShowView("StartEnd", ViewParts = ["End", "Win"], ClearScreen = True)


def UpdateVitalSign(
    VitalSign,
    ElementData = None,
    Value = None):
    """
        Update vital sign with map element, object data or absolute values
        Return appropriate message
    """

    # get value
    if Value is None and ElementData is not None and ElementData["Behaviors"][VitalSign] != 0:
        Value = ElementData["Behaviors"][VitalSign]

    if Value is not None:
        # update player data
        Var.Player[VitalSign] = min(
            Var.Player[VitalSign] + Value,
            Var.Player["Max" + VitalSign])
        # show appropriate message
        MessageName = "You" + ("Earn" if Value > 0 else "Loose")
        return ("\n" +
            Var.MessagesData["Dashboard"][MessageName]
            .replace("{Number}", str(abs(Value)))
            .replace("{VitalSign}", Var.GameData["Game"]["VitalSigns"][VitalSign]["Color"] + Var.MessagesData["Dashboard"][VitalSign] + "[;]"))

    return ""



def SaveGame():
    """
        Player quits, save game
    """
    pass



def WinGame():
    """
        Player wins game
    """
    pass



# # Test code
# if __name__ == "__main__":
#     Initialization()