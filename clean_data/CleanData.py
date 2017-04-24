import itertools
import time
from datetime import datetime
from collections import defaultdict

class CleanData:

    def __init__(self):

        """ Put some initialization code"""

    """
        This method removes all the test lectures FFFFFF
    """
    def removeLostChips(self, idDict, dateDict, completeDict, threshold):

        cleanCompleteDict = {}
        cleanDateDict = {}
        cleanIdDict = {}


        #cleanDictionary = defaultdict(list)
        ommitedValues = defaultdict(list)
        timeDifference =  defaultdict(list)
        FMT = '%H:%M:%S'
        count = 0

        for i in completeDict:
            for j in  completeDict[i]:
                for k in range (len(completeDict[i][j])-1):
                    # validate if there are at least two elements the same day
                    if len(completeDict[i][j]) >= 2:
                        tmpDiff = datetime.strptime(str(completeDict[i][j][k + 1]), FMT) - datetime.strptime(str(completeDict[i][j][k]), FMT)
                        # The value will be discarded and stored in a list
                        #FIXME: CHECK IF IT IS NECCESARY TO STORE THIS DAT
                        if (tmpDiff < threshold):
                            ommitedValues[i].append(completeDict[i][j][k])
                        # The value will be stored in a dictionary
                        else:

                            cleanCompleteDict[i] = defaultdict(list)
                            # The current element doesn't exist in the dictionary
                            if i in cleanCompleteDict.keys():
                                cleanCompleteDict[i][j].append(completeDict[i][j][k])
                            # The element exists
                            else:
                                cleanCompleteDict[i] = defaultdict(list)
                                cleanCompleteDict[i][j].append(completeDict[i][j][k])

                        timeDifference[i].append(tmpDiff)
                if len(timeDifference[i]) > 1:
                    timeDifference[i].sort()
        print "count:  " + str(count)
        #print cleanCompleteDict
        print "Len of cleanDict is: " + str(len(cleanCompleteDict))
        #print cleanDictionary
        print "Len of completeDict is: " + str(len(completeDict))
        #print completeDict
        print "Len of ommited values is: " + str(len(ommitedValues))



