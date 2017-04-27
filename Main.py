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

    # FIXME:This plot have to be in other class
    plot = Plot()
    #plot.pieChart(files, "chartNumLectures", "Relation: Active VS Non-active Days")


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


    # Analyze unclean data
    analyze = AnalizeData()
    uncleanAnalysis = analyze.analizeData(idData, dateData, completeData, "Unclean")
    cleanAnalysis = analyze.analizeData(cleanData['cleanIdDict'], cleanData['cleanDateDict'], cleanData['cleanCompleteDict'], "Clean")

    dates = dateData.keys()
    dates.sort()

    introDict = {
        'numDays':len(dateData),
        'firstDay': dates[0],
        'lastDay': dates[-1],
        'totalRegisters': analyze.getTotalObservations(dateData),
        'totalChips': len(idData.keys()),
        'non-empty': str(len(dateData)),
        'empty-files': str(noFiles - len(dateData)),
        'ObsPerDay': uncleanAnalysis['ObsPerDay'],
        'lifeCycle':uncleanAnalysis['lifeCycle'],
        'differentBeesPerDay': uncleanAnalysis['differentBeesPerDay'],
        'continuousBehavior': uncleanAnalysis['continuousBehavior'],
        'continuousBees': uncleanAnalysis['continuousBees'],
        'averageTotalActivity': uncleanAnalysis['averageTotalActivity']
    }

    """cleanDict = {

        'totalElements': cleanData['totalElements'],
        'totalOmmited': cleanData['totalOmmited'],
        'totalClean': cleanData['totalClean'],
        'ommitedValues': cleanData['ommitedValues'],
        'timeIntervals': cleanData['timeIntervals'],
        'totalElements': cleanData['totalElements'],
        'totalOmmited': cleanData['totalOmmited'],
        'totalClean': cleanData['totalClean']
    }"""

    # Generate Latex Report
    report = GenerateReport()
    #FIXME: CALL ONLY ONCE GEN REPORT AND USE AS PARAMETER INTRO DICT AND CLEAN DATA
    report.generateReport(introDict, 'introduction')
    #report.generateReport(cleanData, 'cleanData')

    # FIXME: Store all the registers in the DB
    # Connect and store values to the DB
    #con = mysqlConnect()
    #con.insertData()

if __name__ == "__main__":
    main()