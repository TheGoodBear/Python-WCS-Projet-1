# coding: utf-8

# Imports modules
import time

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


    # ShowView(Var.GameData["Game"]["CurrentView"], ClearScreen = True)
    Var.GameData["Game"]["CurrentView"] = "Main"
    ShowView(Var.GameData["Game"]["CurrentView"], ClearScreen = True)
    while Var.GameRunning:
        (ActionName, ActionArgument) = AskPlayerAction()
        ExecutePlayerAction(ActionName, ActionArgument)
        # ShowView(Var.GameData["Game"]["CurrentView"], ClearScreen = True)
    
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
    if ViewParts is None:
        # draw view template
        for Index, Line in enumerate(Var.ViewsData[ViewName]):
            RC.Print(Line, 
                Var.GameData["ViewPorts"][ViewName]["Window"]["Y"] + Index, 1, 
                JustifyText = RC.Justify.Center, 
                MaxColumns = Var.GameData["Game"]["WindowWidth"])

    # show view content
    if ViewName == "Start":

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

        # text page 1
        LineOffset = 0
        if Var.MessagesData["Game"]["Image"] is not None:
            LineOffset += RC.Print(Var.MessagesData["Game"]["Image"],
                TextVP["Y"], TextVP["X"],
                JustifyText = RC.Justify.Center,
                MaxColumns = TextVP["Width"],
                Speed = RC.PrintSpeed.UltraFast)[0]

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
            SpecificErrorMessage = "Ton nom doit faire entre 3 et 20 caractères.",
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

        LineOffset += 1 + RC.Print(Var.MessagesData["Game"]["AskSex1"], 
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Left, 
            MaxColumns = TextVP["Width"])[0]

        Sex = Util.GetUserInput(
            Var.MessagesData["Game"]["AskSex2"],
            PossibleValues = list(Var.MessagesData["Game"]["Sex"].keys()),
            SpecificErrorMessage = "Tu dois m'indiquer l'une des lettres entre parenthèses ci-dessus.",
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
                Var.Player["Style"] + Var.Player["Image"] + "[;]"))
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
   
    elif ViewName == "Main" or ViewName == "Challenge":

        # get viewport
        ViewPort = (Var.Player["CurrentMap"] 
            if not Var.Player["CurrentMap"][-1:].isdigit() 
            else Var.Player["CurrentMap"][:-1])

        RC.ShowCursor(False)

        # show map if specified
        if ViewParts is None or "Map" in ViewParts:
            ShowMap()

        # dashboard viewports data
        DashboardVP = Var.GameData["ViewPorts"]["Dashboard"]["Window"]
        TitleVP = Var.GameData["ViewPorts"]["Dashboard"]["Title"]
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
        LineOffset = 0
        LineOffset += RC.Print(f"[B;W]{Var.MessagesData['Game']['Title']}",
            TitleVP["Y"], TitleVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = TitleVP["Width"])[0]
        Message = (Var.MessagesData["Dashboard"]["FullVersion"]
            .replace("{VersionNumber}", Var.GameData["Game"]["VersionNumber"])
            .replace("{VersionDate}", Var.GameData["Game"]["VersionDate"]))
        RC.Print(f"{Message}",
            TitleVP["Y"] + LineOffset, TitleVP["X"],
            JustifyText = RC.Justify.Center,
            MaxColumns = TitleVP["Width"])
        # player view part
        LineOffset = 0
        Message = (Var.GameData["Game"]["Sex"][Var.Player["Sex"]]["Color"] + 
            Var.MessagesData["Dashboard"]["PlayerFullName"]
                .replace("{ColoredName}", Var.Player["Name"])
                .replace("{SexSymbol}", Var.GameData["Game"]["Sex"][Var.Player["Sex"]]["Symbol"]))
        RC.Print(Message,          
            PlayerVP["Y"] + LineOffset, TitleVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = TitleVP["Width"])
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
            for Index, Item in enumerate(Var.ObjectsData['Backpack']['Behaviors']['Contains']):
                Message = f"{Var.ObjectsData[Item]['Style']}{str(Index + 1).rjust(2)}) {Var.MessagesData[Item]['Name']}"
                # add empty of contents remaining if appropriate
                if Var.ObjectsData[Item]['Behaviors']["Contains"] is not None:
                    Message += (
                        f" ({Var.ObjectsData[Item]['Behaviors']['Contains']}/{Var.ObjectsData[Item]['Behaviors']['Capacity']})"
                        if Var.ObjectsData[Item]['Behaviors']["Contains"] > 0
                        else f" ({Var.MessagesData['Dashboard']['Empty']})")
                RC.Print(Message,          
                    BackpackItemsVP["Y"] + LineOffset + Index, BackpackItemsVP["X"],
                    JustifyText = RC.Justify.Left, 
                    MaxColumns = BackpackItemsVP["Width"])
        # environment view part
        if ViewParts is None or "Environment" in ViewParts:
            LineOffset = 0
            Message = (Var.MessagesData["Dashboard"]["PlayerOrientation"]
                .replace(
                    "{DirectionName}", 
                    f"{Var.MessagesData['Dashboard']['Directions'][Var.Player['Direction']]}")
                .replace(
                    "{DirectionSymbol}", 
                    f"{Var.GameData['Game']['Directions'][Var.Player['Direction']]['Symbol']}"))
            LineOffset += RC.Print(Message,          
                EnvironmentVP["Y"] + LineOffset, EnvironmentVP["X"],
                JustifyText = RC.Justify.Center, 
                MaxColumns = EnvironmentVP["Width"])[0]
            OnElement = (Var.MapLayer
                [Var.Player['Y']]
                [Var.Player['X']])
            SymbolString = ("" if Var.MapElementsData[OnElement]['Image'].strip() == ""
                else f" ({Var.MapElementsData[OnElement]['Style']}{Var.MapElementsData[OnElement]['Image']}[;])")
            Message = (Var.MessagesData["Dashboard"]["PlayerMovesOn"]
                .replace(
                    "{Element}", 
                    f"{Var.MapElementsData[OnElement]['Style']}{str(Var.MessagesData[OnElement]['Name']).lower()}[;]{SymbolString}"))
            LineOffset += RC.Print(Message,          
                EnvironmentVP["Y"] + LineOffset, EnvironmentVP["X"],
                JustifyText = RC.Justify.Center, 
                MaxColumns = EnvironmentVP["Width"])[0]
            try:
                SeenElement = (
                    Var.MapLayer[
                        Var.Player['Y'] 
                        + Var.GameData['Game']['Directions']
                            [Var.Player['Direction']]['DeltaY']]
                        [Var.Player['X'] 
                        + Var.GameData['Game']['Directions']
                            [Var.Player['Direction']]['DeltaX']])
                SymbolString = ("" if Var.MapElementsData[SeenElement]['Image'].strip() == ""
                    else f" ({Var.MapElementsData[SeenElement]['Style']}{Var.MapElementsData[SeenElement]['Image']}[;])")
                Message = (Var.MessagesData["Dashboard"]["PlayerSees"]
                    .replace(
                        "{Element}", 
                        f"{Var.MapElementsData[SeenElement]['Style']}{str(Var.MessagesData[SeenElement]['Name']).lower()}[;]{SymbolString}"))
            except IndexError:
                Message = (Var.MessagesData["Dashboard"]["PlayerSees"]
                    .replace(
                        "{Element}", 
                        f"{Var.MapElementsData[OnElement]['Style']}{str(Var.MessagesData[OnElement]['Name']).lower()}[;]{SymbolString}"))
            LineOffset += RC.Print(Message,          
                EnvironmentVP["Y"] + LineOffset, EnvironmentVP["X"],
                JustifyText = RC.Justify.Center, 
                MaxColumns = EnvironmentVP["Width"])[0]
        # action history title view part
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

    # elif ViewName == "Challenge":

        # # viewports data
        # ChallengeVP = Var.GameData["ViewPorts"][ViewName]["Windows"]
        # MapVP = Var.GameData["ViewPorts"][ViewName]["Map"]
        # TitleVP = Var.GameData["ViewPorts"][ViewName]["Title"]
        # TextVP = Var.GameData["ViewPorts"][ViewName]["Text"]
        # AskVP = Var.GameData["ViewPorts"][ViewName]["Ask"]



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
    X = None):
    """
        Show current map on view with all layers (map → objects → characters)

        Full map if no coordinates specified,
        or only refresh map on specified coordinates
    """

    if X == None or Y == None:
        # clear main viewport
        MainMapViewPort = Var.GameData["ViewPorts"]["Main"]["Map"] 
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
            if CharacterHere['CurrentMap'] == Var.Player["CurrentMap"] 
            and CharacterHere['X'] == X and CharacterHere['Y'] == Y]
    if len(CharacterHere) == 1:
        CharacterHere = CharacterHere[0]
        # draw
        RC.Print(
            f"{CharacterHere['Style']}{CharacterHere['Images'][CharacterHere['Direction']]}[;]",
            Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["Y"] + Y,
            Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["X"] + X,
            JumpLineAfter = False)


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
        # save game
        Var.CurrentMessage = Var.MessagesData["Dashboard"]["Actions"]["Quit"]["Success"]
        # refresh view
        ShowView(
            Var.GameData["Game"]["CurrentView"], 
            ViewParts = ["Message"])
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
        ActionMessage = (Var.MessagesData["Dashboard"]["Actions"]["Move"]["Success"]
            .replace("{Steps}", str(ActionArgument)))
        for Index in range(ActionArgument):
            (IsSuccess, Var.CurrentMessage, Event) = Move(Var.Player)
            MoveOtherCharacters()
            # refresh view
            ShowView(
                Var.GameData["Game"]["CurrentView"], 
                ViewParts = ["VitalSigns", "Counters", "Environment", "Message"])
            # stop loop if movement is not possible
            if not IsSuccess:
                ActionMessage = Var.MessagesData["Dashboard"]["Actions"]["Move"]["Failure"]
                break
            # check event
            CheckEvent(Event)

    elif ActionName == "TurnLeft":
        # update direction
        Var.Player["Direction"] = Var.GameData["Game"]["Directions"][Var.Player["Direction"]]["NextLeft"]
        ActionMessage = Var.MessagesData["Dashboard"]["Actions"][ActionName]["Success"]
        # refresh view
        ShowMap(Var.Player["Y"], Var.Player["X"])
        ShowView(
            Var.GameData["Game"]["CurrentView"], 
            ViewParts = ["Environment"])

    elif ActionName == "TurnRight":
        # update direction
        Var.Player["Direction"] = Var.GameData["Game"]["Directions"][Var.Player["Direction"]]["NextRight"]
        ActionMessage = Var.MessagesData["Dashboard"]["Actions"][ActionName]["Success"]
        # refresh view
        ShowMap(Var.Player["Y"], Var.Player["X"])
        ShowView(
            Var.GameData["Game"]["CurrentView"], 
            ViewParts = ["Environment"])

    elif ActionName == "UseObject":
        ActionOK = False
        if ActionArgument == 0 or ActionArgument > len(Var.ObjectsData['Backpack']['Behaviors']['Contains']):
            # no object here
            Var.CurrentMessage = Var.MessagesData["Dashboard"]["Actions"]["UseObject"]["Failure"]
        else:
            # get object data
            CurrentObjectID = Var.ObjectsData['Backpack']['Behaviors']['Contains'][ActionArgument - 1]
            CurrentObjectData = Var.ObjectsData[CurrentObjectID]
            Var.CurrentMessage = (
                Var.MessagesData["Dashboard"]["Actions"]["UseObject"]["Success"]
                .replace("{Object}", CurrentObjectData["Style"] + Var.MessagesData[CurrentObjectID]["Name"] + "[;]"))
            # check and update item capacity if any
            if CurrentObjectData["Behaviors"]["Capacity"] is not None:
                if CurrentObjectData["Behaviors"]["Contains"] > 0:
                    ActionOK = True
                    CurrentObjectData["Behaviors"]["Contains"] -= 1
                    Var.CurrentMessage += (
                            "\n\n" + Var.MessagesData[CurrentObjectID]["Use"].replace("{Contains}", str(CurrentObjectData["Behaviors"]["Contains"])) + "\n")
                    ShowView(Var.GameData["Game"]["CurrentView"], ["BackpackItems"])
                else:
                    Var.CurrentMessage += (
                            "\n\n" + Var.MessagesData[CurrentObjectID]["CantUse"])
            else:
                ActionOK = True
                Var.CurrentMessage += (
                     "\n\n" + Var.MessagesData[CurrentObjectID]["Use"] + "\n")

            if ActionOK:
                ActionMessage = (
                    Var.MessagesData["Dashboard"]["Actions"]["UseObject"]["Success"]
                    .replace("{Object}", CurrentObjectData["Style"] + Var.MessagesData[CurrentObjectID]["Name"] + "[;]"))
                # update vital signs
                Var.CurrentMessage += UpdateVitalSign("Health", CurrentObjectData)
                Var.CurrentMessage += UpdateVitalSign("Hydration", CurrentObjectData)
                Var.CurrentMessage += UpdateVitalSign("Satiety", CurrentObjectData)
            
            # refresh view
            ShowView(Var.GameData["Game"]["CurrentView"], ["VitalSigns", "Message"])


    else:
        ActionMessage = f"Faire {ActionArgument} fois l'action {ActionName}"
    
    # update messages
    if ActionMessage != "":
        Util.ManageMessageHistory(ActionMessage, Var.ActionsHistory)
    ShowView(Var.GameData["Game"]["CurrentView"], ["ActionHistory", "Message"])


