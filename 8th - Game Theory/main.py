from fun import *

showRules()

while True:
    screenClear()
    if not startNewGame():
        break

    nimVariantChoice = chooseNIMVariant()
    turn = whoGoesFirst()

    print( bcolors.MSG + PLUSLINE + bcolors.ENDC )
    print( bcolors.MSG + '\tA new instance of',nimVariantChoice,'is about to start.' + bcolors.ENDC )
    print( bcolors.MSG + '\tThe first move will be done by the ' + 
          bcolors.UNDERLINE + turn + bcolors.ENDC + bcolors.MSG + '.' + bcolors.ENDC )
    print( bcolors.MSG + PLUSLINE + bcolors.ENDC )
    
    match nimVariantChoice:
        case "NIM-1":
            piles = nim1Initiate()
            winner = nim1Play(turn, piles)

        case "NIM-2":
            piles = nim2Initiate()
            winner = nim2Play(turn, piles)
            
        case "NIM-3":
            pile, k = nim3Initiate()
            winner = nim3Play(turn, pile, k)

        case "NIM-4":
            piles = nim4Initiate()
            winner = nim4Play(turn, piles)
        
    # game ended, announce winner
    print( bcolors.MSG + PLUSLINE + bcolors.ENDC )
    print( bcolors.MSG + '\tThe game has ended. The winner is the ' + 
          bcolors.UNDERLINE + winner + bcolors.ENDC + bcolors.MSG + '.' + bcolors.ENDC )
    print( bcolors.MSG + PLUSLINE + bcolors.ENDC )
    input( bcolors.GREY + '\tPress Enter to continue...' + bcolors.ENDC )
