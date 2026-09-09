from aux import *

from functools import reduce
import os
import random

def screenClear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')

def startNewGame():
    # Function for starting a new game
    print(bcolors.QUESTION + '\t[Q0] Would you like to start a new game? (yes or no)' + bcolors.ENDC)
    ans = input('\t' + bcolors.GREY + bcolors.BOLD).lower().startswith('y')
    print(bcolors.ENDC, end='') # clear styling
    return ans

def drawNimPalette(N,ListOfPileCapacities):

    if not(isinstance(ListOfPileCapacities,list )) or not(isinstance(N,int)) or N < 0:
            print(bcolors.ERROR + "\tERROR: The number of piles has to be a positive integer, and the pile capacities must be given as a list of non-negative integers. Try again...")
            return(-1)
    if N != len(ListOfPileCapacities):
            print(bcolors.ERROR + "\tERROR: The number of piles does not match the list of pile capacities. Try again...")
            return(-1)
    
    Cmax = 0
    for pile in range(len(ListOfPileCapacities)):
            if not(isinstance(ListOfPileCapacities[pile],int)) or ListOfPileCapacities[pile] < 0:
                    print(bcolors.ERROR + bcolors.BOLD +  "\tERROR: The capacity of pile " + pile + " must be a non-negative integer. Try again...")
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


