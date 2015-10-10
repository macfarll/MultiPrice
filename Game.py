########################################################################
# A text-base simulation of a popular card game called Hanabi. In the  #
#  current version, only two players are allowed, and the hint system  #
#  is very unsightly. Next version will update the hint function to be #
#  much more compact and implemented more dynamicly like the play      #
#  function.            -by Logan MacFarland. October 9th, 2015        #
########################################################################

import random
import sys

HintCounter=int(8)
ErrorCounter=int(0)
RemainingTurns=int(3)
HintText=" "
#function for drawing cards from deck to an arbitrary player's hand
def Draw(Source):
    if len(Deck) == 0:
        print "No new cards to Draw!"
    elif len(Deck) == 1:
        print "You drew the last card, each player gets one more turn!"
#        DrawnCard = Deck[0]
        Source.append(Deck[0])
        Deck.remove(Deck[0])
        global RemainingTurns
        RemainingTurns=int(2)
    else:
        DrawnCard = random.choice(Deck)
        Source.append(DrawnCard)
        Deck.remove(DrawnCard)
#function for displaying hand of player
def Show(Hand):
    for i in Hand:
        print str(i.color) + " " + str(i.tier)
    print "\n"

#Create object class for each 'card'
class Card(object):
    def __init__(self, tier, color):
        self.tier = tier
        self.color = color
#Create a list of numbers to make for each color
Tiers = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
#Create objects for each card that will be represented in the deck
RedCards = [Card(Tier, 'Red') for Tier in Tiers]
BlueCards = [Card(Tier, 'Blue') for Tier in Tiers]
GreenCards = [Card(Tier, 'Green') for Tier in Tiers]
YellowCards = [Card(Tier, 'Yellow') for Tier in Tiers]
WhiteCards = [Card(Tier, 'White') for Tier in Tiers]
#Merge all the lists together to create the starting deck
Deck = RedCards + BlueCards + GreenCards + YellowCards + WhiteCards
#create hands and discard pile
PlayerOne = []
PlayerTwo = []
DiscardPile = []
#fill hands with random cards from deck
while len(PlayerOne) < 5:
    Draw(PlayerOne)
while len(PlayerTwo) < 5:
    Draw(PlayerTwo)
#create empty stacks for all of the cards to be played into
RedStack = int(0)
BlueStack = int(0)
GreenStack = int(0)
YellowStack = int(0)
WhiteStack = int(0)

def Progress():
    print "Red Stack Shows:" + str(RedStack)
    print "Blue Stack Shows:" + str(BlueStack)
    print "Green Stack Shows:" + str(GreenStack)
    print "Yellow Stack Shows:" + str(YellowStack)
    print "White Stack Shows:" + str(WhiteStack)

#request what type of move the player will make, does not account for if a player is unable to hint or discard
def PromptMove(prompt):
    decision = 'empty'
    while decision == 'empty':
	ValidMove = ['Play', 'play']
        if HintCounter < 8:
            ValidMove.append('Discard')
            ValidMove.append('discard')
        if HintCounter > 0:
            ValidMove.append('Hint')
            ValidMove.append('hint')
        move = raw_input(prompt)
        if  move in ValidMove:
            decision = move
            return decision
        else:
            print "\nPlease type an appropriate move: 'Hint', 'Play', or 'Discard'\n\nKeep in mind you can't hint if none are available,\nand you can't discard if you have 8 hints.\n"
def ColorHint(prompt, PlayerNumber):
#Count colors of cards in the hand being hinted
    global HintText
    RedCount = int(0)
    BlueCount = int(0)
    GreenCount = int(0)
    YellowCount = int(0)
    WhiteCount = int(0)
    for i in PlayerNumber:
        if i.color == 'Red':
             RedCount +=1
        elif i.color == 'Blue':
             BlueCount +=1
        elif i.color == 'Green':
             GreenCount +=1
        elif i.color == 'Yellow':
             YellowCount +=1
        elif i.color == 'White':
             WhiteCount +=1
#create list of valid color hints
    ValidMove = []
    if RedCount > 0:
         ValidMove.append('Red')
         ValidMove.append('red')
    if BlueCount > 0:
         ValidMove.append('Blue')
         ValidMove.append('blue')
    if GreenCount > 0:
         ValidMove.append('Green')
         ValidMove.append('green')
    if YellowCount > 0:
         ValidMove.append('Yellow')
         ValidMove.append('yellow')
    if WhiteCount > 0:
         ValidMove.append('White')
         ValidMove.append('white')
    ColorDecision = 'empty'
    while ColorDecision == 'empty':
        move = raw_input(prompt)
