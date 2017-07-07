__author__ = 'Ulises Olivares'

import os
import fnmatch
import collections
import sys
from collections import defaultdict

class ExportData:
    completePath = " "
    exportPath = " "

    def __init__(self):
        '''
        '''
        self.completePath = os.getcwd()

        # Validate the current working dir to avoid an incorrect path
        # FIXME: THIS STATIC VALIDATION IS NOT A GOOD IDEA, CHANGE IT
        projectPos = self.completePath.find('Bee-BehaviorAnalysis')
        if projectPos != -1:
            projectLength = len('Bee-BehaviorAnalysis')
            if projectPos + projectLength != len(self.completePath):  # There is nothing after the working dir
                self.completePath = self.completePath[:projectPos + projectLength]
        else:
            print " Error, the PATH: " + self.completePath + 'Does not exist'
            sys.exit(0)

        # Remove previous CSV files
        self.exportPath = self.completePath + '\\data\\output\\'
        # FIXME: THIS FUNCTION MUST BE INSTANTITED FROM THE FIRST WRITER METHOD
        self.removePreviousCSVFiles(self.exportPath)


    def removePreviousCSVFiles(self, path):
        '''
        This method removes the all the
        :param path:
        :return:
        '''
        #print "the path is" + str(path)
        files = []
        # FIXME: put a try to avoid getting warning or error if a file is open
        # Detect all the existing files
        for file in os.listdir(path):
            if fnmatch.fnmatch(file, "*.csv"):
                files.append(file)

        # Remove all the existing files to avoid mistakes
        for i in files:
            if os.path.isfile(path + i):
                os.remove(path + i)

    def exportRegistersInformationUnclean(self, registers, weeklyRegisters, detailedActivity, installation, fileName, completeData):
        '''

        :param registers:
        :param weeklyRegisters:
        :param detailedActivity:
        :return:
        '''

        min = {}  # this a variable to extract the minimum element of a list of weeks

        registerPerDay = {}
        for i in completeData:
            registerPerDay[i] = defaultdict(list)
            for j in completeData[i]:
                for k in completeData[i][j]:
                    if k in registerPerDay[i].keys():
                        registerPerDay[i][k] = registerPerDay[i][k] + len(completeData[i][j][k])
                    else:
                        registerPerDay[i][k] =  len(completeData[i][j][k])


        f = open(self.exportPath + str(fileName) + ' Registers'  +'.csv', "wb")

        # Write the information related to registers per site
        f.write("Site,Total No. of registers\n")
        for r in registers:
            f.write(r + ',' + str(registers[r]) + '\n')

        # Add a break line as a separation
        f.write('\n')

        for i in registerPerDay:
            f.write(i + '\n')
            f.write('Day, No. Registers \n')
            regList = registerPerDay[i].keys()
            regList.sort()
            for j in regList:
                f.write(str(j) + ',' + str(registerPerDay[i][j]) + '\n')


        # Add a break line as a separation
        f.write('\n')
        weekCount = 0

        for i in weeklyRegisters:
            # Get the first natural week of measurements
            weekList = weeklyRegisters[i].keys()
            weekList.sort()
            # Store the min element
            min[i] = weekList[0]

            f.write(i + '\n')
            f.write("Week, No. of registers\n")
            weekCount = 1
            for j in weeklyRegisters[i]:
                f.write('Week ' + str(weekCount) + ',' + str(weeklyRegisters[i][j]) + '\n')
                weekCount = weekCount + 1
            f.write('\n')

        f.write('\n')

        for i in detailedActivity:
            # Make the tittle
            f.write(i + '\n')
            f.write("Bee,")
            for r in range(1,weekCount):
                f.write("Week " + str(r) + ",")
            f.write("Installation Date\n")
            for j in detailedActivity[i]:
                lastElement = 1
                f.write(str(j) + ',')
                commaCount = 0
                for k in detailedActivity[i][j]:
                    for m in range(lastElement, (k % min[i]) + 1):
                        f.write(',')
                        commaCount = commaCount + 1
                    f.write(str(detailedActivity[i][j][k]) )
                    lastElement = (k % min[i]) + 1

                if commaCount < weekCount:
                    for w in range((weekCount - commaCount)-1):
                        f.write(',')

                # Write installation day information
                if j in installation[i].keys():
                    week = (installation[i][j].isocalendar()[1] % min[i]) + 1
                    f.write('Week ' + str(week))


                else:
                    f.write('foreign bee')
                f.write('\n')

        f.close()

    def exportRegistersInformationClean(self, registers, weeklyRegisters, detailedActivity, installation, fileName, min, weekC, completeData):
        '''

        :param registers:
        :param weeklyRegisters:
        :param detailedActivity:
        :return:
        '''

        registerPerDay = {}
        for i in completeData:
            registerPerDay[i] = defaultdict(list)
            for j in completeData[i]:
                for k in completeData[i][j]:
                    if k in registerPerDay[i].keys():
                        registerPerDay[i][k] = registerPerDay[i][k] + len(completeData[i][j][k])
                    else:
                        registerPerDay[i][k] = len(completeData[i][j][k])

        f = open(self.exportPath + str(fileName) + ' Registers'  +'.csv', "wb")

        # Write the information related to registers per site
        f.write("Site,Total No. of registers\n")
        for r in registers:
            f.write(r + ',' + str(registers[r]) + '\n')

        # Add a break line as a separation
        f.write('\n')
        weekCount = 0

        for i in weeklyRegisters:
            # Get the first natural week of measurements


            f.write(i + '\n')
            f.write("Week, No. of registers\n")
            weekCount = 1
            for j in weeklyRegisters[i]:
                f.write('Week ' + str(weekCount) + ',' + str(weeklyRegisters[i][j]) + '\n')
                weekCount = weekCount + 1
            f.write('\n')

        f.write('\n')
        weekCount = weekC

        for i in detailedActivity:
            # Make the tittle
            f.write(i + '\n')
            f.write("Bee,")
            for r in range(1,weekCount):
                f.write("Week " + str(r) + ",")
            f.write("Installation Date\n")
            for j in detailedActivity[i]:
                lastElement = 1
                f.write(str(j) + ',')
                commaCount = 0
                for k in detailedActivity[i][j]:
                    for m in range(lastElement, (k % min[i]) + 1):
                        f.write(',')
                        commaCount = commaCount + 1
                    f.write(str(detailedActivity[i][j][k]) )
                    lastElement = (k % min[i]) + 1

                if commaCount < weekCount:
                    for w in range((weekCount - commaCount)-1):
                        f.write(',')

                # Write installation day information
                if j in installation[i].keys():
                    week = (installation[i][j].isocalendar()[1] % min[i]) + 1
                    f.write('Week ' + str(week))


                else:
                    f.write('foreign bee')
                f.write('\n')

        f.close()



    def exportBeeInformationUnclean(self, bees, weeklyActivityBees, detailedActivity, installation, fileName, completeData):
        '''

        :param bees:
        :param weeklyActivityBees:
        :param registers:
        :param weeklyActivityRegisters:
        :return:
        '''
        min ={} # this a variable to extract the minimum element of a list of weeks
        beesPerDay = {}

        # Store all the registers per day
        for i in completeData:
            beesPerDay[i] = defaultdict(list)
            for j in completeData[i]:
                for k in completeData[i][j]:
                    beesPerDay[i][k].append(j)

        f = open(self.exportPath + str(fileName) + ' Bees' + '.csv', "wb")

        # Write the information related to bees per site
        f.write("Site,Total No. of Bees\n")
        for l in bees:
            f.write(l + ',' + str(bees[l]) + '\n')


        # Add a break line as a separation
        f.write('\n')

        # Activity per day
        for i in beesPerDay:
            f.write(i + '\n')
            f.write('Day, No. of Bees' + '\n')
            dayList = beesPerDay[i].keys()
            dayList.sort()
            for j in dayList:
                f.write(str(j) + ',' + str(len(beesPerDay[i][j])) + '\n')

        # Add a break line as a separation
        f.write('\n')

        weekCount = 0
        #f.write('Weekly activity of bees\n')

        for i in weeklyActivityBees:
            # Get the first natural week of measurements
            weekList = weeklyActivityBees[i].keys()
            weekList.sort()
            # Store the min element
            min[i] = weekList[0]

            f.write(i + '\n')
            f.write("Week, No. of bees" +'\n')
            weekCount = 1
            for j in weeklyActivityBees[i]:
                f.write('Week ' + str(weekCount) + ','  + str(weeklyActivityBees[i][j]) + '\n')
                weekCount = weekCount + 1
            f.write('\n')

        f.write('\n')

        for i in detailedActivity:
            # Make the tittle
            f.write(i + '\n')
            f.write("Bee,")
            for r in range(1,weekCount):
                f.write("Week " + str(r) + ",")
            f.write("Installation Date\n")
            for j in detailedActivity[i]:
                lastElement = 1
                f.write(str(j) + ',')
                commaCount = 0
                for k in detailedActivity[i][j]:
                    week = (k % min[i]) + 1
                    for m in range(lastElement, week):
                        f.write(',')
                        commaCount = commaCount + 1
                    f.write(str(detailedActivity[i][j][k]) )
                    lastElement = week

                if commaCount < weekCount:
                    for w in range((weekCount - commaCount)-1):
                        f.write(',')

                # Write installation day information
                if j in installation[i].keys():

                    week = (installation[i][j].isocalendar()[1] % min[i]) + 1
                    if week > 4:
                        print 'error'
                        print installation[i][j]
                        print installation[i][j].isocalendar()[1]

                    f.write('Week ' + str(week))


                else:
                    f.write('foreign bee')
                f.write('\n')
        f.close()
        return min, weekCount

    def exportBeeInformationClean(self, bees, weeklyActivityBees, detailedActivity, installation, fileName, min, weekC, completeData):
        '''

        :param bees:
        :param weeklyActivityBees:
        :param registers:
        :param weeklyActivityRegisters:
        :return:
        '''

        beesPerDay = {}
        # Store all the registers per day
        for i in completeData:
            beesPerDay[i] = defaultdict(list)
            for j in completeData[i]:
                for k in completeData[i][j]:
                    beesPerDay[i][k].append(j)



        f = open(self.exportPath + str(fileName) + ' Bees' +'.csv', "wb")

        # Write the information related to bees per site
        f.write("Site,Total No. of Bees\n")
        for l in bees:
            f.write(l + ',' + str(bees[l]) + '\n')

        # Add a break line as a separation
        f.write('\n')

        # Activity per day
        for i in beesPerDay:
            f.write(i + '\n')
            f.write('Day, No. of Bees' + '\n')
            dayList = beesPerDay[i].keys()
            dayList.sort()
            for j in dayList:
                f.write(str(j) + ',' + str(len(beesPerDay[i][j])) + '\n')

        # Add a break line as a separation
        f.write('\n')
        weekCount = 0
        #f.write('Weekly activity of bees\n')

        for i in weeklyActivityBees:

            f.write(i + '\n')
            f.write("Week, No. of bees\n")
            weekCount = 1
            for j in weeklyActivityBees[i]:
                f.write('Week ' + str(weekCount) + ','  + str(weeklyActivityBees[i][j]) + '\n')
                weekCount = weekCount + 1
            f.write('\n')

        weekCount = weekC

        f.write('\n')

        for i in detailedActivity:
            # Make the tittle
            f.write(i + '\n')
            f.write("Bee,")
            for r in range(1,weekCount):
                f.write("Week " + str(r) + ",")
            f.write("Installation Date\n")
            for j in detailedActivity[i]:
                lastElement = 1
                f.write(str(j) + ',')
                commaCount = 0
                for k in detailedActivity[i][j]:
                    week = (k % min[i]) + 1
                    for m in range(lastElement, week):
                        f.write(',')
                        commaCount = commaCount + 1
                    f.write(str(detailedActivity[i][j][k]) )
                    lastElement = week

                if commaCount < weekCount:
                    for w in range((weekCount - commaCount)-1):
                        f.write(',')

                # Write installation day information
                if j in installation[i].keys():

                    week = (installation[i][j].isocalendar()[1] % min[i]) + 1
                    if week > 4:
                        print 'error'
                        print installation[i][j]
                        print installation[i][j].isocalendar()[1]

                    f.write('Week ' + str(week))


                else:
                    f.write('foreign bee')
                f.write('\n')
        f.close()

    def exportDuration(self, uncleanDuration, fileName):
        '''

        :param uncleanDuration:
        :return:
        '''
        f = open(self.exportPath + fileName + '.csv', "wb")

        for i in uncleanDuration:
            f.write('\n\n' + i + '\n')
            for j in uncleanDuration[i]:
                #FIXME: AVOID PUT EMPTY VALUES
                if len(uncleanDuration[i][j]) > 1:
                    f.write( str(j) + '\n')
                    for k in uncleanDuration[i][j]:
                        f.write(' ,' + str(k) + '\n  ,' )
                        for l in uncleanDuration[i][j][k]:
                            f.write(str(l) + ',')
                        f.write('\n')
        f.close()

    def exportLastRegisters(self, lastRegisters):
        '''

        :param lastRegisters:
        :return:
        '''
        f = open(self.exportPath  + 'LastRegisters.csv', "wb")

        for i in lastRegisters:
            f.write(i + '\n')
            f.write('ID, Date, Time \n')
            for j in lastRegisters[i]:
                f.write(str(i) +  )
            f.write('\n')