def showRules():
    screenClear()

    print(bcolors.HEADER + """
    ---------------------------------------------------------------------
                        CEID NE509 (2023-24)/ LAB-1  
                        Instructor: Spyros Kontogiannis
    ---------------------------------------------------------------------
    STUDENT NAME:           Achilleas Villiotis
    STUDENT AM:             1084567
    ---------------------------------------------------------------------
    """ + bcolors.ENDC)

    input(bcolors.GREY + "\tPress ENTER to continue...")
    print(bcolors.ENDC, end='') # clear styling
    screenClear()

    print(bcolors.HEADER + """
    ---------------------------------------------------------------------
                        1-Dimensional NIM Games: RULES (I)
    ---------------------------------------------------------------------
        1.      A human PLAYER plays against the COMPUTER.
        2.      The starting position is a collection of N >= 1 PILES.
        3.      Each pile i contains a positive number C(i) of matches.
    """ + bcolors.ENDC ) 

    input(bcolors.GREY + "\tPress ENTER to continue...")
    print(bcolors.ENDC, end='') # clear styling
    screenClear()

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

    input(bcolors.GREY + "\tPress ENTER to continue...")
    print(bcolors.ENDC, end='') # clear styling
    screenClear()

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
                    The player who draws the last match WINS.

                    4. NIM-4 VARIANT: There are TWO piles. The players 
                    play interchangeably and remove K matches from one 
                    of the two piles, or K matches from each pile, 
                    for some K of their choice, provided that there 
                    exist enough matches in the chosen pile(s). 
                    The player who draws the last match WINS.
    ---------------------------------------------------------------------
    """ + bcolors.ENDC)
    input(bcolors.GREY + "\tPress ENTER to continue...")
    print(bcolors.ENDC, end='') # clear styling


def chooseNIMVariant():
    # Function for starting a new game
    chooseNIMVariantFlag = False
    while not chooseNIMVariantFlag:
        print(bcolors.QUESTION + '\t[Q1] Which variant of NIM would you like to play?\n\t[k (for NIM-k): k IN {1,2,3,4}]' + bcolors.ENDC)
        variantChoice = input('\t' + bcolors.GREY + bcolors.BOLD).lower()
        if variantChoice == '1':
                return"NIM-1"
        if variantChoice == '2':
                return"NIM-2"
        if variantChoice == '3':
                return"NIM-3"
        if variantChoice == '4':
                return"NIM-4"
        
        print(bcolors.ERROR + '\t[ERROR] Your choice for a NIM-variant is incomprehensible. Try again by giving an integer from {1,2,3,4}...' + bcolors.ENDC)

def whoGoesFirst():
    if random.randint(0,1) == 0:
        return 'computer'
    else:
        return 'player'
    
def nim1Initiate():
    print(bcolors.QUESTION + '\t[Q2] Enter the piles of the game, separated by commas (e.g. 3,4,5,6):' + bcolors.ENDC)
    while True:
        piles = input('\t' + bcolors.GREY + bcolors.BOLD).split(',')
        print(bcolors.ENDC, end='') # clear styling

        if len(piles) < 1:
            print(bcolors.ERROR + '\t[ERROR] You must provide at least one pile. Try again...' + bcolors.ENDC)
        if not all(x.isdigit() for x in piles):
            print(bcolors.ERROR + "\t[ERROR] Enter integers only. Try again..." + bcolors.ENDC)
        break
    
    return [int(pile) for pile in piles]

def nim2Initiate():
    print(bcolors.QUESTION + '\t[Q2] Enter the piles of the game, separated by commas (e.g. 3,4,5,6):' + bcolors.ENDC)
    while True:
        piles = input('\t' + bcolors.GREY + bcolors.BOLD).split(',')
        print(bcolors.ENDC, end='') # clear styling

        if len(piles) < 1:
            print(bcolors.ERROR + '\t[ERROR] You must provide at least one pile. Try again...' + bcolors.ENDC)
        if not all(x.isdigit() for x in piles):
            print(bcolors.ERROR + "\t[ERROR] Enter integers only. Try again..." + bcolors.ENDC)
        break
    
    return [int(pile) for pile in piles]

def nim3Initiate():
    print(bcolors.QUESTION + '\t[Q2] Enter the size of the pile (a positive integer):' + bcolors.ENDC)
    while True:
        pile = input('\t' + bcolors.GREY + bcolors.BOLD)
        print(bcolors.ENDC, end='') # clear styling

        if pile.isdigit() and int(pile) > 0:
            break
        print(bcolors.ERROR + '\t[ERROR] You must provide a positive integer. Try again...' + bcolors.ENDC)
    
    # also ask for k, between 1 and pile
    print(bcolors.QUESTION + '\t[Q3] Enter the maximum number of matches that can be removed from the pile (a positive integer):' + bcolors.ENDC)
    while True:
        k = input('\t' + bcolors.GREY + bcolors.BOLD)
        print(bcolors.ENDC, end='') # clear styling

        if k.isdigit() and int(k) > 0 and int(k) <= int(pile):
            break
        print(bcolors.ERROR + '\t[ERROR] You must provide a positive integer between 1 and the pile size. Try again...' + bcolors.ENDC)

    return int(pile), int(k)

def nim4Initiate():
    print(bcolors.QUESTION + '\t[Q2] Enter the two piles of the game, separated by a comma (e.g. 3,4):' + bcolors.ENDC)
    while True:
        piles = input('\t' + bcolors.GREY + bcolors.BOLD).split(',')
        print(bcolors.ENDC, end='') # clear styling

        if len(piles) != 2:
            print(bcolors.ERROR + '\t[ERROR] You must provide exactly two piles. Try again...' + bcolors.ENDC)
        if not all(x.isdigit() for x in piles):
            print(bcolors.ERROR + "\t[ERROR] Enter integers only. Try again..." + bcolors.ENDC)
        break
    
    return [int(pile) for pile in piles]

def nim1Play(firstToAct, piles):
    turn = firstToAct
    screenClear()

    while sum(piles) > 0:
        drawNimPalette(len(piles), piles)
        print(bcolors.MSG + "\tWaiting on " + bcolors.UNDERLINE + 
            turn + bcolors.ENDC + bcolors.MSG + " to act." + bcolors.ENDC)
        
        if turn == 'player':
            print(bcolors.QUESTION + PLUSLINE)
            print(bcolors.QUESTION + '\tHow many matches would you like to remove and from which pile \n'
                  '\t(separate with comma)? eg. 2 matches from pile 1 => 1,2' + bcolors.ENDC)
            print(bcolors.QUESTION + PLUSLINE)

            #check for valid pile and amount of matches
            while True:
                pile, matches = input("\t" + bcolors.GREY + bcolors.BOLD).split(',')
                print(bcolors.ENDC, end='') # clear bold and grey
                
                pile = int(pile)
                matches = int(matches)

                if pile < 0 or pile >= len(piles) or piles[pile] == 0:
                    print(bcolors.ERROR + '\t[ERROR] You must provide a valid non-empty pile index between 0 and', len(piles)-1, '. Try again...' + bcolors.ENDC)
                    continue

                if matches < 0 or matches > piles[pile]:
                    print(bcolors.ERROR + '\t[ERROR] You must provide a positive integer between 1 and', piles[pile], '. Try again...' + bcolors.ENDC)
                    continue
                
                break

            piles[pile] -= matches
            turn = 'computer'
            continue

        if turn == 'computer':
            #find sum of nim game (xor)
            nimSum = reduce(lambda x, y: x ^ y, piles)

            # losing case, play "randomly"
            # basically, change the nimsum to the biggest one you can
            if nimSum == 0:
                highestContributingBit = int.bit_length(max(piles)) - 1
                # find all piles which have the highest bit set
                highestBitPiles = [i for i, pile in enumerate(piles) if pile & (1 << highestContributingBit)]
                
                randomPile = random.choice(highestBitPiles)

                # set pile to binary unsigned inverse (guaranteed to be less than pile)
                mask = (1 << (highestContributingBit+1)) - 1
                newPile = mask ^ piles[randomPile] # xor to inverse bits
                matchesToRemove = piles[randomPile] - newPile

                #notify player of move
                print(bcolors.COMMENT + MINUSLINE)
                print("\tComputer is playing randomly...\n\tDecided to remove ", end='')
                print(bcolors.UNDERLINE + bcolors.BOLD + str(matchesToRemove) + bcolors.ENDC + bcolors.COMMENT +
                        ' matches from pile', bcolors.UNDERLINE + bcolors.BOLD + str(randomPile) + bcolors.ENDC + bcolors.COMMENT + '.' + bcolors.ENDC)
                print(bcolors.COMMENT + MINUSLINE + bcolors.ENDC)

                piles[randomPile] -= matchesToRemove

            #winning case, play strategically
            else:
                highestContributingBit = int.bit_length(nimSum) - 1
                # find pile which contributes to highest bit in the nim sum
                for i, pile in enumerate(piles):
                    # if the highest bit is set in this pile
                    if pile & (1 << highestContributingBit):
                        matchesToRemove = pile - (pile ^ nimSum) # xor to matches to remove
                        
                        #notify player of move
                        print(bcolors.COMMENT + MINUSLINE)
                        print("\tComputer is playing strategically...\n\tDecided to remove ", end='')
                        print(bcolors.UNDERLINE + bcolors.BOLD + str(matchesToRemove) + bcolors.ENDC + bcolors.COMMENT + 
                              ' matches from pile', bcolors.UNDERLINE + bcolors.BOLD + str(i) + bcolors.ENDC + bcolors.COMMENT + '.' + bcolors.ENDC)
                        print(bcolors.COMMENT + MINUSLINE + bcolors.ENDC)

                        piles[i] -= matchesToRemove
                        break # don't check rest of for loop

            turn = 'player'
            continue

    # game ended, so return previous turn
    if turn == 'player':
        return 'computer'
    else: return 'player'

def nim2Play(firstToAct, piles):
    turn = firstToAct
    screenClear()

    while sum(piles) > 0:
        drawNimPalette(len(piles), piles)
        print(bcolors.MSG + "\tWaiting on " + bcolors.UNDERLINE + 
            turn + bcolors.ENDC + bcolors.MSG + " to act." + bcolors.ENDC)
        
        if turn == 'player':
            print(bcolors.QUESTION + PLUSLINE)
            print(bcolors.QUESTION + '\tHow many matches would you like to remove and from which pile \n'
                  '\t(separate with comma)? eg. 2 matches from pile 1 => 1,2' + bcolors.ENDC)
            print(bcolors.QUESTION + PLUSLINE)

            #check for valid pile and amount of matches
            while True:
                pile, matches = input("\t" + bcolors.GREY + bcolors.BOLD).split(',')
                print(bcolors.ENDC, end='') # clear bold and grey
                
                pile = int(pile)
                matches = int(matches)

                if pile < 0 or pile >= len(piles) or piles[pile] == 0:
                    print(bcolors.ERROR + '\t[ERROR] You must provide a valid non-empty pile index between 0 and', len(piles)-1, '. Try again...' + bcolors.ENDC)
                    continue

                if matches < 0 or matches > piles[pile]:
                    print(bcolors.ERROR + '\t[ERROR] You must provide a positive integer between 1 and', piles[pile], '. Try again...' + bcolors.ENDC)
                    continue
                
                break

            piles[pile] -= matches
            turn = 'computer'
            continue

        if turn == 'computer':
            #find sum of nim game (xor)
            nimSum = reduce(lambda x, y: x ^ y, piles)

            # losing case, play "randomly"
            # basically, change the nimsum to the biggest one you can
            if nimSum == 0:
                highestContributingBit = int.bit_length(max(piles)) - 1
                # find all piles which have the highest bit set
                highestBitPiles = [i for i, pile in enumerate(piles) if pile & (1 << highestContributingBit)]
                
                randomPile = random.choice(highestBitPiles)

                # set pile to binary unsigned inverse (guaranteed to be less than pile)
                mask = (1 << (highestContributingBit+1)) - 1
                newPile = mask ^ piles[randomPile] # xor to inverse bits
                matchesToRemove = piles[randomPile] - newPile

                #notify player of move
                print(bcolors.COMMENT + MINUSLINE)
                print("\tComputer is playing randomly...\n\tDecided to remove ", end='')
                print(bcolors.UNDERLINE + bcolors.BOLD + str(matchesToRemove) + bcolors.ENDC + bcolors.COMMENT +
                        ' matches from pile', bcolors.UNDERLINE + bcolors.BOLD + str(randomPile) + bcolors.ENDC + bcolors.COMMENT + '.' + bcolors.ENDC)
                print(bcolors.COMMENT + MINUSLINE + bcolors.ENDC)

                piles[randomPile] -= matchesToRemove

            #winning case, play strategically
            else:
                # if all but one piles have 1 match remove matches so that the number
                # of piles with 1 match is odd
                if len([pile for pile in piles 
                        if pile == 1 or pile == 0]) == len(piles) - 1:
                    
                    # find the pile with more than 1 match
                    for i, pile in enumerate(piles):
                        if pile > 1:
                            # figure out if number of piles with atleast 1 match is odd
                            if len([pile for pile in piles if pile >= 1]) % 2 == 1:
                                 matchesToRemove = pile - 1
                            else:
                                matchesToRemove = pile

                            #notify player of move
                            print(bcolors.COMMENT + MINUSLINE)
                            print("\tComputer is playing strategically...\n\tDecided to remove ", end='')
                            print(bcolors.UNDERLINE + bcolors.BOLD + str(matchesToRemove) + bcolors.ENDC + bcolors.COMMENT + 
                                ' matches from pile', bcolors.UNDERLINE + bcolors.BOLD + str(i) + bcolors.ENDC + bcolors.COMMENT + '.' + bcolors.ENDC)
                            print(bcolors.COMMENT + MINUSLINE + bcolors.ENDC)

                            piles[i] -= matchesToRemove

                            break # don't check rest of for loop

                # else conntinue with sum-strategy
                highestContributingBit = int.bit_length(nimSum) - 1
                # find pile which contributes to highest bit in the nim sum
                for i, pile in enumerate(piles):
                    # if the highest bit is set in this pile
                    if pile & (1 << highestContributingBit):
                        matchesToRemove = pile - (pile ^ nimSum) # xor to matches to remove
                        
                        #notify player of move
                        print(bcolors.COMMENT + MINUSLINE)
                        print("\tComputer is playing strategically...\n\tDecided to remove ", end='')
                        print(bcolors.UNDERLINE + bcolors.BOLD + str(matchesToRemove) + bcolors.ENDC + bcolors.COMMENT + 
                              ' matches from pile', bcolors.UNDERLINE + bcolors.BOLD + str(i) + bcolors.ENDC + bcolors.COMMENT + '.' + bcolors.ENDC)
                        print(bcolors.COMMENT + MINUSLINE + bcolors.ENDC)

                        piles[i] -= matchesToRemove

                        break # don't check rest of for loop

            turn = 'player'
            continue

    # game ended, so announce winner
    return turn

def nim3Play(firstToAct, pile, k):
    turn = firstToAct
    screenClear()

    while pile > 0:
        drawNimPalette(1, [pile])
        print(bcolors.MSG + "\tWaiting on " + bcolors.UNDERLINE + 
            turn + bcolors.ENDC + bcolors.MSG + " to act." + bcolors.ENDC)
        
        if turn == 'player':
            print(bcolors.QUESTION + PLUSLINE)
            print(bcolors.QUESTION + '\tHow many matches would you like to remove?' + bcolors.ENDC)
            print(bcolors.QUESTION + PLUSLINE)

            while True:
                matches = int(input("\t" + bcolors.GREY + bcolors.BOLD))
                print(bcolors.ENDC, end='') # clear bold and grey

                if matches > 0 and matches <= k:
                    break
                print(bcolors.ERROR + '\t[ERROR] You must provide a positive integer between 1 and', k, '. Try again...' + bcolors.ENDC)

            pile -= matches
            turn = 'computer'
            continue

        if turn == 'computer':
            # losing case, play randomly
            if pile % (k + 1) == 0:
                matches = random.randint(1, k)
                print(bcolors.COMMENT + MINUSLINE)
                print("\tComputer is playing randomly...\n\tDecided to remove ", end='')
                print(bcolors.UNDERLINE + bcolors.BOLD + str(matches) + bcolors.ENDC + bcolors.COMMENT + ' matches.' + bcolors.ENDC)
                print(bcolors.COMMENT + MINUSLINE + bcolors.ENDC)
                
            # winning case, grab matches so that pile has a multiple of k+1 matches
            else:
                matches = pile % (k + 1) 
                print(bcolors.COMMENT + MINUSLINE)
                print("\tComputer is playing strategically...\n\tDecided to remove ", end='')
                print(bcolors.UNDERLINE + bcolors.BOLD + str(matches) + bcolors.ENDC + bcolors.COMMENT + ' matches.' + bcolors.ENDC)
                print(bcolors.COMMENT + MINUSLINE + bcolors.ENDC)

            pile -= matches
            turn = 'player'
            continue
    
    # turn changed, so return previous turn
    if turn == 'player':
        return 'computer'
    else: return 'player'

def nim4IsLosing(piles, losingGames):
    piles = sorted(piles, reverse=True)
    if piles[0] not in losingGames[0]:
        return False
    
    index = losingGames[0].index(piles[0])
    if piles[1] != losingGames[1][index]:
        return False
    
    return True

def nim4Play(firstToAct, piles):
    turn = firstToAct
    screenClear()

    # calculate possible losing games for computer
    losingGames = [[0], [0]]

    for i in range(1, max(piles)+1):
        i_pair = i - len(losingGames[0])

        if i_pair in losingGames[0]:
            continue

        if i_pair in losingGames[1]:
             continue
        
        losingGames[0].append(i)
        losingGames[1].append(i_pair)

    while sum(piles) > 0:
        drawNimPalette(len(piles), piles)
        print(bcolors.MSG + "\tWaiting on " + bcolors.UNDERLINE + 
            turn + bcolors.ENDC + bcolors.MSG + " to act." + bcolors.ENDC)
        
        if turn == 'player':
            print(bcolors.QUESTION + PLUSLINE)
            print(bcolors.QUESTION + '\tHow many matches would you like to remove and from which pile \n'
                  '\t(separate with comma)? Select "pile 2" to remove from both. \n'
                  '\teg. 2 matches from pile 1 => 1,2' + bcolors.ENDC)
            print(bcolors.QUESTION + PLUSLINE)

            #check for valid pile and amount of matches
            while True:
                pile, matches = input("\t" + bcolors.GREY + bcolors.BOLD).split(',')
                print(bcolors.ENDC, end='') # clear bold and grey
                
                pile = int(pile)
                matches = int(matches)

                # remove from both piles
                if pile == 2:
                    if matches <= min(piles):
                        piles[0] -= matches
                        piles[1] -= matches
                        break
                    else:
                        print(bcolors.ERROR + '\t[ERROR] You must provide a number of matches greater than',
                              'or equal to the smallest pile. Try again...' + bcolors.ENDC)
                        continue
                        
                # remove from 1 pile
                if pile < 0 or pile > len(piles) or piles[pile] == 0:
                    print(bcolors.ERROR + '\t[ERROR] You must provide a valid non-empty pile index between 0 and', len(piles), '. Try again...' + bcolors.ENDC)
                    continue
                
                if matches < 0 or matches > piles[pile]:
                    print(bcolors.ERROR + '\t[ERROR] You must provide a positive integer between 1 and', piles[pile], '. Try again...' + bcolors.ENDC)
                    continue
                
                piles[pile] -= matches
                break

            turn = 'computer'
            continue

        if turn == 'computer':
            # losing case, play randomly
            if nim4IsLosing(piles, losingGames):
                # remove random number of matches from random pile
                # first figure out the random number, then figure out from which
                # pile to remove the matches from
                randomNum = random.randint(1, sum(piles))
                randomPile = int(randomNum / (piles[0] + 1))
                if randomPile == 1:
                    randomNum = randomNum - piles[0]
                
                #notify player of move
                print(bcolors.COMMENT + MINUSLINE)
                print("\tComputer is playing randomly...\n\tDecided to remove ", end='')
                print(bcolors.UNDERLINE + bcolors.BOLD + str(randomNum) + bcolors.ENDC + bcolors.COMMENT +
                        ' matches from pile', bcolors.UNDERLINE + bcolors.BOLD + str(randomPile) + bcolors.ENDC + bcolors.COMMENT + '.' + bcolors.ENDC)
                print(bcolors.COMMENT + MINUSLINE + bcolors.ENDC)

                piles[randomPile] -= randomNum

            #winning case, play strategically
            else:
                # if game is located diagonally of a losing game, move to that game
                diff = max(piles) - min(piles)

                if (len(losingGames[0]) >= diff and losingGames[0][diff] <= max(piles)):
                    # remove matches so that the game is a losing game
                    matchesToRemove = max(piles) - losingGames[0][diff]

                    #notify player of move
                    print(bcolors.COMMENT + MINUSLINE)
                    print("\tComputer is playing strategically...\n\tDecided to remove ", end='')
                    print(bcolors.UNDERLINE + bcolors.BOLD + str(matchesToRemove) + bcolors.ENDC + bcolors.COMMENT + 
                        ' matches from ', bcolors.UNDERLINE + bcolors.BOLD + "both piles" + bcolors.ENDC + bcolors.COMMENT + '.' + bcolors.ENDC)
                    print(bcolors.COMMENT + MINUSLINE + bcolors.ENDC)

                    piles[0] -= matchesToRemove
                    piles[1] -= matchesToRemove
                
                # else move orthogonally to a losing game
                else:
                    # bigger pile will stay bigger
                    if min(piles) in losingGames[1]:
                         matchingIndex = losingGames[1].index(min(piles))
                         matchesToRemove = max(piles) - losingGames[0][matchingIndex]
                         
                    # else game will "flip"
                    else:
                        matchingIndex = losingGames[0].index(min(piles))
                        matchesToRemove = max(piles) - losingGames[1][matchingIndex]

                    pileToRemoveFrom = 0 if piles[0] == max(piles) else 1

                    #notify player of move
                    print(bcolors.COMMENT + MINUSLINE)
                    print("\tComputer is playing strategically...\n\tDecided to remove ", end='')
                    print(bcolors.UNDERLINE + bcolors.BOLD + str(matchesToRemove) + bcolors.ENDC + bcolors.COMMENT + 
                        ' matches from pile', bcolors.UNDERLINE + bcolors.BOLD + str(pileToRemoveFrom) + bcolors.ENDC + bcolors.COMMENT + '.' + bcolors.ENDC)
                    print(bcolors.COMMENT + MINUSLINE + bcolors.ENDC)

                    piles[pileToRemoveFrom] -= matchesToRemove

            turn = 'player'
            continue

    # game ended, so return previous turn
    if turn == 'player':
        return 'computer'
    else: return 'player'
