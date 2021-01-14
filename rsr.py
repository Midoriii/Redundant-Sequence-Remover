'''
Copyright (c) 2021, Štěpán Beneš

View README for instructions.
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
    Simple argument parser. The selected argument values are kept as globals
    since it's much more appropriate than passing them around to the functions.
    Given arguments are also checked for any errors.
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
    Creates Pandas dataframes from the provided .csv files. The dataframe for
    merged sequences begins as a deep copy of the long sequences' dataframe.
    All three are returned to the caller.
    '''
    short_sequences_df = pd.read_csv(SHORT_S_FILE)
    long_sequences_df = pd.read_csv(LONG_S_FILE)
    merged_sequences_df = long_sequences_df.copy(deep=True)
    return short_sequences_df, long_sequences_df, merged_sequences_df


def sequence_checker(short_sequences_df, long_sequences_df, merged_sequences_df):
    '''
    Each sequence from the short_sequences dataframe is compared with all of the
    sequences from the long_sequences dataframe. If no match is found, the short
    sequence is added to the merged dataframe, along with its additional info.
    Note that appended short sequences contain the prefix 's_' in the merged file.
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
    Compares the given sequences letter by letter. If the whole shorter sequence
    is not a part of the longer one, False is returned. The argument 'reverse'
    controls, whether the comparison of the two sequences should start from
    the front or from the back. Note that the sequences are only checked from
    the start or from the end, substrings lying in the middle are not a concern.
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
    Saves the finalized merged dataframe to specified or default output file.
    '''
    merged_sequences_df.to_csv(MERGED_S_FILE, index=False)


if __name__ == "__main__":
    parse_arguments()
    save_merged_sequences(sequence_checker(*create_dataframes()))
