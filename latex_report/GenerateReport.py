import numpy as np
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, Plot, Figure, Matrix, LongTabu
from pylatex.utils import italic
import os
import subprocess
import fnmatch
import collections

class GenerateReport:


    doc = Document()

    def __init__(self):
        """
        """
    def addActivity(self, doc):
        """

        :return:
        """
        # --------------------------------------------------------------------------------------------
        #                                        Activity per Day
        # --------------------------------------------------------------------------------------------

    def addIntroduction(self, doc, sectionTitle, introDict):
        """
        Push all the content for a given file
        :param doc:
        :return:
        """

        # --------------------------------------------------------------------------------------------
        #                                        INTRODUCTION
        # --------------------------------------------------------------------------------------------
        with doc.create(Section(sectionTitle)):
            doc.append("The main propose of this document  is to show a concise report about the activity of bees "
                       "and behavior in a specific period of time. This report also shows a complete analysis of "
                       "the most active hours."
                       "\n\n"
                       "Tis report corresponds to a period of time of {} day(s). From {} to {}. "
                       "During this period of time, a total amount of {} lectures were registered from {} "
                       "different bees. There exist a total of {} non-active days. We define an 'active day' "
                       "if there is more than one observation. "
                       "(see Figure1.1)."
                       "\n\n"
                       ""
                       .format(introDict['numDays'], introDict['firstDay'],
                               introDict['lastDay'], introDict['totalRegisters'],
                               introDict['totalChips'], introDict['empty-files']))

            with doc.create(Figure(position='h!')) as fig:
                    fig.add_image("chartNumLectures.png", width='315px')
                    fig.add_caption('Days with and without Empty Reads')

        # --------------------------------------------------------------------------------------------
        #                                        Activity per Day
        # --------------------------------------------------------------------------------------------
        with doc.create(Subsection("Activity per day")):
            doc.append("This section addresses the analysis of the activity per day")

            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("observationsPerday.png", width='400px')
                fig.add_caption('Number of Observations per Day')
                # doc.append("Begin a new pharagraph")

            with doc.create(LongTabu('| c | c | c | c |')) as table:
                table.add_hline()

                obsPerDay = collections.OrderedDict(sorted(introDict['ObsPerDay'].items()))
                beesPerDay = collections.OrderedDict(sorted(introDict['differentBeesPerDay'].items()))
                #print beesPerDay


                table.add_row("Day", "Date","# Observations", "# Bees per day")
                table.add_hline()
                sum = 0
                sum2 = 0
                count = 1
                for i in  obsPerDay:
                    table.add_row(count, i, obsPerDay[i], len(beesPerDay[i]))
                    table.add_hline()
                    sum2 = sum2 + len(beesPerDay[i])
                    sum = sum + obsPerDay[i]
                    count = count + 1
                table.add_hline()
                # Write the average
                table.add_row("--", "Average" , sum/len(obsPerDay.values()) , sum2/len(beesPerDay.values()))
                table.add_hline()
                table.add_hline()

        # --------------------------------------------------------------------------------------------
        #                                        Activity per Day
        # --------------------------------------------------------------------------------------------
        with doc.create(Subsection("Bee Life Cycle")):
            doc.append("In this section is analyzed the Life Cycle of each bee in the hive")
            with doc.create(LongTabu('| c | c | c |')) as table2:
                lifeCycle = collections.OrderedDict(sorted(introDict['lifeCycle'].items()))
                table2.add_hline()
                table2.add_hline()
                table2.add_row("Register", "Bee ID","Life Cycle in Days")
                table2.add_hline()
                table2.add_hline()
                sum = 0
                count = 1
                for i in  lifeCycle:
                    table2.add_row(count, i[-4:], lifeCycle[i])
                    table2.add_hline()
                    sum = sum + lifeCycle[i]
                    count = count + 1
                table2.add_hline()
                # Write the average
                table2.add_row("--","Average" , sum/len(lifeCycle.values()))
                table2.add_hline()
                table2.add_hline()

            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("differentBeesPerday.png", width='400px')
                fig.add_caption('Different Bees Per Day')

            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("beeLifeCycle.png", width='400px')
                fig.add_caption('Bee Life cycle in days')


            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("pieBeeLifeCycle.png", width='400px')
                fig.add_caption('Bee Life cycle in days')
                # doc.append("Begin a new pharagraph")

        # --------------------------------------------------------------------------------------------
        #                                        Activity per Hour
        # --------------------------------------------------------------------------------------------
        with doc.create(Subsection("Analysis of Activity per Hour")):
            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("histogram.png", width='400px')
                fig.add_caption('Histogram of frequencies per hour')

            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("histogramStd.png", width='400px')
                fig.add_caption('Histogram of frequencies per hour. It includes standard deviation')





        return doc.dumps_content()

    def removePreviousFiles(self, path):
        """
        This method removes the all the
        :param path:
        :return:
        """
        files = []
        # FIXME: put a try to avoid getting warning or errer if a file is open
        # Detect all the existing files
        for file in os.listdir(path):
            if fnmatch.fnmatch(file, "Latex Report.*"):
                files.append(file)

        # Remove all the existing files to avoid mistakes
        for i in files:
            if os.path.isfile(path + i):
                os.remove(path + i)


    def generatePDF(self, path):
        """
        Generates the pdf from a .tex file compile and build three times
        :param path:
        :return:
        """
        os.chdir(path)
        # Compile three times the .tex file
        output = ''
        error = ''
        for i in range(3):
            devnull = open(os.devnull, 'wb')
            #proc = subprocess.Popen(['pdflatex', 'Latex Report.tex'], shell=False,
            #                        stdout=subprocess.PIPE, stderr=devnull)
            proc = subprocess.Popen(['pdflatex', 'Latex Report.tex'])
            #output, error = proc.communicate()
            proc.communicate()
        if os.path.isfile(path + "Latex Report.pdf") and error != 'None':
            print "PDF Report generated Correctly"
        else:
            "There was an error during PDF report Generation please check the log file"
            print output

    def readTemplate(self, templateFile):
        """
        Reads the template file and return a buffer with all the information
        :param templateFile: Path of the template
        :return buffer:
        """
        with open(templateFile, 'r') as inFile:
            buffer = inFile.readlines()
        return buffer

    def addContent(self, texFile, contents, doc, buffer):
        """
        This Function takes an input list and add its contents to a tex file
        :param texFile: Path of the tex file
        :param contents: List that has all the information
        :param doc: Documment
        :param buffer: Buffer of the template
        :return: None
        """
        with open(texFile, 'w') as outFile:
            for line in buffer:
                if (line.find("%INSERT_CONTENT_HERE")!= -1):
                    # Add all the content form the contents list
                    for i in contents:
                        line = line + i
                outFile.write(line)


    def generateReport(self, introDict):
        """
        Principal function to add content to the .tex file
        :return: None
        """

        geometry_options = {
            "landscape": False,
            "margin": "5.5in",
            "headheight": "20pt",
            "headsep": "10pt",
            "includeheadfoot": False
        }
        # Variable definition
        doc = Document(geometry_options=geometry_options)
        workingDir = os.getcwd()
        path = workingDir + '\latex_report\latex_template\\'
        template = path + "Template.tex"
        texFile = path + "Latex Report.tex"
        contents = []

        # Removes previous generated files
        self.removePreviousFiles(path)

        # Reads the template and store it in a buffer
        buffer = self.readTemplate(template)

        # Add an introductory section
        contents.append(self.addIntroduction(doc, "Introduction", introDict))

        #print contents



        # Add content to the file
        self.addContent(texFile, contents, doc, buffer)

        # Generate the PDF file using pdf_latex
        self.generatePDF(path)
