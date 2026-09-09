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
