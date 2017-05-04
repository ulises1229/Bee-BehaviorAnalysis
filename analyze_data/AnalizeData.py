__author__ = 'Ulises Olivares'

from plots.Plot import Plot
import numpy as np
import datetime
import itertools
from datetime import datetime as dt
from collections import defaultdict
import collections

start = []
end = []
observationsPerDay = ''
class AnalizeData:

    def __init__(self):
        """Initializa code here"""

    def getTotalObservations(self, dateDict):
        total = 0
        for i in dateDict.values():
            total = total + len(i)
        return total

    def getObservations(self, dateDictionary, date):
        return len(dateDictionary[date])


    def observationsPerDay(self, idDict, dateDict):
        """
        This method returns the total ammount of the observations per day
        :param idDict:
        :param dateDict:
        :return:
        """
        observations = {}
        for i in dateDict:
            observations[i] = len(dateDict[i])
        return observations

    # This method returns the total time interval for a day takes the last - frist element in a sorted list
    def getTimeInterval(self, list):
        return list[len(list)-1] - list[0]

    # returns a range of time from the fisrt to the last register
    def activityPerDay(self, dateDictionary):
        difference = []
        for i in dateDictionary:
            list = []
            for k in range (len(dateDictionary[i])):
                list.append(dateDictionary[i][k])
            list.sort()
            start.append(list[0])
            end.append(list[len(list)-1])
            difference.append(datetime.datetime.combine(i ,list[-1]) - datetime.datetime.combine(i ,list[0]))

            #print str(list[0].hour) + " " + str(list[0].minute) + " " + str(list[0].second)
        #print difference
        return difference

    # This method returns the average of total activity per day
    def averageTotalActivity(self, timeInterval):
        sum = datetime.timedelta(0, 0)
        for i in timeInterval:
            sum = sum + i
        #print "Average: " + str(sum / len(timeInterval))
        return sum / len(timeInterval)

    """
     This method returns a list where the first, second and third elements are hours, minutes and seconds
     Input: timedate.timedelta
     Output: list[hours, minutes, seconds]
    """
    def extractTime(self, timeDelta):
        list = []
        hours, remainder = divmod(timeDelta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        list.append(hours)
        list.append(minutes)
        list.append(seconds)
        return list

    """
    """
    def combineDateTime(self, date, time):
        return datetime.datetime.combine(date, time)

    """
         This method analyzes all the activity and divides the space in 24 buckets = hours per day and make a
         frequency analysis for performing a frequency analysis
         Input:
            ObservationsPerDay = Dictionary date, number of observations per day
         Output:
            DateDic = Dictionary date, time in datetime format

    """
    def getActivityPerHour(self, observationsPerDay, dateDic ):
        totalActivity = {}
        for i in observationsPerDay:
            # Fill a list with 0s 24 elements
            activity = [0] * 24
            for j in range(observationsPerDay[i]):
                pos = dateDic[i][j].hour -1
                activity[pos] = activity[pos] + 1
            totalActivity[i] = activity
        return totalActivity

    """
     This method calculates the average of all the activity per hour
     Input:
        totalActivity: Dictionary = Date, list[24] with frequencies
     Output:
        average: List [24] each position represents the average of the len(totalActivity) days
    """
    def getAverageActivityPerHour(self, totalActivity):
        average = [0.0] * 24
        for i in totalActivity:
            for j in range(len(totalActivity[i])):
                average[j] = average[j] + totalActivity[i][j]
        #print average
        for i in range(len(average)):
             average[i] = average[i] / len(totalActivity)
        return average

    """This method calculates how many days a bee will live based on the registered activity
     Input:
        IdDictionay = Id, Date
     Output:
        LifecycleDic = ID, number of days"""
    def beeLifeCycleDays(self, idDic, dateDic, completeDict):
        beeLifeCycleDays = {}
        beeActivityPerDay = {}

        for i in completeDict:
            #print i
            sortedDate = completeDict[i].keys()
            sortedDate.sort()
            start = sortedDate[0]
            end = sortedDate[-1]
            totalDays = (end - start)
            totalDays = totalDays.days + 1
            for j in sortedDate:
                if totalDays< 1:
                    beeLifeCycleDays[i] = 1
                else:
                    beeLifeCycleDays[i] = totalDays
                for k in completeDict[i][j]:
                    # register the number of bees detected per day
                    if i in beeActivityPerDay:
                        beeActivityPerDay[i] = beeActivityPerDay[i] + 1
                    else:
                        beeActivityPerDay[i] = 1

        return beeLifeCycleDays, beeActivityPerDay

    # Reestructure this method it must have a different name
    def differentObservationsPerDay(self,completeDict, lifeCycle):
        diffObsPerDay = {}
        avgActivity = {}

        FMT = '%H:%M:%S'
        for i in completeDict:
            avgActivity[i] = 0
            #print "Id: " + str(i)
            diffObsPerDay[i] = {}
            for j in completeDict[i]:
                #print "Num of Observations:" +str(len(completeDict[i][j]))
                avgActivity[i] = avgActivity[i] + len(completeDict[i][j])
                diffObsPerDay[i][j] = defaultdict(list)
                for k in range(len(completeDict[i][j])-1):
                    # append the number of days 1 - end of the obs
                    # Validate if there are enough elements
                    #tmpDiff = []
                    #diffObsPerDay[i][j][len(completeDict[i][j])] = defaultdict(list)
                    if len(completeDict[i][j]) > 1:
                        diffObsPerDay[i][j][len(completeDict[i][j])].append(dt.strptime(str(completeDict[i][j][k + 1]), FMT) - dt.strptime(str(completeDict[i][j][k]), FMT))
                        # calculate the average of activity for each bee
                    else:
                        #if there are not enough elements append a 0
                        #tmpDiff=[0]
                        diffObsPerDay[i][j][len(completeDict[i][j])].append(0)
                    # Append the elements of the dict in the final list
                    #diffObsPerDay[i][j][len(completeDict[i][j])] = tmpDiff
                    # FIXME: detect if all the registers are continuous ej if there are 15 days detect if there exist activity everyday

    def differentBeesPerDay(self, idDict):
        """
        This method build a dictionary with DAY => List of IDS
        :param idDict:
        :return:
        """
        differentBeesPerDay = defaultdict(list)
        for i in idDict:
            for j in idDict[i]:
                if i not in differentBeesPerDay[j]:
                    differentBeesPerDay[j].append(i)

        return differentBeesPerDay

    def getSortedDays(self, days):
        element = 1
        days.sort()
        sortedDays = {}
        for i in days:
            sortedDays[i] = element
            element = element + 1
        sortedDays = collections.OrderedDict(sorted(sortedDays.items()))
        return sortedDays

    def detectContinuousBehavior(self, sortedDays, beeLifeCycleDays, completeDict):
        """
        This method detects od a bee has a continuous activity or not
        :param sortedDays:
        :param beeLifeCycleDays:
        :param completeDict:
        :return: continuousBehavior Dictionary ID => List of ordered days
        :return: continuousBees ID => Continous activity
        """
        continuousBehavior = defaultdict(list)
        continuousBees= {}
        for i in completeDict:
            for j in completeDict[i]:
                continuousBehavior[i].append(sortedDays[j])
            continuousBehavior[i].sort()
            if beeLifeCycleDays[i] == len(continuousBehavior[i]):
                continuousBees[i] = 'Continuous Activity'
            else:
                continuousBees[i] = 'Non-Continuous Activity'
        return continuousBehavior, continuousBees

    #def detectNocturneBehivior(self, completeDict):




    def analizeData(self, idDict, dateDict, completeDict, type):
        """
        This method analizes all input data and additionally, it generates graphs.
        :param idDict:
        :param dateDict:
        :param completeDict:
        :param type: type of data clean or unclean
        :return:
        """
        # Instatiate a plot object
        plot = Plot()
        """----------------------------------------------------------------------------------------
        1. What is the activity of the hive # of lectures per day?
           Get all the observations per day format = Observation date, number of observations
        ----------------------------------------------------------------------------------------"""
        observationsPerDay= self.observationsPerDay(idDict, dateDict)
        title = "Number of Observations Per Day"
        xAxis = "Period of Observation (DAYS):\n"
        yAxis = "Observations"
        chartName = "observationsPerday" + type

        #plot.barPlot(observationsPerDay, title, xAxis, yAxis, chartName, 'Obs')

        """----------------------------------------------------------------------------------------
        2. For how long a bee will be detected? how long a bee will live?
        Observations: taking into account the installation date
        ----------------------------------------------------------------------------------------"""
        beeLifeCycleDays, beeActivityPerDay= self.beeLifeCycleDays(idDict, dateDict, completeDict)
        #print beeLifeCycleDays
        title = "Life Cycle of a bee in Days"
        xAxis = "Bees"
        yAxis = "Number of Days"
        chartName = "beeLifeCycle" + type
        chartName2 = "pieBeeLifeCycle" + type
        #plot.barPlot(beeLifeCycleDays, title, xAxis, yAxis, chartName, 'Life')
        #plot.pieChartBeeLifeCycle(beeLifeCycleDays,chartName2, title)
        #print beeActivityPerDay
        """----------------------------------------------------------------------------------------
        3. How many different bees are active per day?
        ----------------------------------------------------------------------------------------"""
        #self.differentObservationsPerDay(completeDict, beeLifeCycleDays)

        # Dictionary => Date => ID
        differentBeesPerDay = self.differentBeesPerDay(idDict)

        # Dictionary ID = 1, 2, ... n  Keys= sortedDays
        sortedDays  = self.getSortedDays(dateDict.keys())

        # A Continuous behavior is detected if the bee has activity at least once a day
        continuousBehavior, continuousBees = self.detectContinuousBehavior(sortedDays, beeLifeCycleDays, completeDict)

        # First graph different Bees Per Day
        title = "Register of Different Bees per Day"
        xAxis = "Days\n"
        yAxis = "Number of bees"
        chartName = "differentBeesPerday" + type

        #plot.barPlot(differentBeesPerDay, title, xAxis, yAxis, chartName, 'diffBees')

        """----------------------------------------------------------------------------------------
        4. What is the total activity per day number of hours?
        Get the range of activity time for each day timeInterval
        ----------------------------------------------------------------------------------------"""
        timeInterval = self.activityPerDay(dateDict)
        #get the average of activity per day = single timedelta value
        averageTotalActivity = self.averageTotalActivity(timeInterval)
        print "Average total activity: " + str(averageTotalActivity)

        """----------------------------------------------------------------------------------------
        5. What are the most active hours within a day?
        divide the space in 24 equivalence classes and obtain the frequency for each class
        ----------------------------------------------------------------------------------------"""
        totalActivityEquivClasses = self.getActivityPerHour(observationsPerDay, dateDict)

        """----------------------------------------------------------------------------------------
        6. What are the mean of the most active hours taking into account all the observations?
        ----------------------------------------------------------------------------------------"""

        averageEquivClasses = np.mean(totalActivityEquivClasses.values(), dtype=np.float32, axis=0)
        stdEquivClasses = np.std(totalActivityEquivClasses.values(), dtype=np.float32, axis=0)
        #print "Average: " + str(averageEquivClasses)
        #print "Std: " + str(stdEquivClasses)
        # Graph the activity by equivalence classes

        title = "Average of the Activity Per Hour"
        xAxis = "Hours"
        yAxis = "Occurrences"
        chartName = "histogram" + type
        plot.plotEquivalenceClass(averageEquivClasses, title, xAxis, yAxis, chartName)



        title = "Average of the Activity Per Hour Including Standard Deviation"
        xAxis = "Hours"
        yAxis = "Occurrences"
        chartName = "histogramStd" + type
        plot.plotEquivalenceClassStd(averageEquivClasses, title, xAxis, yAxis, stdEquivClasses, chartName)



        """----------------------------------------------------------------------------------------
        7. Time interval between activities
        ----------------------------------------------------------------------------------------"""

        #8. Make a scatter plot of all observations

        #9. detect Nocturnal behavior


        dict = {
            'ObsPerDay': observationsPerDay,
            'lifeCycle': beeLifeCycleDays,
            'differentBeesPerDay': differentBeesPerDay,
            'continuousBehavior' : continuousBehavior,
            'continuousBees': continuousBees,
            'averageTotalActivity': averageTotalActivity

        }
        return dict



