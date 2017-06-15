__author__ = 'Ulises Olivares'

import csv
import os
import fnmatch

class ExportData:

    def __init__(self):
        '''
         initialize constructor
        '''
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

    def exportWeeklyBeeActivity(self, bees, weeklyActivityBees, registers, weeklyActivityRegisters):
        '''

        :param bees:
        :param weeklyActivityBees:
        :param registers:
        :param weeklyActivityRegisters:
        :return:
        '''
        completePath = os.getcwd()

        # Validate the current working dir to avoid an incorrect path
        # FIXME: THIS STATIC VALIDATION IS NOT A GOOD IDEA, CHANGE IT
        projectPos = completePath.find('Bee-BehaviorAnalysis')
        if  projectPos!= -1:
            projectLength = len('Bee-BehaviorAnalysis')
            if projectPos + projectLength != len (completePath): # There is nothing after the working dir
                completePath = completePath[:projectPos + projectLength]
        else:
            print " Error, the PATH: " + completePath + 'Does not exist'

        # Remove previous CSV files
        exportPath = completePath + '\\data\\output\\'
        # FIXME: THIS FUNCTION MUST BE INSTANTITED FROM THE FIRST WRITER METHOD
        self.removePreviousCSVFiles(exportPath)

        f = open(exportPath + 'Bees and Registers.csv', "wb")

        # Write the information related to bees per site
        f.write("Site,Number of Bees\n")
        for l in bees:
            f.write(l + ',' + str(bees[l]) + '\n')

        # Add a break line as a separation
        f.write('\n')

        #f.write('Weekly activity of bees\n')
        for i in weeklyActivityBees:
            f.write(i + '\n')
            f.write("Week, No. of bees\n")
            count = 1
            for j in weeklyActivityBees[i]:
                f.write('Week ' + str(count) + ','  + str(weeklyActivityBees[i][j]) + '\n')
                count = count + 1
            f.write('\n')

        f.write('\n')

        # Write the information related to registers per site
        f.write("Site,Number of registers\n")
        for r in registers:
            f.write(r + ',' + str(registers[r]) + '\n')

        # Add a break line as a separation
        f.write('\n')

        for i in weeklyActivityRegisters:
            f.write(i + '\n')
            f.write("Week, No. of registers\n")
            count = 1
            for j in weeklyActivityRegisters[i]:
                f.write('Week ' + str(count) + ','  + str(weeklyActivityRegisters[i][j]) + '\n')
                count = count + 1
            f.write('\n')


        ## Python will convert \n to os.linesep
        f.close()

        '''with open( exportPath + 'ID and Registers.csv', "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=' ')
            for l in bees:
                writer.writerow(l)'''

        '''output = open( exportPath + 'ID and Registers.csv', "wb")
        writer = csv.writer(output)

        writer.writerow('site, Number of Bees')
        for i in bees:
            writer.writerow(i)

        output.close()'''