#if hint color is valid, iterate through target hand and hint color for each card to the other player.
        if move in ValidMove:
            if move in ['Red', 'red']:
                ColorDecision = move
                for i in PlayerNumber:
                    if i.color == 'Red':
                        HintText = "You have been hinted that your card at position " + str(int(PlayerNumber.index(i))+1) + " is Red."
            elif move in ['Blue', 'blue']:
                ColorDecision = move
                for i in PlayerNumber:
                    if i.color == 'Blue':
                        HintText = "You have been hinted that your card at position " + str(int(PlayerNumber.index(i))+1) + " is Blue."
            elif move in ['Green', 'green']:
                ColorDecision = move
                for i in PlayerNumber:
                    if i.color == 'Green':
                        HintText = "You have been hinted that your card at position " + str(int(PlayerNumber.index(i))+1) + " is Green."
            elif move in ['Yellow', 'yellow']:
                ColorDecision = move
                for i in PlayerNumber:
                    if i.color == 'Yellow':
                        HintText = "You have been hinted that your card at position " + str(int(PlayerNumber.index(i))+1) + " is Yellow."
            elif move in ['White', 'white']:
                ColorDecision = move
                for i in PlayerNumber:
                    if i.color == 'White':
                        HintText = "You have been hinted that your card at position " + str(int(PlayerNumber.index(i))+1) + " is White."
#if an invalid hint is answered, returns an error
        else:
            print "\nPlease choose an appropriate color: 'Red', 'Blue', 'Green', 'Yellow', or 'White'\nAlso, you must choose a color represented in the other player's hand.\n"

def NumberHint(prompt, PlayerNumber):
#Count numbers of cards in the hand being hinted
    global HintText
    OneCount = int(0)
    TwoCount = int(0)
    ThreeCount = int(0)
    FourCount = int(0)
    FiveCount = int(0)
    for i in PlayerNumber:
        if i.tier == 1:
             OneCount +=1
        elif i.tier == 2:
             TwoCount +=1
        elif i.tier == 3:
             ThreeCount +=1
        elif i.tier == 4:
             FourCount +=1
        elif i.tier == 5:
             FiveCount +=1
#create list of valid number hints
    ValidMove = []
    if OneCount > 0:
         ValidMove.append(1)
    if TwoCount > 0:
         ValidMove.append(2)
    if ThreeCount > 0:
         ValidMove.append(3)
    if FourCount > 0:
         ValidMove.append(4)
    if FiveCount > 0:
         ValidMove.append(5)
    NumberDecision = 'empty'
    while NumberDecision == 'empty':
        move = int(raw_input(prompt))
#if hint number is valid, iterate through target hand and hint number for each card to the other player.
        if move in ValidMove:
            if move == 1:
                NumberDecision = move
                for i in PlayerNumber:
                    if i.tier == 1:
                        HintText = "You have been hinted that your card at position " + str(int(PlayerNumber.index(i))+1) + " is a 1."
            elif move == 2:
                NumberDecision = move
                for i in PlayerNumber:
                    if i.tier == 2:
                        HintText = "You have been hinted that your card at position " + str(int(PlayerNumber.index(i))+1) + " is a 2."
            elif move == 3:
                NumberDecision = move
                for i in PlayerNumber:
                    if i.tier == 3:
                        HintText = "You have been hinted that your card at position " + str(int(PlayerNumber.index(i))+1) + " is a 3."
            elif move == 4:
                NumberDecision = move
                for i in PlayerNumber:
                    if i.tier == 4:
                        HintText = "You have been hinted that your card at position " + str(int(PlayerNumber.index(i))+1) + " is a 4."
            elif move == 5:
                NumberDecision = move
                for i in PlayerNumber:
                    if i.tier == 5:
                        HintText = "You have been hinted that your card at position " + str(int(PlayerNumber.index(i))+1) + " is a 5."
#if an invalid hint is answered, returns an error
        else:
            print "\nPlease choose an appropriate number: '1', '2', '3', '4', '5'\nAlso, you must choose a number represented in the other player's hand.\n"
#checks if hint is either number or color, and passes command to appropriate function, also removes one available hint
def Hint(prompt):
    global HintCounter
    HintCounter -= 1
    HintDecision = 'empty'
    while HintDecision == 'empty':
        ValidMove = ['Color', 'color', 'Number', 'number']
        move = raw_input(prompt)
        if move in ValidMove:
            HintDecision = move
            return HintDecision
        else:
            print "Please type 'Color', or 'Number'"
def Discard(prompt, PlayerNumber):
    global HintCounter
    HintCounter += 1
    DiscardDecision = 'empty'
    while DiscardDecision == 'empty':
        move = int(raw_input(prompt))
        if move in range(1,len(PlayerNumber)+1):
            AdjustedMove = move-1
            DiscardedCard = PlayerNumber[AdjustedMove]
            DiscardPile.append(DiscardedCard)
            print "You discarded a " + str(DiscardedCard.color) + " " + str(DiscardedCard.tier)
            PlayerNumber.remove(DiscardedCard)
            Draw(PlayerNumber)
            DiscardDecision = AdjustedMove
        else:
            print "Please type '1', '2', '3', '4', or '5'"
