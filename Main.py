#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ulises Olivares'

from analyze_data.AnalizeData import AnalizeData
from import_data.ImportData import ImportData
from latex_report.GenerateReport import GenerateReport
from plots.Plot import Plot
from clean_data.CleanData import CleanData

from datetime import datetime, timedelta
import time


# Data folder
data = "data/"

def sortDates(dates):
    """
    This method sorts an input array
    :param dates:
    :return:
    """
    return sorted(dates)
    

def main():
    # ------------------------
    # Object declaration
    # ------------------------
    imp = ImportData()          # Import data
    plot = Plot()               # Plot data
    clean = CleanData()         # Clean data
    analyze = AnalizeData()     # Analyze unclean data
    report = GenerateReport()   # Generate report of analyzed data


    #------------------------
    #Variable declaration
    #------------------------
    FMT = '%H:%M:%S'
    thresholdLostChips = datetime.strptime("00:01:00", FMT)
    thresholdLostChips = timedelta(hours=thresholdLostChips.hour, minutes=thresholdLostChips.minute,
                                   seconds=thresholdLostChips.second)
    thresholdForaging = datetime.strptime("00:20:00", FMT)
    thresholdForaging = timedelta(hours=thresholdForaging.hour, minutes=thresholdForaging.minute,
                                   seconds=thresholdForaging.second)
    cleanDataDict = {}
    uncleanAnalysis = {}
    cleanAnalysis = {}
    cleanDict = {}
    uncleanDict = {}
    reportContent = {}     # Contains the latex document in a str format

    # TODO:  pass by reference all the parameters implement this to reduce the memory footprint
    start = time.time()
    noFiles = imp.importInputData(data)

    end = time.time()
    delta = end - start
    print("Time Lapse of importation: " + str(delta))

    if len(noFiles) < 1:
        print ("There are not input Files, Please be sure that your input files are in the data Directory...")
        exit(0)

    #Get data
    #idData, dateData, completeData = imp.getIdDictionary()
    #dateData = imp.getDateDictionaary()

    # Obtain data from CSV Files
    idData, dateData, completeData, installationDates= imp.getCompleteDictionary()

    activity = {}

    # Iteration for analyzing all the input data of independent sites
    sites = []
    for i in completeData:
        sites.append(i)
        print ("---------------------------------")
        print ("Site Name: " + i)
        print ("---------------------------------")

        print ("Number of files: " + str(noFiles[i]))
        print ("Active Days: " + str(len(dateData[i])))
        print ("Non-Active Days: " + str(noFiles[i] - len(dateData[i])))

        # Store values of activity for each site
        activity[i] = {}
        activity[i]['Active Days'] = len(dateData[i])
        activity[i]['Non-Active Days'] = noFiles[i] - len(dateData[i])

        # TODO:This plot has to be in other class
        chartName=  i + "-chartNumLectures"
        plot.pieChart(activity[i], chartName, "Relation: Active VS Non-active Days: " + i)

        print ("---------------------------------")
        print("Cleaning data...\n" + "Threshold: " + str(thresholdLostChips))

        # sorting all dates to select 1st and last date and make a difference
        sortedDates = sortDates(dateData[i].keys())

        cleanDataDict[i] = clean.removeLostChips( completeData[i], thresholdLostChips)

        # Perform an analysis of clean data
        cleanAnalysis[i] = analyze.analizeSingleSite(cleanDataDict[i]['cleanIdDict'], cleanDataDict[i]['cleanDateDict'],
                                               cleanDataDict[i]['cleanCompleteDict'], "Clean", i)
        cleanDict[i] = {}
        cleanDict[i] = {
            'thresholdLostChips': thresholdLostChips,
            'totalElements': cleanDataDict[i]['totalElements'],
            'totalOmmited': cleanDataDict[i]['totalOmmited'],
            'totalClean': cleanDataDict[i]['totalClean'],
            'ommitedValues': cleanDataDict[i]['ommitedValues'],
            'timeIntervals': cleanDataDict[i]['timeIntervals'],
            'totalElements': cleanDataDict[i]['totalElements'],
            'totalOmmited': cleanDataDict[i]['totalOmmited'],
            'totalClean': cleanDataDict[i]['totalClean'],
            'ObsPerDay': cleanAnalysis[i]['ObsPerDay'],
            'lifeCycle': cleanAnalysis[i]['lifeCycle'],
            'differentBeesPerDay': cleanAnalysis[i]['differentBeesPerDay'],
            'continuousBehavior': cleanAnalysis[i]['continuousBehavior'],
            'continuousBees': cleanAnalysis[i]['continuousBees'],
            'averageTotalActivity': cleanAnalysis[i]['averageTotalActivity']
        }

        print("Cleaning data process finished..\n" )




        # Performs an analysis of unclean data
        uncleanAnalysis[i] = analyze.analizeSingleSite(idData[i], dateData[i], completeData[i], "Unclean", i)
        #TODO: CHECK THE TWO DICTIONARIES AND SELECT ANOTHER WAY TO STORE DATA WITHOUT MAKING THIS PART HUGE
        uncleanDict[i] = {}
        uncleanDict[i] = {
            'numDays': len(dateData[i].keys()),
            'firstDay': sortedDates[0],
            'lastDay': sortedDates[-1],
            'totalRegisters': analyze.getTotalObservations(dateData[i]),
            'totalChips': len(idData[i].keys()),
            'non-empty': str(len(dateData[i])),
            'empty-files': str(noFiles[i]- len(dateData[i])),
            'ObsPerDay': uncleanAnalysis[i]['ObsPerDay'],
            'lifeCycle': uncleanAnalysis[i]['lifeCycle'],
            'differentBeesPerDay': uncleanAnalysis[i]['differentBeesPerDay'],
            'continuousBehavior': uncleanAnalysis[i]['continuousBehavior'],
            'continuousBees': uncleanAnalysis[i]['continuousBees'],
            'averageTotalActivity': uncleanAnalysis[i]['averageTotalActivity']
        }

        #FIXME: PASS ALL THE PARAMETERS IN ORDER TO GENERATE THE REPORT CORRECTLY
        # Generate Latex Report
        #TODO: WITH THIS APPROACH ALL THE INFORMATION IS OVERWRITTEN CORRECT IT.
        reportContent[i] = report.generateLatexContent(uncleanDict[i], cleanDict[i], i)


    # Analysis of all sites as a result several CSV files are generated.
    analyze.analizeAllSites(completeData, installationDates)


    # Generate the .tex file
    report.generateReport(reportContent)


if __name__ == "__main__":
    main()