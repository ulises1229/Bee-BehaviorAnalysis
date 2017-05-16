import numpy as np
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, Plot, Figure, Matrix, LongTabu
import os
import subprocess
import fnmatch
import collections
from datetime import datetime, timedelta

class GenerateReport:


    doc = Document()


    def __init__(self):
        """
        """
    def addActivityUncleanData(self, doc, introDict):
        # --------------------------------------------------------------------------------------------
        #                                        Activity per Day
        # --------------------------------------------------------------------------------------------
        with doc.create(Subsection("Activity Per Day of Raw Data")):
            doc.append("This section addresses the analysis of raw data. Which implies that this date is presented "
                       "without filters or a data preprocessing step to clean the data. This section presents several"
                       "graphs which reflects the behavior of a beehive during a specific period of time.")

            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("observationsPerdayUnclean.png", width='400px')
                fig.add_caption('Number of Observations per Day')
                # doc.append("Begin a new pharagraph")

            with doc.create(LongTabu('| c | c | c | c |')) as table:
                table.add_hline()

                obsPerDay = collections.OrderedDict(sorted(introDict['ObsPerDay'].items()))
                beesPerDay = collections.OrderedDict(sorted(introDict['differentBeesPerDay'].items()))
                # print beesPerDay


                table.add_row("Day", "Date", "# Observations", "# Bees per day")
                table.add_hline()
                sum = 0
                sum2 = 0
                count = 1
                for i in obsPerDay:
                    table.add_row(count, i, obsPerDay[i], len(beesPerDay[i]))
                    table.add_hline()
                    sum2 = sum2 + len(beesPerDay[i])
                    sum = sum + obsPerDay[i]
                    count = count + 1
                table.add_hline()
                # Write the average
                table.add_row("--", "Average", sum / len(obsPerDay.values()), sum2 / len(beesPerDay.values()))
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
                table2.add_row("Register", "Bee ID", "Life Cycle in Days")
                table2.add_hline()
                table2.add_hline()
                sum = 0
                count = 1
                for i in lifeCycle:
                    table2.add_row(count, i[-4:], lifeCycle[i])
                    table2.add_hline()
                    sum = sum + lifeCycle[i]
                    count = count + 1
                table2.add_hline()
                # Write the average
                table2.add_row("--", "Average", sum / len(lifeCycle.values()))
                table2.add_hline()
                table2.add_hline()

            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("differentBeesPerdayUnclean.png", width='400px')
                fig.add_caption('Different Bees Per Day')

            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("beeLifeCycleUnclean.png", width='400px')
                fig.add_caption('Bee Life cycle in days')

            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("pieBeeLifeCycleUnclean.png", width='400px')
                fig.add_caption('Bee Life cycle in days')
                # doc.append("Begin a new pharagraph")

        # --------------------------------------------------------------------------------------------
        #                                        Activity per Hour
        # --------------------------------------------------------------------------------------------
        with doc.create(Subsection("Analysis of Activity per Hour")):
            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("histogramUnclean.png", width='400px')
                fig.add_caption('Histogram of frequencies per hour')

            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("histogramStdUnclean.png", width='400px')
                fig.add_caption('Histogram of frequencies per hour. It includes standard deviation')
        return doc.dumps_content()

    def addActivityCleanData(self, doc, cleanDict):
        # --------------------------------------------------------------------------------------------
        #                                        Activity per Day
        # --------------------------------------------------------------------------------------------
        with doc.create(Subsection("Activity Per Day of Clean Data")):
            doc.append("In this section is presented an analysis of input data. During this analysis some filters"
                       " were applied. One of these filters is the definition of a threshold which removes all"
                       " the observations that fall in a period of time less than {} seconds. This preprocessing step tends to"
                       "  remove all the lost chips which generated unnecessary and repeated registers"
                       " ".format(cleanDict['thresholdLostChips'].seconds))

            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("observationsPerdayClean.png", width='400px')
                fig.add_caption('Number of Observations per Day')
                # doc.append("Begin a new pharagraph")

            with doc.create(LongTabu('| c | c | c | c |')) as table:
                table.add_hline()

                obsPerDay = collections.OrderedDict(sorted(cleanDict['ObsPerDay'].items()))
                beesPerDay = collections.OrderedDict(sorted(cleanDict['differentBeesPerDay'].items()))
                # print beesPerDay


                table.add_row("Day", "Date", "# Observations", "# Bees per day")
                table.add_hline()
                sum = 0
                sum2 = 0
                count = 1
                for i in obsPerDay:
                    table.add_row(count, i, obsPerDay[i], len(beesPerDay[i]))
                    table.add_hline()
                    sum2 = sum2 + len(beesPerDay[i])
                    sum = sum + obsPerDay[i]
                    count = count + 1
                table.add_hline()
                # Write the average
                table.add_row("--", "Average", sum / len(obsPerDay.values()), sum2 / len(beesPerDay.values()))
                table.add_hline()
                table.add_hline()

        # --------------------------------------------------------------------------------------------
        #                                        Activity per Day
        # --------------------------------------------------------------------------------------------
        with doc.create(Subsection("Bee Life Cycle")):

            with doc.create(LongTabu('| c | c | c |')) as table2:
                lifeCycle = collections.OrderedDict(sorted(cleanDict['lifeCycle'].items()))
                table2.add_hline()
                table2.add_hline()
                table2.add_row("Register", "Bee ID", "Life Cycle in Days")
                table2.add_hline()
                table2.add_hline()
                sum = 0
                count = 1
                for i in lifeCycle:
                    table2.add_row(count, i[-4:], lifeCycle[i])
                    table2.add_hline()
                    sum = sum + lifeCycle[i]
                    count = count + 1
                table2.add_hline()
                # Write the average
                table2.add_row("--", "Average", sum / len(lifeCycle.values()))
                table2.add_hline()
                table2.add_hline()

            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("differentBeesPerdayClean.png", width='400px')
                fig.add_caption('Different Bees Per Day')

            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("beeLifeCycleClean.png", width='400px')
                fig.add_caption('Bee Life cycle in days')

            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("pieBeeLifeCycleClean.png", width='400px')
                fig.add_caption('Bee Life cycle in days')
                # doc.append("Begin a new pharagraph")

        # --------------------------------------------------------------------------------------------
        #                                        Activity per Hour
        # --------------------------------------------------------------------------------------------
        with doc.create(Subsection("Analysis of Activity per Hour")):
            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("histogramClean.png", width='400px')
                fig.add_caption('Histogram of frequencies per hour')

            # Add Figure
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image("histogramStdClean.png", width='400px')
                fig.add_caption('Histogram of frequencies per hour. It includes standard deviation')
        return doc.dumps_content()

    def addIntroduction(self, doc, sectionTitle, introDict):
        """
        Push all the content for a given file
        :param doc:
        :return:
        """

        #print "Number of days: " + str(introDict['numDays'])

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
        return doc.dumps_content()

    def removePreviousFiles(self, path):
        """
        This method removes the all the
        :param path:
        :return:
        """
        #print "the path is" + str(path)
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
            proc = subprocess.Popen(['pdflatex', 'Latex Report.tex'], shell=False,
                                    stdout=subprocess.PIPE, stderr=devnull)
            #proc = subprocess.Popen(['pdflatex', 'Latex Report.tex'])
            output, error = proc.communicate()
            #proc.communicate()
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

    def addContent(self, texFile, contents, buffer):
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

    def generateReport(self, contents):
        """

        :param contents:
        :return:
        """
        print contents

        workingDir = os.getcwd()
        path = workingDir + '\latex_report\latex_template\\'
        if path.count("\latex_report\latex_template") > 1:
            path = path.replace('\latex_report\latex_template', '', 1)
        template = path + "Template.tex"
        texFile = path + "Latex Report.tex"

        # Append the all the content
        totalContent = ""
        for i in contents:
            for j in contents[i]:
                totalContent = totalContent + str(j)

        # Reads the template and store it in a buffer
        buffer = self.readTemplate(template)

        # Add content to the file
        self.addContent(texFile,totalContent, buffer)

        # FIXME: VERIFY THAT THE PATH CONTAINS THE FILES NECESSARY IMAGES (Pictures/ => latex image path)
        # Generate the PDF file using pdf_latex
        self.generatePDF(path)




    def generateLatexContent(self, uncleanDict, cleanDict, site):
        """
        This methods generates a PDF report for each site
        :param uncleanDict: Dictifindonary that contains all the information
        :param type: This parameter denotes
        :return:
        """
        contents = []

        workingDir = os.getcwd()
        path = workingDir + '\latex_report\latex_template\\'
        if path.count("\latex_report\latex_template") > 1:
            path = path.replace('\latex_report\latex_template', '', 1)

        geometry_options = {
            "landscape": False,
            "margin": "5.5in",
            "headheight": "20pt",
            "headsep": "10pt",
            "includeheadfoot": False
        }
        # Variable definition
        doc = Document(geometry_options=geometry_options)

        # Removes previous generated files
        self.removePreviousFiles(path)



        #FIXME: ADD A CHAPTER FOR EACH SITE

        # Add Capter 1: Introductory section
        contents.append("\part{" + str(site)+ "}\n")
        contents.append("\chapterimage{head2.jpg} % Chapter heading image \n")
        contents.append("\chapter{Introduction} \n")
        contents.append(self.addIntroduction(doc, "Introduction", uncleanDict))

        doc1 = Document(geometry_options=geometry_options)
        #Add Chapter 2 analysis of RAW data
        contents.append("\chapterimage{head3.jpg} % Chapter heading image \n")
        contents.append("\chapter{Analysis of Raw Data} \n")
        contents.append(self.addActivityUncleanData(doc1, uncleanDict))

        doc2 = Document(geometry_options=geometry_options)
        #Add chapter 3 analysis of clean data
        contents.append("\chapterimage{head4.jpg} % Chapter heading image \n")
        contents.append("\chapter{Analysis of Clean Data}\n")
        contents.append(self.addActivityCleanData(doc2, cleanDict))

        doc3 = Document(geometry_options=geometry_options)
        #Add chapter 4 foraging behavior
        contents.append("\chapterimage{head5.jpg} % Chapter heading image\n")
        contents.append("\chapter{Analysis of Foraging Behavior}\n")

        return contents

