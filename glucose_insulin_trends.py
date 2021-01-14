import datetime
import random
import datetime


def calculateInsulin(recentGlucoseLevel, recentGlucoseTime, glucoseTrend, targetGlucoseLevel):
    """
    This function takes the most recent glucose level reading, the time of that reading, the most
    recently calculated glucoseTrend, and the users target glucose level and then calculates the
    amount of insulin required. If the calculated dosage is negative, this is a sign that the user
    should eat some fast-acting carbs. If positive, then the user should administer to themselves
    that many units of insulin.
    """

    if recentGlucoseTime < datetime.datetime.now() - datetime.timedelta(hours=2):
        return "NA"

    if glucoseTrend >= 2:
        dose = ((recentGlucoseLevel - targetGlucoseLevel) / 40) + 2.5
    elif 1 < glucoseTrend < 2:
        dose = ((recentGlucoseLevel - targetGlucoseLevel) / 40) + 1.5
    elif -1 <= glucoseTrend <= 1:
        dose = ((recentGlucoseLevel - targetGlucoseLevel) / 40)
    elif -2 < glucoseTrend < -1:
        dose = ((recentGlucoseLevel - targetGlucoseLevel) / 40) - 1.5
    elif glucoseTrend <= -2:
        dose = ((recentGlucoseLevel - targetGlucoseLevel) / 40) - 2.5
    return dose


def calculateTrend(recentGlucoseLevel1, recentGlucoseTime1, recentGlucoseLevel2, recentGlucoseTime2):
    """
    This function takes the most recent glucose level reading, the time of that reading, the second
    most recent glucose level reading, and the time of that reading and then calculates the current
    trend of the users glucose levels as a numerical value given in mg/dl/m and as an easily
    understandable description.
    """

    # if recentGlucoseTime2 < recentGlucoseTime1 - datetime.timedelta(hours=2):
    #     return "NA"

    # glucoseTrend = (recentGlucoseLevel1 - recentGlucoseLevel2) / (recentGlucoseTime1 - recentGlucoseTime2)
    glucoseTrend = random.randrange(-10, 10, 1)
    print(glucoseTrend)
    if glucoseTrend >= 2:
        trendDescription = "rapidly rising"
    elif 1 < glucoseTrend < 2:
        trendDescription = "rising"
    elif -1 <= glucoseTrend <= 1:
        trendDescription = "changing slowly"
    elif -2 < glucoseTrend < -1:
        trendDescription = "falling"
    elif glucoseTrend <= -2:
        trendDescription = "rapidly falling"
    return glucoseTrend, trendDescription