def Play(prompt, PlayerNumber):
    PlayDecision = 'empty'
    while PlayDecision == 'empty':
        move = int(raw_input(prompt))
        if move in range(1,len(PlayerNumber)+1):
            AdjustedMove = move - 1
            PlayingCard = PlayerNumber[AdjustedMove]
            AppropriatePile = str(PlayingCard.color) + "Stack"
            if int(PlayingCard.tier) == (int(eval(AppropriatePile))+1):
                print "Card played correctly!"
                #creates two commands (as a string), that adds one to the value of the appropriate stack, and makes the stack global
                Command = str(AppropriatePile) + " += 1" 
                exec Command in globals()
            else:
                global ErrorCounter
                ErrorCounter += 1
                if ErrorCounter == 3:
                    print "You've made three errors!"
                    GameOver()
            DiscardPile.append(PlayerNumber[AdjustedMove])
            PlayerNumber.remove(PlayerNumber[AdjustedMove])
            Draw(PlayerNumber)
            print "\n"
            PlayDecision = "over"
        else:
            print "Please type '1', '2', '3', '4', or '5'"
def GameOver():
    print "The game is over, your score is:"
    FinalScore = RedStack + BlueStack + GreenStack + YellowStack + WhiteStack
    print FinalScore
    sys.exit()

#Player one's turn
def TurnP1():
    print "\n\n\n\n\n\n\n\n\n\n"
    raw_input("Press enter to start your turn, Player One.")
    global HintText
    print HintText
    HintText = "You have not been given a new hint."
    global RemainingTurns
    if RemainingTurns == 2:
        print "The other player drew the last card, this is your last turn!"
        RemainingTurns -= 1
    elif RemainingTurns == 1:
        print "This is your last turn!"
        RemainingTurns = 0
    print "\nPlayer Two's hand:"
    Show(PlayerTwo)
    Progress()
    print "\nDiscard pile:"
    Show(DiscardPile)
    print "You have " + str(HintCounter) + " hints left, and have made " + str(ErrorCounter) + " errors."
    decision = str(PromptMove("What would you like to do? You may 'Hint', 'Play', or 'Discard'.\n"))
    if decision in ['Hint', 'hint']:
#        print "Who would you like to give a hint to?"
        HintDecision = str(Hint("Would you like to hint them a color or a number?\n"))
        if HintDecision in ['Color', 'color']:
            ColorHint("What color would you like to tell the other player about?\n", PlayerTwo)
        elif HintDecision in ['Number', 'number']:
            NumberHint("What number would you like to tell the other player about?\n", PlayerTwo)
        else:
            print "Somehow I managed to accept an inappropriate response..."
    elif decision in ['Play', 'play']:
        Play("What card would you like to play?\n",PlayerOne)
    elif decision in ['Discard', 'discard']:
        Discard("What card would you like to discard?\n", PlayerOne)
    else:
        print "Somehow I managed to accept an inappropriate response..."     
    CurrentScore = RedStack + BlueStack + GreenStack + YellowStack + WhiteStack
    if CurrentScore == 25:
        print "You have completed every stack!"
        GameOver()
#    global RemainingTurns
    if RemainingTurns == 0:
        print "The game ended because you ran out of turns!"
        GameOver()
    raw_input("Press enter to end your turn, Player One.")
    TurnP2()

#Player two's turn
def TurnP2():
    print "\n\n\n\n\n\n\n\n\n\n"
    raw_input("Press enter to begin your turn, Player Two.")
    global HintText
    print HintText
    HintText = "You have not been given a new hint."
    global RemainingTurns
    if RemainingTurns == 2:
        print "The other player drew the last card, this is your last turn!"
        RemainingTurns -= 1
    elif RemainingTurns == 1:
        print "This is your last turn!"
        RemainingTurns = 0
    print "\nPlayer One's hand:"
    Show(PlayerOne)
    Progress()
    print "\nDiscard pile:"
    Show(DiscardPile)
    print "You have " + str(HintCounter) + " hints left, and have made " + str(ErrorCounter) + " errors."
    decision = str(PromptMove("What would you like to do? You may 'Hint', 'Play', or 'Discard'.\n"))
    if decision in ['Hint', 'hint']:
#        print "Who would you like to give a hint to?"
        HintDecision = str(Hint("Would you like to hint them a color or a number?\n"))
        if HintDecision in ['Color', 'color']:
            ColorHint("What color would you like to tell the other player about?\n", PlayerOne)
        elif HintDecision in ['Number', 'number']:
            NumberHint("What number would you like to tell the other player about?\n", PlayerOne)
        else:
            print "Somehow I managed to accept an inappropriate response..."
    elif decision in ['Play', 'play']:
        Play("What card would you like to play?\n",PlayerTwo)
    elif decision in ['Discard', 'discard']:
        Discard("What card would you like to discard?\n", PlayerTwo)
    else:
        print "Somehow I managed to accept an inappropriate response..."
    CurrentScore = RedStack + BlueStack + GreenStack + YellowStack + WhiteStack
    if CurrentScore == 25:
        print "You have completed every stack!"         
        GameOver()
#    global RemainingTurns
    if RemainingTurns == 0:
        print "The game ended because you ran out of turns!"
        GameOver()
    raw_input("Press enter to end your turn, Player Two.")
    TurnP1()
TurnP1()