def Move(
    Character):
    """
        Try to move character in current direction
        If possible update its coordinates
        Returns true/false matching mouvement success, appropriate message and event if any
    """

    Event = None
    ElementAtCurrentPosition = Var.MapElementsData[Var.MapLayer[Character["Y"]][Character["X"]]]

    # define new position
    NewX = Character["X"] + Var.GameData["Game"]["Directions"][Character["Direction"]]["DeltaX"]
    NewY = Character["Y"] + Var.GameData["Game"]["Directions"][Character["Direction"]]["DeltaY"]

    # check if no map element obstacle
    try:
        ElementAtNewPosition = Var.MapElementsData[Var.MapLayer[NewY][NewX]]
    except IndexError:
        # player is going out of map (exit to main)
        # return message and current position event
        return (True,
            (Var.MessagesData[Var.MapLayer[Character["Y"]][Character["X"]]]["MoveOn"]
                .replace("{Element}", ElementAtCurrentPosition["Style"] + Var.MessagesData[Var.MapLayer[Character["Y"]][Character["X"]]]["Name"].lower() + "[;]")), 
            ElementAtCurrentPosition["Behaviors"]["Event"])

    if not ElementAtNewPosition["Behaviors"]["CanMoveOn"]:
        # move is not possible
        return (False, 
            f"{Var.MessagesData['Dashboard']['Actions']['Move']['Failure']}\n{Var.MessagesData[Var.MapLayer[NewY][NewX]]['CantMoveOn']}", 
            None)
    else:
        # get other character at new position
        CharacterHere = [
            CharacterHere for CharacterHere in Var.CharactersData 
            if CharacterHere['Name'] != Character['Name']
                and CharacterHere['CurrentMap'] == Var.Player["CurrentMap"] 
                and CharacterHere['X'] == NewX and CharacterHere['Y'] == NewY]
        if len(CharacterHere) == 1:
            # other character is blocking movement
            CharacterHere = CharacterHere[0]
            return (False,
                f"{Var.MessagesData[CharacterHere['Name']]['Name']}.\n\n{Var.MessagesData[CharacterHere['Name']]['Talk']}", 
                CharacterHere["Event"])
    
    # movement possible
    # update character position
    OldX = Character["X"]
    OldY = Character["Y"]
    Character["X"] = NewX
    Character["Y"] = NewY
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
            Var.Player["X"] = Event["X"]
            Var.Player["Y"] = Event["Y"]
            Var.Player["Direction"] = Event["Direction"]
            GetMapLayersAndViewPort()
            ShowView(
                Var.GameData["Game"]["CurrentView"], 
                ViewParts = ["Map", "VitalSigns", "Counters", "Environment", "ActionHistory", "Message"])



def UpdateVitalSign(
    VitalSign,
    ElementData):
    """
        Update vital sign with map element or object data
        Return appropriate message
    """
    if ElementData["Behaviors"][VitalSign] != 0:
        # update player data
        Var.Player[VitalSign] = min(
            Var.Player[VitalSign] + ElementData["Behaviors"][VitalSign],
            Var.Player["Max" + VitalSign])
        # show appropriate message
        MessageName = "You" + ("Earn" if ElementData["Behaviors"][VitalSign] > 0 else "Loose")
        return ("\n" +
            Var.MessagesData["Dashboard"][MessageName]
            .replace("{Number}", str(abs(ElementData["Behaviors"][VitalSign])))
            .replace("{VitalSign}", Var.GameData["Game"]["VitalSigns"][VitalSign]["Color"] + Var.MessagesData["Dashboard"][VitalSign] + "[;]"))

    return ""



def SaveGame():
    """
        Player quits, save game
    """
    pass


# # Test code
# if __name__ == "__main__":
#     Initialization()