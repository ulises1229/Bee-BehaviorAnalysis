class Statistics:

    def average(self, list):
        sum = 0
        for i in list:
            sum = sum + i;
        return (sum / len(list))

