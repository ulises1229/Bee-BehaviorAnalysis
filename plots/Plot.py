__author__ = 'Ulises Olivares'

import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly
import numpy as np
#FIXME: READ THE USER AND THE API KEY FROM A .INI FILE
plotly.tools.set_credentials_file(username='ulises1229', api_key='IBElW0dqjDEJXCuozFGy')
import plotly.graph_objs as go
import os
from matplotlib.gridspec import GridSpec

class Plot:
    figPath = '\\latex_report\\latex_template\\Pictures\\plots\\'

    def __init__(self):
        """put code here"""

    '''def multiplePiePlot(self, input, chartName, title):
        labels = []

        for i in input:
            labels.append(i)


        # Make square figures and axes
        the_grid = GridSpec(2, 1)
        plt.subplot(the_grid[0, 0], aspect=1)

        plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)'''


    def pieChart(self, input, chartName, title):
        """
        Generates
        :param input:
        :return:
        """
        # Define a dictionary for parsing all the parameters
        fig = {
            'data': [{'labels': [],
                      'values': [],
                      'type': 'pie'}],
            'layout': {'title': ''}
        }

        # Fill the dictionary
        for i in input.keys():
            fig['data'][0]['labels'].append(i)
        for i in input.values():
            fig['data'][0]['values'].append(i)
        fig['layout']['title'] = title


        #Save the pie plot
        fileName = os.getcwd()  + self.figPath + chartName + '.png'
        #exit(0)
        py.image.save_as(fig, filename=fileName)

    def pieChartBeeLifeCycle(self, input, chartName, title):
        """
        Generates
        :param input:
        :return:
        """
        # Define a dictionary for parsing all the parameters
        tmp = {}
        for i in input.values():
            if i in tmp.keys():
                tmp[i] = tmp[i] + 1
            else:
                tmp[i] = i

        fig = {
            'data': [{'labels': [],
                      'values': [],
                      'type': 'pie'}],
            'layout': {'title': ''}
        }

        # Fill the dictionary
        for i in tmp.keys():
            if i == 1:
                suffix = " Day"
            else:
                suffix = " Days"
            fig['data'][0]['labels'].append(str(i) + suffix)
        for i in tmp.values():
            fig['data'][0]['values'].append(i)
        fig['layout']['title'] = title


        #Save the pie plot
        fileName = os.getcwd()  + self.figPath + chartName + '.png'
        #exit(0)
        py.image.save_as(fig, filename=fileName)

    def barPlot(self, inputData, title, xAxis, yAxis, chartName, type):
        """

        :param inputData: Dictionaty Date => No Obs
        :param title:
        :param xAxis:
        :param yAxis:
        :return:
        """

        inputX = inputData.keys()
        inputY = []
        if (type != 'diffBees'):
            inputY = inputData.values()

        if type == 'Obs':
            tmpX = inputX
            tmpX.sort()
            first = tmpX[0]
            last = tmpX[-1]
            xAxis = xAxis + "From {} to {}".format(first, last)

        if type == 'diffBees':
            for i in inputData:
                inputY.append(len(inputData[i]))

        # Create a listo of nums from 1 to n where n is the num of elements for plots only
        numericX =[]
        for i in range (len(inputX)):
            numericX.append(i + 1)

        data = [go.Bar(
                x = numericX,
                y = inputY
        )]

        layout = go.Layout(
                title = title,
                xaxis=dict(
                    title = xAxis,
                    titlefont=dict(
                        size=16,
                        color='rgb(107, 107, 107)'
                    ),
                    tickfont=dict(
                        size=14,
                        color='rgb(107, 107, 107)'
                    )
                ),
                yaxis=dict(
                    title = yAxis,
                    titlefont=dict(
                        size=16,
                        color='rgb(107, 107, 107)'
                    ),
                    tickfont=dict(
                        size=14,
                        color='rgb(107, 107, 107)'
                    )
                )
        )

        # Save the bar plot
        fileName = os.getcwd() + self.figPath + chartName + '.png'
        fig = go.Figure(data = data, layout=layout)
        py.image.save_as(fig, filename=fileName)

    def linePlotBeesPerDay(self, inputData, title, xAxis, yAxis, chartName):
        x = inputData.keys()
        y = inputData.values()
        fig, ax = plt.subplots()
        line1, = ax.plot(x, np.sin(x), '--', linewidth=2,label='Dashes set retroactively')


    def plotEquivalenceClass(self, inputData, title, xAxisTitle, yAxisTitle, chartName):
        """
        This method generates a histogram
        :param inputData:
        :param title:
        :param xAxisTitle:
        :param yAxisTitle:
        :param chartName:
        :return:
        """
        print (inputData)
        labels = ["label%d" % i for i in xrange(len(inputData))]
        x = range(len(inputData))
        y = inputData

        tmpX =[]
        for i in x:
            if i < 10:
                tmpX.append("0" + str(i))
            else:
                tmpX.append(str(i))
        #print tmpX
        #FIXME: DISPLAY XTICKS IN HOUR FORMAT
        plt.xticks(x, fontsize=7)
        #plt.yticks(y, fontsize=2)
        plt.bar(x , y , align='center' , color='blue', alpha=0.8)

        plt.xlabel(xAxisTitle, fontsize=11)
        plt.ylabel(yAxisTitle, fontsize=11)
        plt.title(title)

        fileName = os.getcwd() + self.figPath + chartName + ".png"
        if fileName.count("\latex_report\latex_template") > 1:
            fileName = fileName.replace('\\latex_report\\latex_template' , '', 1)

        plt.savefig(fileName, format='png', dpi=600)
        plt.close()

    def plotEquivalenceClassStd(self, inputData, title, xAxisTitle, yAxisTitle, std, chartName):

        plt.title(title)
        plt.xlabel(xAxisTitle)
        plt.ylabel(yAxisTitle)


        labels = ["label%d" % i for i in xrange(len(inputData))]
        x = range(len(inputData))
        y = inputData
        plt.xticks(x, fontsize=7)
        plt.bar(x , y , align='center' , color='blue', yerr=std, alpha=0.8)
        #plt.show()
        fileName = os.getcwd() + self.figPath + chartName + ".png"
        if fileName.count("\latex_report\latex_template") > 1:
            fileName = fileName.replace('\latex_report\latex_template' , '', 1)
        plt.savefig(fileName, format='png', dpi=600)
        plt.close()




    def barPlotCategories(self, ids, registers):
        N = 2
        ind = np.arange(N)
        width = 0.35

        site1 = []
        site2 = []

        site1.append(ids['Morelia Hive 1'])
        site1.append(ids['Morelia Hive 2'])

        site2.append(registers['Morelia Hive 1'])
        site2.append(registers['Morelia Hive 2'])

        print ("Morelia - Site 1: " + str(site1))
        print ("Morelia - Site 2: " + str(site2))

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, site1, width, color='b')
        rects2 = ax.bar(ind + width, site2, width, color='r')

        ax.set_ylabel('Observations \n log scale')
        ax.set_title('Number of Ids and Registers per Site')
        ax.set_xticks(ind + width / 2)
        ax.set_xticklabels(('Site 1', 'Site 2'))
        ax.set_yscale('log')

        ax.legend((rects1, rects2), ('Ids', 'Registers'))

        for rect in rects1:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')

        for rect in rects2:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')

        #plt.show()

        fileName = os.getcwd() + self.figPath + "Registers_IDs" + ".png"
        if fileName.count("\latex_report\latex_template") > 1:
            fileName = fileName.replace('\latex_report\latex_template', '', 1)
        plt.savefig(fileName, format='png', dpi=600)
        plt.close()



    def barplotDictionary(self, inputData, title, xAxisTitle, yAxisTitle ):

        dictionary = plt.figure()
        list = []
        for i in inputData:
            list.append(str(i))
        list.sort()

        # Set tittle of the graph
        plt.title(title)
        plt.xlabel("Observed Days \nFrom: " + str(list[0]) + " to: " + str(list[len(list)-1]) + "\n " + str(len(list)) + " Days" )
        plt.ylabel("Number of Observations")


        plt.bar(range(len(inputData)), inputData.values(), align='center')
        if (len(list) < 60):
            plt.xticks(range(len(inputData)), range(1,len(inputData)+1))


        plt.savefig("test.png", format='png', figsize=(20.7, 1.3), dpi=1200)
        plt.show()
        #py.plot(dictionary, filename='mpl-dictionary')

