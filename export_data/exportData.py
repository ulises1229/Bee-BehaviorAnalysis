__author__ = 'Ulises Olivares'

import csv
import os

class ExportData:

    def __init__(self):
        """
            initialize constructor
        """
    def exportWeeklyBeeActivity(self, bees, weeklyActivityBees, registers, weeklyActivityRegisters):
        '''

        :param bees:
        :param weeklyActivityBees:
        :param registers:
        :param weeklyActivityRegisters:
        :return:
        '''
        completePath = os.getcwd()

        # Variables for printing errors
        #CRED = '\033[91m'
        #CEND = '\033[0m'

        # Validate the current working dir to avoid an incorrect path
        # FIXME: THIS STATIC VALIDATION IS NOT A GOOD IDEA, CHANGE IT
        projectPos = completePath.find('Bee-BehaviorAnalysis')
        if  projectPos!= -1:
            projectLength = len('Bee-BehaviorAnalysis')
            if projectPos + projectLength != len (completePath): # There is nothing after the working dir
                completePath = completePath[:projectPos + projectLength]

            output = open('test.csv', "wb")
            writer = csv.writer(output, delimiter=',')
            reader = "this is a test" ,"hello"
            for row in reader:
                writer.writerow(row)
            output.close()
        else:
            print " Error: "
