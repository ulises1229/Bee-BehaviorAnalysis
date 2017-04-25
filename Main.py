#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ulises Olivares'

from analyze_data.AnalizeData import AnalizeData
from import_data.ImportData import ImportData
from latex_report.GenerateReport import GenerateReport
from plots.Plot import Plot
from clean_data.CleanData import CleanData

from datetime import datetime, timedelta

# Data folder
data = "data/"

def main():

    # Read all the CSV files and import data
    imp = ImportData()
    #imp.importCSV()

    # FIXME: how to pass by reference all the parameters implement this to reduce the memory footprint
    noFiles = imp.importCSV(data)
    idData = imp.getIdDictionary()
    dateData = imp.getDateDictionaary()
    completeData = imp.getCompleteDictionary()
    print "Number of files: " + str(noFiles)
    print "Active Days: " + str(len(dateData))
    print "Non-Active Days: " + str(noFiles - len(dateData))

    files = {}
    files['Active Days'] = len(dateData)
    files['Non-Active Days'] = noFiles - len(dateData)

    plot = Plot()
    plot.pieChart(files, "chartNumLectures", "Relation: Active VS Non-active Days")


    # FIXME: CLEAN DATA BEFORE ANALYZE IT
    # Clean data
    clean = CleanData()
    FMT = '%H:%M:%S'

    threshold = datetime.strptime("00:01:00", FMT)
    threshold = timedelta(hours=threshold.hour, minutes=threshold.minute, seconds=threshold.second)
    print("Cleaning data...\n" + "Threshold: " + str(threshold))

    """
    This method returns a dictionary cleanData with the information:
    'cleanCompleteDict': Dictionary
    'cleanIdDict': Dictionary
    'cleanDateDict': Dictionary
    'ommitedValues': Dictionary
    'timeIntervals': Dictionary
    'totalElements': int
    'totalOmmited':  int
    'totalClean':    int
    """
    cleanData = clean.removeLostChips(idData, dateData, completeData, threshold)

    # Analyze data data with lost chips
    #analyze = AnalizeData()
    #analysis = analyze.analizeData(idData, dateData, completeData)
    #analyze.getTotalObservationsperDay(dateData, date)

    #cleanAnalysisi = analyze.analizeData(idData, dateData, completeData)

    """dates = dateData.keys()
    dates.sort()

    introDict = {
        'numDays':len(dateData),
        'firstDay': dates[0],
        'lastDay': dates[-1],
        'totalRegisters': analyze.getTotalObservations(dateData),
        'totalChips': len(idData.keys()),
        'non-empty': str(len(dateData)),
        'empty-files': str(noFiles - len(dateData)),
        'ObsPerDay': analysis['ObsPerDay'],
        'lifeCycle':analysis['lifeCycle'],
        'differentBeesPerDay': analysis['differentBeesPerDay'],
        'continuousBehavior': analysis['continuousBehavior'],
        'continuousBees': analysis['continuousBees']
    }
    cleanDict = {

        'totalElements': cleanData['totalElements'],
        'totalOmmited': cleanData['totalOmmited'],
        'totalClean': cleanData['totalClean']
    }


    # Generate Latex Report
    report = GenerateReport()
    report.generateReport(introDict, 'intro')
    report.generateReport(cleanDict, 'clean')
    """


    # FIXME: Store all the registers in the DB
    # Connect and store values to the DB
    #con = mysqlConnect()
    #con.insertData()

if __name__ == "__main__":
    main()