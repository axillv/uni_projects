# 1-D NIM Games
import os
import random

############################### FG COLOR DEFINITIONS ###############################
class bcolors:
    # pure colors...
    GREY      = '\033[90m'
    RED       = '\033[91m'
    GREEN     = '\033[92m'
    YELLOW    = '\033[93m'
    BLUE      = '\033[94m'
    BLUE      = '\033[94m'
    PURPLE    = '\033[95m'
    CYAN      = '\033[96m'
    # color styles...
    HEADER      = '\033[95m'
    QUESTION    = '\033[93m\033[3m'
    MSG         = '\033[94m'
    COMMENT     = '\033[96m\033[3m'
    WARNING     = '\033[93m'
    ERROR       = '\033[91m'
    ENDC        = '\033[0m'    # RECOVERS DEFAULT TEXT COLOR
    BOLD        = '\033[1m'
    ITALICS     = '\033[3m'
    UNDERLINE   = '\033[4m'

    def disable(self):
        self.HEADER      = '\033[95m'
        self.QUESTION    = '\033[93m\033[3m'
        self.MSG         = '\033[94m'
        self.COMMENT     = '\033[96m\033[3m'
        self.WARNING     = '\033[93m'
        self.ERROR       = '\033[91m'
        self.ENDC        = '\033[0m'    # RECOVERS DEFAULT TEXT COLOR
        self.BOLD        = '\033[1m'
        self.ITALICS     = '\033[3m'
        self.UNDERLINE   = '\033[4m'

############# CONSTRUCTION OF VARIOUS TYPES OF SEPARATION LINES #############
EQLINE          = '\t'
MINUSLINE       = '\t'
PLUSLINE        = '\t'
SPACESLINE      = '\t'
CONSECEQUALS    = ''
CONSECMINUS     = ''
CONSECPLUS      = ''
CONSECSPACES    = ''

for i in range(5):
        CONSECEQUALS    = CONSECEQUALS  + '='
        CONSECMINUS     = CONSECMINUS   + '-'
        CONSECPLUS      = CONSECPLUS    + '+'
        if i%4 == 0:
               CONSECSPACES    = CONSECSPACES  + ' '

for i in range(12):
        EQLINE          = EQLINE        + CONSECEQUALS
        MINUSLINE       = MINUSLINE     + CONSECMINUS
        PLUSLINE        = PLUSLINE      + CONSECPLUS
        SPACESLINE      = SPACESLINE    + CONSECSPACES

def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')


def drawNimPalette(N,ListOfPileCapacities):

        if not(isinstance(ListOfPileCapacities,list )) or not(isinstance(N,int)) or N < 0:
                print(bcolors.ERROR + "ERROR: The number of piles has to be a positive integer, and the pile capacities must be given as a list of non-negative integers. Try again...")
                return(-1)

        if N != len(ListOfPileCapacities):
                print(bcolors.ERROR + "ERROR: The number of piles does not match the list of pile capacities. Try again...")
                return(-1)
        
        Cmax = 0

        for pile in range(len(ListOfPileCapacities)):
                if not(isinstance(ListOfPileCapacities[pile],int)) or ListOfPileCapacities[pile] < 0:
                        print(bcolors.ERROR + "ERROR: The capacity of pile ",pile," must be a non-negative integer. Try again...")
                        return(-1)
                Cmax = max(Cmax,ListOfPileCapacities[pile])


        print(bcolors.MSG + EQLINE)
        print("\tCURRENT POSITION: ",ListOfPileCapacities)
        for pile in range(N):
                #PRINTING ROW FOR PILE i...
                if pile == 0:
                        print(EQLINE)
                else:
                        print(MINUSLINE)

                printRowString = '\t' + str(pile) + ': ' +'['

                for j in range(ListOfPileCapacities[pile]):
                        # PRINTING FILLED CELL (i,j)...
                        printRowString += " ▓▓ |"
                for j in range(ListOfPileCapacities[pile],Cmax):
                        # PRINTING EMPTY CELL (i,j)...
                        printRowString += "    |"

                printRowString = printRowString[:len(printRowString)-1] + ']'

                print (printRowString)
        print ( EQLINE + bcolors.ENDC)
        return(0)

def inputPlayerLetter():
        # The player chooses which label (letter) will fill the cells
        letter = ''
        while not(letter == 'G' or letter == 'R'):
                print ( bcolors.QUESTION + '[Q1] What letter do you choose to play? [ G(reen) | R(ed) ]' + bcolors.ENDC )
                letter = input().upper()
                # The first letter corresponds to the HUMAN and the second element corresponds to the COMPUTER
                if letter == 'G':
                        return ['G','R']
                else:
                        if letter == 'R':
                                return ['R','G']
                        else:
                                print (bcolors.ERROR + 'ERROR1: You provided an invalid choice. Please try again...' + bcolors.ENDC)

def whoGoesFirst():
        if random.randint(0,1) == 0:
                return 'computer'
        else:
                return 'player'

