__author__ = 'Ulises Olivares'

import csv

class ExportData:

    def __init__(self):
        """
            initialize constructor
        """
    def exportWeeklyBeeActivity(self, bees, weeklyActivityBees, registers, weeklyActivityRegisters):

        output = open('test.csv', "wb")
        writer = csv.writer(output, delimiter='', quotechar='"', quoting=csv.QUOTE_ALL)
        reader = "this is a test"
        for row in reader:
            writer.writerow(row)

        output.close()

