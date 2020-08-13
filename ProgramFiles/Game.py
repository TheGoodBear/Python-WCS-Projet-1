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
    # load map data and prepare layers
    Var.MapLayer, BlankLayer = Util.LoadMap(Var.ResourcesFolder, "Map")
    Var.ObjectsLayer = list(BlankLayer)
    Var.CharactersLayer = list(BlankLayer)
    # update Map viewport so it matches map size
    MapViewPort = Var.GameData["Views"]["Main"]["MapViewPort"]
    DeltaWidth = MapViewPort["Width"] - len(Var.MapLayer[0])
    DeltaHeight = MapViewPort["Height"] - len(Var.MapLayer)
    MapViewPort["X"] += DeltaWidth // 2 
    MapViewPort["Y"] += DeltaHeight // 2 
    MapViewPort["Width"] -= DeltaWidth
    MapViewPort["Height"] -= DeltaHeight
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

    # ShowView(Var.GameData["Game"]["CurrentView"], ClearScreen = True)
    Var.GameData["Game"]["CurrentView"] = "Main"
    ShowView(Var.GameData["Game"]["CurrentView"], ClearScreen = True)
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
    ViewName,
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

    LineOffset = 0
    for Index, Line in enumerate(Var.ViewsData[ViewName]):
        RC.Print(Line, 
            Var.GameData["Views"][ViewName]["WindowViewPort"]["Y"] + Index, 1, 
            JustifyText = RC.Justify.Center, 
            MaxColumns = Var.GameData["Game"]["WindowWidth"])

    # show view content
    if ViewName == "Start":

        RC.ShowCursor(False)

        # viewports data
        TitleVP = Var.GameData["Views"][ViewName]["TitleViewPort"]
        TextVP = Var.GameData["Views"][ViewName]["TextViewPort"]
        AskVP = Var.GameData["Views"][ViewName]["AskViewPort"]

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

        # text page 1
        LineOffset = 0
        if Var.MessagesData["Game"]["Image"] is not None:
            LineOffset += RC.Print(Var.MessagesData["Game"]["Image"],
                TextVP["Y"], TextVP["X"],
                JustifyText = RC.Justify.Center,
                MaxColumns = TextVP["Width"],
                Speed = RC.PrintSpeed.UltraFast)

        RC.Print(Var.MessagesData["Game"]["History"],          
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = TextVP["Width"])
        RC.Print(Var.MessagesData["Game"]["AskContinue"],          
            AskVP["Y"], AskVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = AskVP["Width"],
            Speed = RC.PrintSpeed.Fast)
        RC.PlaceCursorAt(
            AskVP["Y"], 
            AskVP["X"] + len(Var.MessagesData["Game"]["AskContinue"]))
        input("")

        # clear text between pages
        RC.ClearConsole(
            TextVP["Y"], TextVP["X"], 
            TextVP["Width"], TextVP["Height"])
        RC.ClearConsole(
            AskVP["Y"], AskVP["X"], 
            AskVP["Width"], AskVP["Height"])

        # text page 2
        LineOffset = 0
        LineOffset += 1 + RC.Print(Var.MessagesData["Game"]["Rules"],          
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = TextVP["Width"])
        
        RC.PlaceCursorAt(TextVP["Y"] + LineOffset, TextVP["X"])
        RC.ShowCursor()
        Var.CharactersData["Player"]["Name"] = Util.GetUserInput(
            Var.MessagesData["Game"]["AskName"])
        RC.ShowCursor(False)
        Message = (Var.MessagesData["Game"]["Hello"]
            .replace("{Name}", Var.CharactersData["Player"]["Name"]))
        LineOffset += 1 + RC.Print(Message,
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = TextVP["Width"])

        LineOffset += 1 + RC.Print(Var.MessagesData["Game"]["AskSex1"], 
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = TextVP["Width"])
        RC.PlaceCursorAt(TextVP["Y"] + LineOffset, TextVP["X"])
        RC.ShowCursor()
        Var.CharactersData["Player"]["Sex"] = Util.GetUserInput(
            Var.MessagesData["Game"]["AskSex2"], 
            PossibleValues = list(Var.GameData["Game"]["Sex"].keys())).upper()
        RC.ShowCursor(False)
        Message = (Var.MessagesData["Game"]["Hello2"]
            .replace("{ColoredName}", 
                Var.GameData["Game"]["Sex"][Var.CharactersData["Player"]["Sex"]]["Color"] + Var.CharactersData["Player"]["Name"] + "[;]")
            .replace("{Symbol}", 
                Var.GameData["Game"]["Sex"][Var.CharactersData["Player"]["Sex"]]["Color"] + Var.CharactersData["Player"]["Image"] + "[;]"))
        LineOffset += RC.Print(Message,          
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = TextVP["Width"])

        RC.Print(Var.MessagesData["Game"]["AskReady"],          
            AskVP["Y"], AskVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = AskVP["Width"],
            Speed = RC.PrintSpeed.Fast)
        RC.PlaceCursorAt(
            AskVP["Y"], 
            AskVP["X"] + len(Var.MessagesData["Game"]["AskReady"]))
        input("")
   
    elif ViewName == "Main":

        if ViewParts is None or "Map" in ViewParts:
            ShowMap()

        # viewports data
        DashboardVP = Var.GameData["Views"][ViewName]["DashboardViewPort"]
        TitleVP = Var.GameData["Views"][ViewName]["TitleViewPort"]
        PlayerVP = Var.GameData["Views"][ViewName]["PlayerViewPort"]
        VitalSignsVP = Var.GameData["Views"][ViewName]["VitalSignsViewPort"]
        CountersVP = Var.GameData["Views"][ViewName]["CountersViewPort"]
        BackpackTitleVP = Var.GameData["Views"][ViewName]["BackpackTitleViewPort"]
        BackpackItemsVP = Var.GameData["Views"][ViewName]["BackpackItemsViewPort"]
        EnvironmentVP = Var.GameData["Views"][ViewName]["EnvironmentViewPort"]
        AskActionVP = Var.GameData["Views"][ViewName]["AskActionViewPort"]
        ActionHistoryTitleVP = Var.GameData["Views"][ViewName]["ActionHistoryTitleViewPort"]
        ActionHistoryVP = Var.GameData["Views"][ViewName]["ActionHistoryViewPort"]
        MessageVP = Var.GameData["Views"][ViewName]["MessageViewPort"]
        
        # dashboard
        # title view part
        LineOffset = 0
        LineOffset += RC.Print(f"[B;W]{Var.MessagesData['Game']['Title']}",
            TitleVP["Y"], TitleVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = TitleVP["Width"])
        Message = (Var.MessagesData["Dashboard"]["FullVersion"]
            .replace("{VersionNumber}", Var.GameData["Game"]["VersionNumber"])
            .replace("{VersionDate}", Var.GameData["Game"]["VersionDate"]))
        RC.Print(f"{Message}",
            TitleVP["Y"] + LineOffset, TitleVP["X"],
            JustifyText = RC.Justify.Center,
            MaxColumns = TitleVP["Width"])
        # player view part
        LineOffset = 0
        Message = (Var.GameData["Game"]["Sex"][Var.CharactersData["Player"]["Sex"]]["Color"] + 
            Var.MessagesData["Dashboard"]["PlayerFullName"]
                .replace("{ColoredName}", Var.CharactersData["Player"]["Name"])
                .replace("{SexSymbol}", Var.GameData["Game"]["Sex"][Var.CharactersData["Player"]["Sex"]]["Symbol"]))
        RC.Print(Message,          
            PlayerVP["Y"] + LineOffset, TitleVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = TitleVP["Width"])
        # vital signs view part
        if ViewParts is None or "VitalSigns" in ViewParts:
            LineOffset = 0
            HealthLength = (Var.GameData["Game"]["VitalSigns"]["BarLength"] * 
                (Var.CharactersData["Player"]["Health"] * 100 // Var.CharactersData["Player"]["MaxHealth"])
                // 100)
            Message = (Var.MessagesData["Dashboard"]["PlayerHealth"]
                .replace(
                    "{HealthCounter}", 
                    f"{Var.GameData['Game']['VitalSigns']['Health']['Color']}{''.ljust(HealthLength, Var.GameData['Game']['VitalSigns']['Health']['Symbol'])}[;]"))
            LineOffset += RC.Print(Message,          
                VitalSignsVP["Y"] + LineOffset, VitalSignsVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = VitalSignsVP["Width"])
            HydrationLength = (Var.GameData["Game"]["VitalSigns"]["BarLength"] * 
                (Var.CharactersData["Player"]["Hydration"] * 100 // Var.CharactersData["Player"]["MaxHydration"])
                // 100)
            Message = (Var.MessagesData["Dashboard"]["PlayerHydration"]
                .replace(
                    "{HydrationCounter}", 
                    f"{Var.GameData['Game']['VitalSigns']['Hydration']['Color']}{''.ljust(HydrationLength, Var.GameData['Game']['VitalSigns']['Hydration']['Symbol'])}[;]"))
            LineOffset += RC.Print(Message,          
                VitalSignsVP["Y"] + LineOffset, VitalSignsVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = VitalSignsVP["Width"])
            SatietyLength = (Var.GameData["Game"]["VitalSigns"]["BarLength"] * 
                (Var.CharactersData["Player"]["Satiety"] * 100 // Var.CharactersData["Player"]["MaxSatiety"])
                // 100)
            Message = (Var.MessagesData["Dashboard"]["PlayerSatiety"]
                .replace(
                    "{SatietyCounter}", 
                    f"{Var.GameData['Game']['VitalSigns']['Satiety']['Color']}{''.ljust(SatietyLength, Var.GameData['Game']['VitalSigns']['Satiety']['Symbol'])}[;]"))
            LineOffset += RC.Print(Message,          
                VitalSignsVP["Y"] + LineOffset, VitalSignsVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = VitalSignsVP["Width"])
        # counters view part
        if ViewParts is None or "Counters" in ViewParts:
            LineOffset = 0
            Message = (Var.MessagesData["Dashboard"]["CounterMovements"]
                .replace(
                    "{TotalMovements}", 
                    f"{Var.CharactersData['Player']['TotalMovements']}"))
            RC.Print(Message,          
                CountersVP["Y"], CountersVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = CountersVP["Width"] // 2)
            Message = (Var.MessagesData["Dashboard"]["CounterActions"]
                .replace(
                    "{TotalActions}", 
                    f"{Var.CharactersData['Player']['TotalActions']}"))
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
            for Index, Item in enumerate(Var.ObjectsData['Backpack']['Behaviors']['Contains']):
                Message = f"{Var.ObjectsData[Item]['Style']}{str(Index + 1).rjust(2)}) {Var.MessagesData[Item]['Name']}"
                RC.Print(Message,          
                    BackpackItemsVP["Y"] + LineOffset + Index, BackpackItemsVP["X"],
                    JustifyText = RC.Justify.Left, 
                    MaxColumns = BackpackItemsVP["Width"])
        # environement view part
        if ViewParts is None or "Environment" in ViewParts:
            LineOffset = 0
            Message = (Var.MessagesData["Dashboard"]["PlayerOrientation"]
                .replace(
                    "{DirectionName}", 
                    f"{Var.MessagesData['Dashboard']['Directions'][Var.CharactersData['Player']['Direction']]}")
                .replace(
                    "{DirectionSymbol}", 
                    f"{Var.GameData['Game']['Directions'][Var.CharactersData['Player']['Direction']]['Symbol']}"))
            LineOffset += RC.Print(Message,          
                EnvironmentVP["Y"] + LineOffset, EnvironmentVP["X"],
                JustifyText = RC.Justify.Center, 
                MaxColumns = EnvironmentVP["Width"])
            OnElement = (Var.MapLayer
                [Var.CharactersData['Player']['Y']]
                [Var.CharactersData['Player']['X']])
            Message = (Var.MessagesData["Dashboard"]["PlayerWalksOn"]
                .replace(
                    "{Element}", 
                    f"{Var.MapElementsData[OnElement]['Style']}{str(Var.MessagesData[OnElement]['Name']).lower()}[;] ({Var.MapElementsData[OnElement]['Style']}{Var.MapElementsData[OnElement]['Image']}[;])"))
            LineOffset += RC.Print(Message,          
                EnvironmentVP["Y"] + LineOffset, EnvironmentVP["X"],
                JustifyText = RC.Justify.Center, 
                MaxColumns = EnvironmentVP["Width"])
            SeenElement = (
                Var.MapLayer[
                    Var.CharactersData['Player']['Y'] 
                    + Var.GameData['Game']['Directions']
                        [Var.CharactersData['Player']['Direction']]['DeltaY']]
                    [Var.CharactersData['Player']['X'] 
                    + Var.GameData['Game']['Directions']
                        [Var.CharactersData['Player']['Direction']]['DeltaX']])
            Message = (Var.MessagesData["Dashboard"]["PlayerSees"]
                .replace(
                    "{Element}", 
                    f"{Var.MapElementsData[SeenElement]['Style']}{str(Var.MessagesData[SeenElement]['Name']).lower()}[;] ({Var.MapElementsData[SeenElement]['Style']}{Var.MapElementsData[SeenElement]['Image']}[;])"))
            LineOffset += RC.Print(Message,          
                EnvironmentVP["Y"] + LineOffset, EnvironmentVP["X"],
                JustifyText = RC.Justify.Center, 
                MaxColumns = EnvironmentVP["Width"])
        # action history title view part
        LineOffset = 0
        RC.Print(Var.MessagesData["Dashboard"]["ActionHistoryTitle"],          
            BackpackTitleVP["Y"] + LineOffset, BackpackTitleVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = BackpackTitleVP["Width"])
        # action history view part
        if ViewParts is None or "ActionHistory" in ViewParts:
            RC.ClearConsole(
                ActionHistoryVP["Y"], ActionHistoryVP["X"], 
                ActionHistoryVP["Width"], ActionHistoryVP["Height"])
            LineOffset = 0
            for Index, Action in enumerate(Var.ActionsHistory[-ActionHistoryVP["Height"]:]):
                Message = f"{str(Index).rjust(4)}) {Action}"
                RC.Print(Message,          
                    ActionHistoryVP["Y"] + LineOffset + Index, ActionHistoryVP["X"],
                    JustifyText = RC.Justify.Left, 
                    MaxColumns = ActionHistoryVP["Width"])
        # message view part
        if ViewParts is None or "Message" in ViewParts:
            RC.ClearConsole(
                MessageVP["Y"], MessageVP["X"], 
                MessageVP["Width"], MessageVP["Height"])
            LineOffset = 0
            RC.Print(Var.CurrentMessage,          
                MessageVP["Y"] + LineOffset, MessageVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = MessageVP["Width"])
        # ask action view part
        if ViewParts is None or "AskAction" in ViewParts:
            RC.Print(Var.MessagesData["Dashboard"]["AskAction"],          
                AskActionVP["Y"], AskActionVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = AskActionVP["Width"])
            RC.PlaceCursorAt(
                AskActionVP["Y"], 
                AskActionVP["X"] + len(Var.MessagesData["Game"]["AskAction"]))
            input("")

    elif ViewName == "Challenge":

        # viewports data
        DashboardVP = Var.GameData["Views"][ViewName]["DashboardViewPort"]
        ChallengeVP = Var.GameData["Views"][ViewName]["ChallengeViewPort"]
        TitleVP = Var.GameData["Views"][ViewName]["TitleViewPort"]
        TextVP = Var.GameData["Views"][ViewName]["TextViewPort"]
        AskVP = Var.GameData["Views"][ViewName]["AskViewPort"]



def ShowMap(
    Y = None, 
    X = None):
    """
        Show map on view with all layers (map → objects → characters)

        Full map if no coordinates specified,
        or only refresh map on specified coordinates
    """

    if X == None or Y == None: 
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
        Var.GameData["Views"]["Main"]["MapViewPort"]["Y"] + Y,
        Var.GameData["Views"]["Main"]["MapViewPort"]["X"] + X,
        JumpLineAfter = False)

    # object layer
    if Var.ObjectsLayer[Y][X] != "":
        # get object element data for current object
        MapObject = Var.ObjectsData[Var.ObjectsLayer[Y][X]]
        # draw
        RC.Print(
            f"{MapObject['Style']}{MapObject['Image']}[;]",
            Var.GameData["Views"]["Main"]["MapViewPort"]["Y"] + Y,
            Var.GameData["Views"]["Main"]["MapViewPort"]["X"] + X,
            JumpLineAfter = False)
