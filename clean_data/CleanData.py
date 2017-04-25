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
    #FIXME: IS NOT NECCESARY TO TRANSFEER IDDICT AND DATEDICT
    def removeLostChips(self, idDict, dateDict, completeDict, threshold):

        cleanCompleteDict = {}
        ommitedValues = {}
        timeDifference =  defaultdict(list)
        cleanIdDict = defaultdict(list)
        cleanDateDict = defaultdict(list)
        FMT = '%H:%M:%S'

        # Get statistics of lost chips
        totalElements = 0
        totalOmmited = 0
        totalClean = 0

        for i in completeDict:
            for j in  completeDict[i]:
                cleanIdDict[i].append(j)
                for k in range (len(completeDict[i][j])-1):
                    # validate if there are at least two elements the same day
                    totalElements = totalElements + 1
                    if len(completeDict[i][j]) >= 2:
                        tmpDiff = datetime.strptime(str(completeDict[i][j][k + 1]), FMT) - datetime.strptime(str(completeDict[i][j][k]), FMT)
                        # The value will be discarded and stored in a list
                        #FIXME: CHECK IF IT IS NECCESARY TO STORE THIS DATE
                        if (tmpDiff < threshold):
                            totalOmmited = totalOmmited + 1
                            #veriify if the ith element exist
                            if i in ommitedValues.keys():
                                ommitedValues[i][j].append(completeDict[i][j][k])
                            else:
                                ommitedValues[i] = defaultdict(list)
                                ommitedValues[i][j].append(completeDict[i][j][k])
                        # The value will be stored in a dictionary
                        else:
                            totalClean = totalClean + 1
                            cleanCompleteDict[i] = defaultdict(list)
                            # The current element exists in the dictionary
                            if i in cleanCompleteDict.keys():
                                cleanCompleteDict[i][j].append(completeDict[i][j][k])
                                cleanDateDict[j].append(completeDict[i][j][k])
                            # The element doesn't exists
                            else:
                                cleanCompleteDict[i] = defaultdict(list)
                                cleanCompleteDict[i][j].append(completeDict[i][j][k])

                        timeDifference[i].append(tmpDiff)
                if len(timeDifference[i]) > 1:
                    timeDifference[i].sort()


        results = {
            'cleanCompleteDict': cleanCompleteDict,
            'cleanIdDict': cleanIdDict,
            'cleanDateDict': cleanDateDict,
            'ommitedValues': ommitedValues,
            'timeIntervals': timeDifference,
            'totalElements': totalElements,
            'totalOmmited': totalOmmited,
            'totalClean': totalClean
        }

        return results



