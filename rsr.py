'''
Copyright (c) 2021, Štěpán Beneš


'''
import sys
import getopt
import os
import pandas as pd

# Global options
SHORT_S_FILE = ""
LONG_S_FILE = ""
MERGED_S_FILE = "Data/merged.csv"
FORWARDS_ONLY = False
BACKWARDS_ONLY = False


def parse_arguments():
    '''
    bla
    '''
    global SHORT_S_FILE
    global LONG_S_FILE
    global MERGED_S_FILE
    global FORWARDS_ONLY
    global BACKWARDS_ONLY

    try:
        arguments, _ = getopt.getopt(sys.argv[1:], "s:l:m:fb")
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for arg, value in arguments:
        if arg == "-s":
            SHORT_S_FILE = "Data/" + value + ".csv"
        elif arg == "-l":
            LONG_S_FILE = "Data/" + value + ".csv"
        elif arg == "-m":
            MERGED_S_FILE = "Data/" + value  + ".csv"
        elif arg == "-f":
            FORWARDS_ONLY = True
        elif arg == "-b":
            BACKWARDS_ONLY = True

    if FORWARDS_ONLY and BACKWARDS_ONLY:
        print("Parameters '-f' and '-b' cannot be combined. If you desire to check "
              + "the sequences in both forwards and backwards manner, simply do not "
              + "specify any parameter.")
        sys.exit(2)

    if SHORT_S_FILE == "" or LONG_S_FILE == "":
        print("You need to specify both of the input files.")
        sys.exit(2)

    if not os.path.isfile(SHORT_S_FILE) or not os.path.isfile(LONG_S_FILE):
        print("Specified files are invalid.")
        sys.exit(2)


def create_dataframes():
    '''
    bla
    '''
    short_sequences_df = pd.read_csv(SHORT_S_FILE)
    long_sequences_df = pd.read_csv(LONG_S_FILE)
    merged_sequences_df = long_sequences_df.copy(deep=True)
    return short_sequences_df, long_sequences_df, merged_sequences_df


def sequence_checker(short_sequences_df, long_sequences_df, merged_sequences_df):
    '''
    bla
    '''
    long_sequences = long_sequences_df['sequence'].tolist()

    for _, row in short_sequences_df.iterrows():
        duplicate_found = False

        for sequence in long_sequences:
            if not BACKWARDS_ONLY:
                if sequences_match(row['sequence'], sequence):
                    duplicate_found = True
                    break
            if not FORWARDS_ONLY:
                if sequences_match(row['sequence'], sequence, True):
                    duplicate_found = True
                    break

        if not duplicate_found:
            row['ASVNumber'] = "s_" + row['ASVNumber']
            merged_sequences_df = merged_sequences_df.append(row)

    return merged_sequences_df


def sequences_match(shorter, longer, reverse=False):
    '''
    bla
    '''
    if reverse:
        shorter = shorter[::-1]
        longer = longer[::-1]

    for a, b in zip(shorter, longer):
        if a != b:
            return False
    return True


def save_merged_sequences(merged_sequences_df):
    '''
    bla
    '''
    merged_sequences_df.to_csv(MERGED_S_FILE, index=False)


if __name__ == "__main__":
    '''
    bla
    '''
    parse_arguments()
    save_merged_sequences(sequence_checker(*create_dataframes()))
