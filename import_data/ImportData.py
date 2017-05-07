#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ulises Olivares'

import csv
from datetime import *
import arrow
from os import walk
from collections import defaultdict
import itertools
import time
from datetime import datetime
import datetime



"""
    Define global variables
"""
TZDifference = -5;  # -5 hours of difference

# This lists store all the global data (complete set of all datasets)
globaDate = {}
globalTime = {}
globalID = {}

installationDates = {}


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

    """ This Function retrieves all the files for a specified path"""

    def exploreDirs(self, path):
        # Iterate on the path and get the filenames
        dirs = []
        for (dirpath, dirnames, filenames) in walk(path):
            dirs.extend(dirnames)
            break
        return dirs

    def adjustTime(self, originalTime, row, tvar):
        """
        This function adjusts the time to an specific Time Zone
        :param originalTime:
        :param row:
        :param tvar:
        :return:
        """
        correctedTime = originalTime + TZDifference
        if (correctedTime < 10):
            if (correctedTime < 0):  # handle negative cases FIXME: this is the past day correct it
                tmp2 = str(24 + correctedTime) + row[tvar + 3:-1]
            else:
                tmp2 = str(0) + str(originalTime + TZDifference) + row[tvar + 3:-1]
        else:
            tmp2 = str(originalTime + TZDifference) + row[tvar + 3:-1]
        return tmp2

    def importRawData(self, rawFiles, rawPath):
        """
        This function imports all the
        :param rawFiles:
        :param rawPath:
        :return:
        """
        for i in rawFiles:
            # Declare the lists for storing
            date = []
            time = []
            sensorID = []
            for j in rawFiles[i]:
                try:
                    currentFile = str(rawPath + i + '\\' + j)
                    # print currentFile
                    f = open(currentFile)
                    for row in csv.reader(f):
                        # Skip first line of the csv
                        if row[0][0] == '#':
                            continue
                        # Remove all the FFFFFF reads those are for test proposes
                        # FIXME: store all the FFFFFF reads for statistical proposes
                        elif row[1][0] != 'F':
                            # Parse dete and time values
                            tvar = row[0].find('T')



                            # Parse Time in a 'HH:MM:SS' format
                            tmp1 = int(row[0][tvar + 1:tvar + 3]) # Extract hour and adjust time zone
                            tmp2 = self.adjustTime(tmp1, row[0], tvar)
                            # Build a datetime from a string
                            completeDateTime= datetime.datetime(int (row[0][0:4]), int (row[0][4:6]) , int (row[0][6:tvar]), int (tmp2[:2]) , int (tmp2[2:4]) , int (tmp2[4:6]))

                            # Append date and time to the lists
                            date.append(completeDateTime.date())
                            time.append(completeDateTime.time())

                            """
                            # Parse time
                            tmpTime = arrow.get(tmp2, 'HHmmss').time()
                            time.append(tmpTime)


                            # Parse Date
                            tmpDate = arrow.get(row[0][:tvar], 'YYYYMD').date()
                            date.append(tmpDate)
                            """

                            # Parse ID and store it in a list
                            sensorID.append(row[1][:24])
                        #else:
                        #    print "Unknown value or error in input file" + str(row)
                except csv.Error, e:
                    sys.exit('file %s, line %d: %s' % (currentFile, f.line_num, e))
            globaDate[i] = date
            globalID[i] = sensorID
            globalTime[i] = time

    def importInstallationFiles(self, installationFiles, installationPath):
        """

        :param installationFiles:
        :param installationPath:
        :return:
        """
        # sort the name of the installation files to be sure that they will be in order
        #installationFiles = installationFiles.sort()
        for i in installationFiles:
            try:
                currentFile = str(installationPath + i)
                f = open(currentFile)
                for row in csv.reader(f):
                    # Detects the first digit if it begins with two it is a valid entry
                    if row[0]:
                        if row[0][0] == '2':
                            if row[1] not in installationDates:
                                installationDates[row[1]] = row[0]
                            else:
                                print "Errror: Plaese, check te input installation files" \
                                      " You have inserted repeated IDs"
            except csv.Error, e:
                sys.exit('file %s, line %d: %s' % (currentFile, f.line_num, e))

    def importInputData(self, path):
        """
        This method invocates other methods to import input data (raw and installation data)
        :param path:
        :return:
        """
        lenDict = {}

        # Get all the files tha contains all the information related to IDs and installation date
        installationPath = path + "\\installation_data\\"
        installationFiles = self.exploreFiles(installationPath)
        self.importInstallationFiles(installationFiles, installationPath)

        # Get all the files related to raw data
        rawPath = path + "\\raw_data\\"
        # This is a list wich contains in each possition a datasate for an specific Hive
        rawFiles = {}

        # Explore the contents of "path + raw_data" to find all the folders
        rawDataDirs = self.exploreDirs(rawPath)
        rawDataDirs.sort(reverse=True)
        for i in rawDataDirs:
            rawFiles[i] = (self.exploreFiles(rawPath + i))
            lenDict[i] = len(rawFiles[i])
        self.importRawData(rawFiles, rawPath)
        return lenDict

    def getCompleteDictionary(self):
        """
        This method creates a nested dictionary with all the elements ID => Date => Time
        :return:
        """
        fullDict = {}
        completeDateDict = {}
        completeIdDict = {}
        for i  in globalID:
            completeDictionary = {}
            idDict = defaultdict(list)
            dateDict = defaultdict(list)
            for j, k ,l in itertools.izip(globalID[i], globaDate[i], globalTime[i]):
                idDict[j].append(k)
                dateDict[k].append(l)
                if j in completeDictionary.keys():
                    completeDictionary[j][k].append(l)
                else:
                    completeDictionary[j] = defaultdict(list)
                    completeDictionary[j][k].append(l)
            fullDict[i] = completeDictionary
            completeIdDict[i] = idDict
            completeDateDict[i] = dateDict
        return completeIdDict, completeDateDict, fullDict


    def getIdDictionary(self):
        """
        This method gets a dictionary which contains all the ID and dates
        :return:
        """
        # completeIdDict = ID => date
        completeIdDict = {}
        for i in globalID:
            id = 0
            date = 0
            idDict = defaultdict(list)

            for j, k in itertools.izip(globalID[i], globaDate[i]):
                if j not in idDict.keys():
                    id = id + 1
                idDict[j].append(k) #FIXME: CHECK IF THIS IS CORRECT AND APPLY THIS APPORACH TO DATEDICT
                date = date +1
            completeIdDict[i] =  idDict
        print "Id Dict: Total Elements: ID: " + str(id) + " Date: " + str(date)

        for i in completeIdDict:
            print " Ids: " + str(len(completeIdDict[i].keys())) + " Dates: " + str(len(completeIdDict[i].values()))
        return completeIdDict

    def getDateDictionaary(self):
        """
        This method returns a complete dictionary of
        :return:
        """
        # complete dateDict = Date => time
        completeDateDict = {}
        for i in globaDate:
            dateDict = defaultdict(list)
            for j, k in itertools.izip(globaDate[i], globalTime[i]):
                dateDict[j].append(k);
            completeDateDict[i] = dateDict
        return completeDateDict
