#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ulises Olivares'

import csv
from datetime import *
import arrow
from os import walk
from collections import defaultdict
import itertools


"""
    Define global variables
"""
TZDifference = -5;  # -5 hours of difference
date = []
time = []
sensorID = []


class ImportData:

    def __init__(self):

        """ Put some initialization code"""

    """ This Function retrieves all the files for a specified path"""
    def exploreFiles(self, path):
        # Iterate on the path and get the filenames
        files = []
        for (dirpath, dirnames, filenames) in walk(path):
            files.extend(filenames)
            break
        return files

    # This function adjusts the time to an specific Time Zone
    def adjustTime(self, originalTime, row, tvar):
        correctedTime = originalTime + TZDifference
        if (correctedTime < 10):
            if (correctedTime < 0):  # handle negative cases FIXME: this the past day correct it
                tmp2 = str(24 + correctedTime) + row[tvar + 3:-1]
            else:
                tmp2 = str(0) + str(originalTime + TZDifference) + row[tvar + 3:-1]
        else:
            tmp2 = str(originalTime + TZDifference) + row[tvar + 3:-1]
        return tmp2

    """ This function imports all the values in a CSV file"""

    def importCSV(self, path):
        #FIXME: CORRECT THE TIMEZONE
        files = self.exploreFiles(path)
        for i in files:
            currentFile = str(path + i)
            #print currentFile
            f = open(currentFile) #FIXME: PUT IN A TRY TO VALIDATE IF THERE ARE EMPTY OR DAMAGED FILES
            for row in csv.reader(f):
                # Skip first line
                if row[0][0] == '#':
                    continue
                # Remove all the FFFFFF reads those are for test proposses
                #FIXME: store all the FFFFFF reads for statististical proposes
                elif row[1][0] != 'F':
                    # Parse dete and time values
                    tvar = row[0].find('T')

                    # Parse Time in a 'HH:MM:SS' format
                    tmp1 = int(row[0][tvar + 1:tvar + 3])
                    tmp2 = self.adjustTime(tmp1, row[0], tvar)
                    tmpTime = arrow.get(tmp2, 'HHmmss').time()
                    time.append(tmpTime)

                    # Parse Date
                    tmpDate = arrow.get(row[0][:tvar], 'YYYYMD').date()
                    date.append (tmpDate)

                    # Parse ID and store it in a list
                    sensorID.append(row[1][:24])

        return len(files)

    def getCompleteDictionary(self):
        # Create a nested dictionary with all the elements ID => Date => Time
        completeDictionary = {}
        for i, j ,k in itertools.izip(sensorID, date, time):
            if i in completeDictionary.keys():
                completeDictionary[i][j].append(k)
            else:
                completeDictionary[i] = defaultdict(list)
                completeDictionary[i][j].append(k)
        #print completeDictionary
        return completeDictionary


    def getIdDictionary(self):
        # IdDict = ID => date
        IdDict = defaultdict(list)
        for i, j in itertools.izip(sensorID, date):
            IdDict[i].append(j)
        return IdDict

    def getDateDictionaary(self):
        # dateDict = Date => time
        dateDict = defaultdict(list)
        for i, j in itertools.izip(date, time):
            dateDict[i].append(j);
        return dateDict
