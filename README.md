# Redundant-Sequence-Remover
Tailored script for removing redundant sequences from database. Expects the provided data to be of *.csv* type, placed in Data folder in the main folder.


Two necessary arguments of the **rsr.py** script are **-s** and **-l**, specifying the path to the sequence files. Note that adding *.csv* as the suffix is done by the script.

The output merged file can be specified by the argument **-m**. Arguments **-b** and **-f** specify whether the shorter sequences should be checked from the back or from the front of the longer sequences. If neither of those two is specified, both checks are performed.

Non-duplicate shorter sequences are added to the merged file, with the prefix **s_** added to their ASVNumber.


Note that column names **ASVNumber** and **sequence** are expected in the *.csv* files
