'''
Copyright (c) 2021, Štěpán Beneš


'''
import pandas as pd
import sys
import getopt

# Global options
SHORT_S_FILE = ""
LONG_S_FILE = ""
FORWARDS_ONLY = False
BACKWARDS_ONLY = False


def parse_arguments():
    '''
    bla
    '''
    global SHORT_S_FILE
    global LONG_S_FILE
    global FORWARDS_ONLY
    global BACKWARDS_ONLY

    try:
        arguments, _ = getopt.getopt(sys.argv[1:], "s:l:fb")
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for arg, value in arguments:
        if arg == "-s":
            SHORT_S_FILE = "Data/" + value
        elif arg == "-l":
            LONG_S_FILE = "Data/" + value
        elif arg == "-f":
            FORWARDS_ONLY = True
        elif arg == "-b":
            BACKWARDS_ONLY = True

    if FORWARDS_ONLY and BACKWARDS_ONLY:
        print("Parameters '-f' and '-b' cannot be combined. If you desire to check "
              + "the sequences in both forwards and backwards manner, simply do not "
              + "specify any parameter.")
        sys.exit(2)
    return


def create_dataframes():
    '''
    bla
    '''
    short_sequences = pd.read_csv(SHORT_S_FILE)
    long_sequences = pd.read_csv(LONG_S_FILE)
    merged_sequences = long_sequences.copy(deep=True)
    return short_sequences, long_sequences, merged_sequences


if __name__ == "__main__":
    '''
    bla
    '''
    parse_arguments()

    short_sequences, long_sequences, merged_sequences = create_dataframes()
