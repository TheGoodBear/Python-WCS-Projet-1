# coding: utf-8

# Imports modules
import time
import random

# Import application code
import ProgramFiles.Variables as Var
import ProgramFiles.Utilities.Utilities as Util
import ProgramFiles.Utilities.RichConsole as RC


# Functions
def Challenge1():
    """
        Manage challenge 1 (Mysterious number)
    """

    TextVP = Var.GameData["ViewPorts"]["Challenge"]["Text"]
    AskVP = Var.GameData["ViewPorts"]["Challenge"]["Ask"]

    RemainingTries = Var.CurrentChallengeData["MaxTries"]
    NumbersFound = 0
    ProposedNumber = None
    MinProposedNumber = 0
    MaxProposedNumber = 101
    MysteriousNumber = random.randint(
        Var.CurrentChallengeData["MinimumNumber"],
        Var.CurrentChallengeData["MaximumNumber"])
    FoundNumber = " ??? "

    while (RemainingTries > 0 
        and NumbersFound < Var.CurrentChallengeData["Rounds"]):

        # challenge dashboard
        RC.ClearConsole(
            TextVP["Y"], TextVP["X"], 
            TextVP["Width"], TextVP["Height"])
        LineOffset = 0

        # Message = (Var.MessagesData[CurrentMap]["Story1"]
        #     .replace("{Name}", 
        #         Var.Player["Style"] + Var.Player["Name"] + "[;]"))
        Message = f"Il te reste encore {RemainingTries} essais.\n\n"
        LineOffset += RC.Print(Message,          
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = TextVP["Width"])[0]
        Message = f"{MinProposedNumber}  <<<  [;;SI]{FoundNumber}[;]  <<<  {MaxProposedNumber}\n\n"
        LineOffset += RC.Print(Message,          
            TextVP["Y"] + LineOffset, TextVP["X"],
            JustifyText = RC.Justify.Center, 
            MaxColumns = TextVP["Width"])[0]
        
        # ask number
        RC.ShowCursor()
        ProposedNumber = Util.GetUserInput(
            Var.MessagesData["Challenge1"]["AskUser"],
            ValueType = "int",
            Minimum = Var.CurrentChallengeData["MinimumNumber"],
            Maximum = Var.CurrentChallengeData["MaximumNumber"],
            SpecificErrorMessage = (
                Var.MessagesData["Challenge1"]["Wrong"]
                .replace("{MinimumNumber}", str(Var.CurrentChallengeData["MinimumNumber"]))
                .replace("{MaximumNumber}", str(Var.CurrentChallengeData["MaximumNumber"]))),
            RichConsoleParameters = [TextVP["Y"] + LineOffset, TextVP["X"], TextVP["Width"]])
        RC.ShowCursor(False)
        RC.ClearConsole(
            TextVP["Y"] + LineOffset, TextVP["X"], 
            TextVP["Width"], 2)

        RemainingTries -= 1

        # check answer
        if ProposedNumber == MysteriousNumber:
            # good answer
            NumbersFound += 1
            CurrentStar = Var.CurrentChallengeData["Stars"]["Elements"][NumbersFound - 1]

            Message = (Var.MessagesData["Challenge1"]["Equal"]
                .replace("{Number}", str(MysteriousNumber))
                .replace("{Star}", CurrentStar["Style"] + CurrentStar["Image"] + "[;]"))
            LineOffset += RC.Print(Message,          
                TextVP["Y"] + LineOffset, TextVP["X"],
                JustifyText = RC.Justify.Left, 
                MaxColumns = TextVP["Width"])[0]

            # light star
            RC.Print(
                f"{Var.CurrentChallengeData['Stars']['Style']}{Var.CurrentChallengeData['Stars']['Image']}[;]",
                Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["Y"] + CurrentStar["Y"],
                Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["X"] + CurrentStar["X"],
                JumpLineAfter = False)

            if NumbersFound == Var.CurrentChallengeData["Rounds"]:
                # challenge won
                RC.ClearConsole(
                    TextVP["Y"], TextVP["X"], 
                    TextVP["Width"], TextVP["Height"])
                LineOffset = 0
                # show message
                Message = (Var.MessagesData["Challenge1"]["Success"]
                    .replace("{Name}", 
                        Var.Player["Style"] + Var.Player["Name"] + "[;]"))
                LineOffset += RC.Print(Message,          
                    TextVP["Y"] + LineOffset, TextVP["X"],
                    JustifyText = RC.Justify.Left, 
                    MaxColumns = TextVP["Width"])[0]
                # unlight eyes
                for Element in Var.CurrentChallengeData["Eyes"]["Elements"]:
                    RC.Print(
                        f"[B;B]{Var.CurrentChallengeData['Eyes']['Image']}[;]",
                        Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["Y"] + Element["Y"],
                        Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["X"] + Element["X"],
                        JumpLineAfter = False)
                # free key
                Var.ObjectsData["BronzeKey"]["Behaviors"]["Pickable"] = True
                # close challenge
                Var.MapElementsData["1"]["Behaviors"]["Event"] = None

            else:
                # draw next number
                MysteriousNumber = random.randint(
                    Var.CurrentChallengeData["MinimumNumber"],
                    Var.CurrentChallengeData["MaximumNumber"])

        else:
            # bad answer

            MinProposedNumber = min(MinProposedNumber, int(ProposedNumber))
            MaxProposedNumber = max(MaxProposedNumber, int(ProposedNumber))

            if ProposedNumber < MysteriousNumber:
                # too low
                Message = Var.MessagesData["Challenge1"]["Higher"]
                LineOffset += RC.Print(Message,          
                    TextVP["Y"] + LineOffset, TextVP["X"],
                    JustifyText = RC.Justify.Left, 
                    MaxColumns = TextVP["Width"])[0]
            else:
                # too high
                Message = Var.MessagesData["Challenge1"]["Lower"]
                LineOffset += RC.Print(Message,          
                    TextVP["Y"] + LineOffset, TextVP["X"],
                    JustifyText = RC.Justify.Left, 
                    MaxColumns = TextVP["Width"])[0]

            if RemainingTries == 0:
                # challenge lost
                # show message
                Message = (Var.MessagesData["Challenge1"]["Failure"]
                    .replace("{Name}", 
                        Var.Player["Style"] + Var.Player["Name"] + "[;]"))
                LineOffset += RC.Print(Message,          
                    TextVP["Y"] + LineOffset, TextVP["X"],
                    JustifyText = RC.Justify.Left, 
                    MaxColumns = TextVP["Width"])[0]
                # unlight eyes
                for Element in Var.CurrentChallengeData["Eyes"]["Elements"]:
                    RC.Print(
                        f"[B;B]{Var.CurrentChallengeData['Eyes']['Image']}[;]",
                        Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["Y"] + Element["Y"],
                        Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["X"] + Element["X"],
                        JumpLineAfter = False)

            
                





