# coding: utf-8

# Imports modules
import time
import random

# Import application code
import ProgramFiles.Variables as Var
import ProgramFiles.Utilities.Utilities as Util
import ProgramFiles.Utilities.RichConsole as RC


# Functions
def StartChallenge():
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

    # clean text area
    RC.ClearConsole(
        TextVP["Y"], TextVP["X"], 
        TextVP["Width"], TextVP["Height"])
    LineOffset = 0

    # print start message
    LineOffset += RC.Print(Var.MessagesData["Challenge1"]["Start"] + "\n\n",          
        TextVP["Y"] + LineOffset, TextVP["X"],
        JustifyText = RC.Justify.Center, 
        MaxColumns = TextVP["Width"])[0]

    Message = ""
    while (RemainingTries > 0 
        and NumbersFound < Var.CurrentChallengeData["Rounds"]):

        Message += f"Il te reste encore {RemainingTries} essais.\n\n"
        Message += f"{MinProposedNumber}  <<<  [;;SI]{FoundNumber}[;]  <<<  {MaxProposedNumber}\n\n"
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

        # clear challenge text
        RC.ClearConsole(
            TextVP["Y"], TextVP["X"], 
            TextVP["Width"], TextVP["Height"])
        LineOffset = 0
        Message = ""

        RemainingTries -= 1

        # check answer
        if ProposedNumber == MysteriousNumber:
            # good answer
            NumbersFound += 1

            # switch on star
            SphinxStars(NumbersFound - 1)

            Message += (
                Var.MessagesData["Challenge1"]["Equal"]
                    .replace("{Number}", str(MysteriousNumber))
                    .replace("{Star}", Var.CurrentChallengeData["Stars"]["StyleOn"] + Var.CurrentChallengeData["Stars"]["Image"] 
                + "[;]")
                + "\n\n")

            if NumbersFound == Var.CurrentChallengeData["Rounds"]:
                # challenge won
                RC.ClearConsole(
                    TextVP["Y"], TextVP["X"], 
                    TextVP["Width"], TextVP["Height"])
                LineOffset = 0
                # show message
                Message += (Var.MessagesData["Challenge1"]["Success"]
                    .replace("{Name}", 
                        Var.Player["Style"] + Var.Player["Name"] + "[;]"))
                LineOffset += RC.Print(Message,          
                    TextVP["Y"] + LineOffset, TextVP["X"],
                    JustifyText = RC.Justify.Center, 
                    MaxColumns = TextVP["Width"])[0]

                # switch off eyes
                SphinxEyes(False)
                # free key
                Var.ObjectsData["BronzeKey"]["Behaviors"]["Pickable"] = True
                # close challenge
                Var.MapElementsData["4"]["Behaviors"]["Event"] = None
                Var.MessagesData["4"]["CantMoveOn"] = Var.MessagesData["1"]["CantMoveOn"]
                Var.CurrentChallengeData["Won"] = True

            else:
                # start new round
                ProposedNumber = None
                MinProposedNumber = 0
                MaxProposedNumber = 101
                MysteriousNumber = random.randint(
                    Var.CurrentChallengeData["MinimumNumber"],
                    Var.CurrentChallengeData["MaximumNumber"])
                FoundNumber = " ??? "

        else:
            # bad answer

            if ProposedNumber < MysteriousNumber:
                # too low
                MinProposedNumber = max(MinProposedNumber, int(ProposedNumber))
                Message += Var.MessagesData["Challenge1"]["Higher"] + "\n\n"
            else:
                # too high
                MaxProposedNumber = min(MaxProposedNumber, int(ProposedNumber))
                Message += Var.MessagesData["Challenge1"]["Lower"] + "\n\n"

            if RemainingTries == 0:
                # challenge lost
                # show message
                Message += (Var.MessagesData["Challenge1"]["Failure"]
                    .replace("{Name}", 
                        Var.Player["Style"] + Var.Player["Name"] + "[;]"))
                LineOffset += RC.Print(Message,          
                    TextVP["Y"] + LineOffset, TextVP["X"],
                    JustifyText = RC.Justify.Center, 
                    MaxColumns = TextVP["Width"])[0]
                
                # switch off eyes
                SphinxEyes(False)
                # switch off stars
                SphinxStars()


            

def SphinxEyes(
    SwitchOn = True):
    """
        Switch on/off sphinx eyes
    """
    
    Style = Var.CurrentChallengeData["Eyes"]["StyleOn"] if SwitchOn else Var.CurrentChallengeData["Eyes"]["StyleOff"]

    for Element in Var.CurrentChallengeData["Eyes"]["Elements"]:
        RC.Print(
            f"{Style}{Var.CurrentChallengeData['Eyes']['Image']}[;]",
            Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["Y"] + Element["Y"],
            Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["X"] + Element["X"],
            JumpLineAfter = False)


def SphinxStars(
    StarNumber = None):
    """
        Switch on specified star or switch off all stars
    """

    MinStar = StarNumber if StarNumber is not None else 0
    MaxStar = StarNumber if StarNumber is not None else len(Var.CurrentChallengeData["Stars"]["Elements"]) - 1
    Style = Var.CurrentChallengeData["Stars"]["StyleOn"] if StarNumber is not None else Var.CurrentChallengeData["Stars"]["StyleOff"]

    for ElementNumber in range(MinStar, MaxStar + 1):
        CurrentStar = Var.CurrentChallengeData["Stars"]["Elements"][ElementNumber]

        RC.Print(
            f"{Style}{Var.CurrentChallengeData['Stars']['Image']}[;]",
            Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["Y"] + CurrentStar["Y"],
            Var.GameData["ViewPorts"][Var.MapViewPortName]["Map"]["X"] + CurrentStar["X"],
            JumpLineAfter = False)
