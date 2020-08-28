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
        Manage challenge 3 (Multi FizzBuzz)
    """

    TextVP = Var.GameData["ViewPorts"]["Challenge"]["Text"]
    AskVP = Var.GameData["ViewPorts"]["Challenge"]["Ask"]

    Answers = []

    # clean text area
    RC.ClearConsole(
        TextVP["Y"], TextVP["X"], 
        TextVP["Width"], TextVP["Height"])
    LineOffset = 0

    # print start message
    LineOffset += RC.Print(Var.MessagesData["Challenge3"]["Start"] + "\n\n",          
        TextVP["Y"] + LineOffset, TextVP["X"],
        JustifyText = RC.Justify.Center, 
        MaxColumns = TextVP["Width"])[0]
        
    # ask start
    RC.ShowCursor()
    PlayerEntersGame = Util.GetUserInput(
        Var.MessagesData["Challenge3"]["AskStartChallenge"],
        ValueType = "bool",
        DefaultValue = False,
        RichConsoleParameters = [TextVP["Y"] + LineOffset, TextVP["X"], TextVP["Width"]])
    RC.ShowCursor(False)

    if not PlayerEntersGame:
        # clean text area
        RC.ClearConsole(
            TextVP["Y"], TextVP["X"], 
            TextVP["Width"], TextVP["Height"])
        # exit challenge
        return

    # print second start message
    LineOffset += RC.Print(Var.MessagesData["Challenge3"]["Start2"] + "\n\n",          
        TextVP["Y"] + LineOffset, TextVP["X"],
        JustifyText = RC.Justify.Center, 
        MaxColumns = TextVP["Width"])[0]
    # wait
    time.sleep(Var.CurrentChallengeData["DelayAfterBadAnswer"])

    # clean text area
    RC.ClearConsole(
        TextVP["Y"], TextVP["X"], 
        TextVP["Width"], TextVP["Height"])
    LineOffset = 0
    
    # define player list
    RemainingPlayers = sorted(list(Var.CharactersData), key = lambda k: k['OrderInChallenge3']) 

    # put characters in place
    PlaceCharacters(RemainingPlayers, True)

    # define first player
    CurrentPlayerNumber = random.randint(0, len(RemainingPlayers) - 1)

    # game loop
    MainPlayerStillInGame = True
    while len(RemainingPlayers) > 1 and MainPlayerStillInGame:
        CurrentNumber = 1
        GoodAnswer = True
        while GoodAnswer:
            Answer = (
                "[Y;]FizzBuzz[;]" if CurrentNumber % 15 == 0
                else "[G;]Fizz[;]" if CurrentNumber % 3 == 0
                else "[C;]Buzz[;]" if CurrentNumber % 5 == 0
                else str(CurrentNumber))

            # define current player
            CurrentPlayer = RemainingPlayers[CurrentPlayerNumber]
            AnswerPercent = random.randint(1, Var.CurrentChallengeData["MaxChanceOfFailureForNumber"])
            if CurrentNumber % 3 == 0 or CurrentNumber % 5 == 0:
                AnswerPercent = random.randint(1, Var.CurrentChallengeData["MaxChanceOfFailureForFizzBuzz"])
            AnswerMessage = ""
            # AnswerMessage = f"{AnswerPercent}/{CurrentPlayer['Challenge3Chance']} → "

            if CurrentPlayer["Challenge3Chance"] >= AnswerPercent:
                # good answer
                AnswerMessage += (
                    Var.MessagesData["Challenge3"]["PlayerAnswer"]
                        .replace("{Character}", 
                            CurrentPlayer["Style"] + CurrentPlayer["Name"] + "[;]")
                        .replace("{Answer}",
                            Answer))
                # show answer
                ManageChallengeHistory(AnswerMessage, Answers, TextVP)
                # switch on player
                HighlightPlayer(CurrentPlayer)
                # wait
                time.sleep(Var.CurrentChallengeData["DelayBetweenAnswers"])
                # switch off current player
                HighlightPlayer(CurrentPlayer)
                # go to next player
                CurrentPlayerNumber = (
                    CurrentPlayerNumber + 1
                    if CurrentPlayerNumber + 1 < len(RemainingPlayers) 
                    else 0)

            else:
                # bad answer
                GoodAnswer = False
                # create a bad answer
                Answer = (
                    str(CurrentNumber) 
                    if CurrentNumber % 3 == 0 or CurrentNumber % 5 == 0
                    else ["Fizz", "Buzz", "FizzBuzz"][random.randint(0, 2)])

                if CurrentPlayer["Category"] == "Player":
                    # challenge lost
                    MainPlayerStillInGame = False
                    AnswerMessage += (
                        "\n" + Var.MessagesData["Challenge3"]["Failure"]
                            .replace("{Character}", 
                                CurrentPlayer["Style"] + CurrentPlayer["Name"] + "[;]")
                            .replace("{Answer}",
                                Answer))
                    # show answer
                    ManageChallengeHistory(AnswerMessage, Answers, TextVP)
                    # switch on player
                    HighlightPlayer(CurrentPlayer)
                    # wait
                    time.sleep(Var.CurrentChallengeData["DelayAfterBadAnswer"])
                    # switch off current player
                    HighlightPlayer(CurrentPlayer, True)

                else:
                    # monkey loose
                    AnswerMessage += (
                        Var.MessagesData["Challenge3"]["MonkeyWrong"]
                            .replace("{Character}", 
                                CurrentPlayer["Style"] + CurrentPlayer["Name"] + "[;]")
                            .replace("{Answer}",
                                Answer))
                    # show answer
                    ManageChallengeHistory(AnswerMessage, Answers, TextVP)
                    # switch on player
                    HighlightPlayer(CurrentPlayer)
                    # wait
                    time.sleep(Var.CurrentChallengeData["DelayAfterBadAnswer"])
                    # switch off current player
                    HighlightPlayer(CurrentPlayer, True)
                    # remove player from game
                    RemainingPlayers.remove(CurrentPlayer)
                    if CurrentPlayerNumber >= len(RemainingPlayers):
                        CurrentPlayerNumber = 0
                    # clean text area
                    RC.ClearConsole(
                        TextVP["Y"] + TextVP["Height"] - 1, TextVP["X"], 
                        TextVP["Width"], 1)
        
            # next number
            CurrentNumber += 1

    # clean text area
    RC.ClearConsole(
        TextVP["Y"], TextVP["X"], 
        TextVP["Width"], TextVP["Height"])

    if MainPlayerStillInGame:
        # Challenge won
        # show message
        LineOffset += RC.Print(Var.MessagesData["Challenge3"]["Success"],          
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = TextVP["Width"])[0]
        # change chief talk
        Var.MessagesData["El Maestro"]["Talk"] = Var.MessagesData["Challenge3"]["ChiefAfterChallengeWon"]
        # free key
        Var.ObjectsData["GoldKey"]["Behaviors"]["Pickable"] = True
        # close challenge
        Var.Player["ChallengesWon"]["3"] = True

    # put characters back at their original place
    PlaceCharacters(Var.CharactersData, False)



def PlaceCharacters(
    RemainingPlayers,
    ChallengePosition = True):
    """
        Place remaining players at position (Challenge3 or standard)
        Also draw chance for this game if ChallengePosition
    """

    for Player in RemainingPlayers:
        # get character actual position
        PreviousPosition = (Player["Position"]["Y"], Player["Position"]["X"])
        # place character at challenge start position
        Player["Position"]["Y"] = Player["Challenge3Position"]["Y"]
        Player["Position"]["X"] = Player["Challenge3Position"]["X"]
        # refresh map
        Game.ShowMap(PreviousPosition[0], PreviousPosition[1])
        Game.ShowMap(Player["Position"]["Y"], Player["Position"]["X"])
        
        # draw player chance for this game (or reset)
        if Player["Category"] == "Monkey":
            Player["Challenge3Chance"] = (
                random.randint(
                    Player["ChanceMin"], Player["ChanceMax"])
                if ChallengePosition
                else None)
            # stop event for (chief) monkey if challenge won
            if Var.Player["ChallengesWon"]["3"]:
                Player["Event"] = None


            
def HighlightPlayer(
    CurrentPlayer,
    Eliminate = False):
    """
        Switch on/off current player
    """
    
    # switch on/off current player
    if Eliminate:
        CurrentPlayer["Style"] = Var.CurrentChallengeData["EliminatedStyle"]
    else:
        CurrentPlayer["Style"] = (
            CurrentPlayer["Style"].replace("]", ";SI]") 
            if len(CurrentPlayer["Style"]) <= 5
            else CurrentPlayer["Style"].replace(";SI]", "]"))

    # refresh map
    Game.ShowMap(CurrentPlayer["Position"]["Y"], CurrentPlayer["Position"]["X"])

    # give player original style if eliminated
    if Eliminate:
        CurrentPlayer["Style"] = CurrentPlayer["DefaultStyle"]



def ManageChallengeHistory(
    Answer,
    Answers,
    TextVP):
    """
        Add new answer to history and show it
    """

    # add to challenge history
    Util.ManageMessageHistory(Answer, Answers)

    # show challenge history
    for Index, Message in enumerate(Answers[-(TextVP["Height"] - 1):]):
        RC.Print(f"{Message}",          
            TextVP["Y"] + Index, TextVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = TextVP["Width"])