def howComputerPlays():
        
        while True:
                print ( bcolors.QUESTION + '[Q5] How will the computer play? [ R (randomly) | F (first Free) | C (copycat)]' + bcolors.ENDC )
                strategyLetter = input().upper()
        
                if strategyLetter == 'R':
                        return 'random'
                else: 
                        if strategyLetter == 'F':
                                return 'first free'
                        else:
                                if strategyLetter == 'C':
                                        return 'copycat'
                                else:
                                        print( bcolors.ERROR + 'ERROR 3: Incomprehensible strategy was provided. Try again...' + bcolors.ENDC )

def startNewGame():
        # Function for starting a new game
        print(bcolors.QUESTION + '[Q0] Would you like to start a new game? (yes or no)' + bcolors.ENDC)
        return input().lower().startswith('y')

def chooseNIMVariant():
        # Function for starting a new game
        chooseNIMVariantFlag = False
        while not chooseNIMVariantFlag:
                print(bcolors.QUESTION + '[Q1] Which variant of NIM would you like to play? [k (for NIM-k): k IN {1,2,3,4}]' + bcolors.ENDC)
                variantChoice = input().lower()
                if variantChoice == '1':
                        return"NIM-1"
                if variantChoice == '2':
                        return"NIM-2"
                if variantChoice == '3':
                        return"NIM-3"
                if variantChoice == '4':
                        return"NIM-4"
                
                print(bcolors.ERROR + '[ERROR] Your choice for a NIM-variant is incomprehensible. Try again by giving an integer from {1,2,3,4}...' + bcolors.ENDC)

######### MAIN PROGRAM BEGINS #########
screen_clear()

print(bcolors.HEADER + """
---------------------------------------------------------------------
                     CEID NE509 (2023-24)/ LAB-1  
                     Instructor: Spyros Kontogiannis
---------------------------------------------------------------------
STUDENT NAME:           Achilleas Villiotis
STUDENT AM:             1084567
---------------------------------------------------------------------
""" + bcolors.ENDC)

input("Press ENTER to continue...")
screen_clear()

print(bcolors.HEADER + """
---------------------------------------------------------------------
                     1-Dimensional NIM Games: RULES (I)
---------------------------------------------------------------------
    1.      A human PLAYER plays against the COMPUTER.
    2.      The starting position is a collection of N >= 1 PILES.
    3.      Each pile i contains a positive number C(i) of matches.
""" + bcolors.ENDC ) 

input("Press ENTER to continue...")
screen_clear()

print(bcolors.HEADER + """
---------------------------------------------------------------------
                     1-Dimensional NIM Games: RULES (II) 
---------------------------------------------------------------------
    4.      A NIM game is represented by an NxM matrix, where each 
            row i corresponds to a pile, and has its first C(i) cells
            filled with a special string '▓▓'. The remaining cells 
            of the row remain empty.E.g. for N=4, the starting position 
            [1,4,5,8] will be represented as follows:
""" + bcolors.ENDC)

drawNimPalette( N=4, ListOfPileCapacities=[1,4,5,8] )

input("Press ENTER to continue...")
screen_clear()

print(bcolors.HEADER + """
---------------------------------------------------------------------
                     1-Dimensional NIM Games: RULES (III) 
---------------------------------------------------------------------
    5.      The first step is for the player to choose a NIM VARIANT
            to play. The following options must be provided:
      
                1. NIM-1 VARIANT: The players play interchangeably
                   and remove matches (at least one, no more than the 
                   available) from a SINGLE pile of their choice.
                   The player who draws the last match WINS.

                2. NIM-2 VARIANT: The players play interchangeably
                   and remove matches (at least one, no more than the 
                   available) from a SINGLE pile of their choice.
                   The player who draws the last match LOSES.

                3. NIM-3 VARIANT: There is only ONE pile. The players 
                   play interchangeably and remove AT LEAST ONE and AT 
                   MOST K matches from the pile, for a given value K.
                   The player who draws the last match LOSES.

                4. NIM-4 VARIANT: There are TWO piles. The players 
                   play interchangeably and remove K matches from one 
                   of the two piles, or K matches from each pile, 
                   for some K of their choice, provided that there 
                   exist enough matches in the chosen pile(s). 
                   The player who draws the last match LOSES.
---------------------------------------------------------------------
""" + bcolors.ENDC)

playNewGameFlag = True

while playNewGameFlag:

        if not startNewGame():
                break

        nimVariantChoice = chooseNIMVariant()
        
        turn = whoGoesFirst()

        print( bcolors.MSG + PLUSLINE + bcolors.ENDC )
        print( bcolors.MSG + '\tA new instance of',nimVariantChoice,'is about to start.' + bcolors.ENDC )
        print( bcolors.MSG + '\tThe first move will be done by the ' + bcolors.UNDERLINE + turn + '.' + bcolors.ENDC )
        print( bcolors.MSG + MINUSLINE + bcolors.ENDC )
        print( bcolors.MSG + '\tExecute your own code here for the workflow of this game:' + bcolors.ENDC )
        print( bcolors.MSG + PLUSLINE + bcolors.ENDC )
        
######### MAIN PROGRAM ENDS #########
