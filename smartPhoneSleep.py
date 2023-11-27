# Importing the module into this Python environment

# TODO: ADD R SQUARED FACTOR FOR TRENDLINE

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager
import pandas as pd
import numpy as np
import csv, random
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# FIRST GRAPH

with open('sleepHealthLifestyle.csv', newline='') as sleepHealthRawData:
    reader = csv.reader(sleepHealthRawData)
    sleepHealthData = list(reader)

sleepHealthData.pop(0)

processedHealthData = []
gender = 1
sleepDuration = 4
qualitySleep = 5
dailySteps = 11

i = 0

while i < len(sleepHealthData):
    # Store the processed data into separate variables
    processedGender = sleepHealthData[i][gender]
    processedSleepDuration = float(sleepHealthData[i][sleepDuration])
    processedQualitySleep = int(sleepHealthData[i][qualitySleep])
    processedDailySteps = int(sleepHealthData[i][dailySteps])
    processedHealthData.append([processedDailySteps, processedSleepDuration, processedQualitySleep, processedGender]) 
    i += 1 
 
    processedHealthData = list(set(map(tuple, processedHealthData))) # Get rid of duplicate lists

femaleSleepHealthData = []
maleSleepHealthData = []

for participant in processedHealthData:
    if participant[3] == "Female": 
        femaleSleepHealthData.append(participant)
    if participant[3] == "Male": 
        maleSleepHealthData.append(participant)

processedHealthData.sort()
femaleSleepHealthData.sort()
maleSleepHealthData.sort()

# for i in femaleSleepHealthData:
#     print(i)

# for i in maleSleepHealthData:
#     print(i)

# for i in processedHealthData:
#     print(i)

# Remove outliers
processedHealthDataCleaned = processedHealthData
for i in range(5):
    processedHealthDataCleaned.pop(-2)
for i in range(2):
    processedHealthDataCleaned.pop(-16)

dfCleaned = pd.DataFrame(processedHealthDataCleaned, columns = ["dailySteps", "sleepDuration", "sleepQuality", "gender"])

df = pd.DataFrame(processedHealthData, columns=["dailySteps", "sleepDuration", "sleepQuality", "gender"])
df0 = pd.DataFrame(femaleSleepHealthData, columns = ["dailySteps", "sleepDuration", "sleepQuality", "gender"])
df1 = pd.DataFrame(maleSleepHealthData, columns = ["dailySteps", "sleepDuration", "sleepQuality", "gender"])

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6,6))
fig.tight_layout(pad=5.0)

yStart = 5.5
yTicks = []
while yStart <= 8.5:
    yTicks.append(yStart)
    yStart += 0.5

xStart = 3000
xTicks = []
while xStart <= 10000:
    xTicks.append(xStart)
    xStart += 1000

ax[0].set_xticks(xTicks)
ax[0].set_yticks(yTicks)
ax[0].set_title("Correlation of Daily Steps \nto Sleep Duration", fontname="Silom", size=16, fontweight="bold", pad=15.0)
ax[0].set_xlabel("Average Daily Steps", fontname="Silom", size=12, fontweight="bold", labelpad=10)
ax[0].set_ylabel("Average Sleep Duration (hr)", fontname="Silom", size=12, fontweight="bold", labelpad=10)
ax[0].set_position([0.1,0.1,0.3,0.77])
ax[0].set_facecolor('xkcd:very light blue')
labels = ax[0].get_xticklabels() + ax[0].get_yticklabels()
[label.set_fontname("Silom") for label in labels]

femaleScatter = ax[0].scatter(df0.dailySteps, df0.sleepDuration, color='xkcd:scarlet', s=df0.sleepDuration ** 8 / 40000, alpha=df0.sleepQuality ** 2 * 0.01)
maleScatter = ax[0].scatter(df1.dailySteps, df1.sleepDuration, color='xkcd:bright blue', s=df1.sleepDuration ** 8 / 40000, alpha=df1.sleepQuality ** 2 * 0.01) 

slope, intercept = np.polyfit(dfCleaned.dailySteps, dfCleaned.sleepDuration, 1)
ax[0].plot(dfCleaned.dailySteps, slope*dfCleaned.dailySteps+intercept, color='xkcd:jade green', lw=5.0, alpha=0.8)

legend_elements = [
                    Line2D([0], [0], marker='o', color='xkcd:light sea green', label='Female, all ages',
                        markerfacecolor='xkcd:scarlet', markersize=15),
                    Line2D([0], [0], marker='o', color='xkcd:light sea green', label='Male, all ages',
                        markerfacecolor='xkcd:bright blue', markersize=15), 
                    Line2D([0], [0], color='xkcd:jade green', lw=4, label='Trendline')
                    # Patch(facecolor='xkcd:marine', edgecolor='xkcd:light sea green',
                    #     label='Size: Sleep Duration'),
                    # Patch(facecolor='xkcd:deep teal', edgecolor='xkcd:light sea green',
                    # label='Opacity: Sleep Quality')
                    ]
# frameon=False/True, title=''
legend = ax[0].legend(handles=legend_elements, loc='center', bbox_to_anchor=(1.4, 0.9), ncol=1, frameon=True, borderpad=1.0, labelspacing=0.8, prop={'family':"Silom"})
frame = legend.get_frame()
frame.set_facecolor('xkcd:light sea green')
frame.set_edgecolor('black')


# SECOND GRAPH

# Opening and reading the CSV file
with open('typicalSmartphoneUsage.csv', newline='') as smartphoneRawData:
    # Stores the data inside a smartphoneData variable
    reader = csv.reader(smartphoneRawData)
    # The format of smartphoneData will be a list of lists. 
    smartphoneData = list(reader)


# This removes the first row of the dataset, which includes all the titles for the columns as it is irrelevant in data processing
smartphoneData.pop(0)

processedSelectedData = [] # Create the list for the final processed data
numberOfDays = 13 # This is how long the experimented lasted, will be used later to calculate average
columnIndex1 = 34 # This selects the column for the total smartphone use in the span of 13 days
columnIndex2 = 35 # This selects the column for the total smartphone checks in the span of 13 days
columnIndex3 = 3 # This selects the column for the gender of the participant (1 for female, 2 for male)
columnIndex4 = 1 # This selects the column for the MPPUS
columnIndex5 = 2 # This selects the column for the age

# Initialize the index
i = 0

while i < len(smartphoneData):
    # Store the processed data into separate variables
    processedData1 = float(smartphoneData[i][columnIndex1]) / numberOfDays # Important to convert string to float before calculation for average
    processedData2 = float(smartphoneData[i][columnIndex2]) / numberOfDays
    genderData = int(smartphoneData[i][columnIndex3])
    mppusData = int(smartphoneData[i][columnIndex4])
    ageData = int(smartphoneData[i][columnIndex5])
    processedSelectedData.append([processedData1, processedData2, genderData, mppusData, ageData]) # Append the two variables in a list formal
    i += 1 

# Create 1 separate list for all the female participants, 1 separate list for all the male participants
femaleProcessedData = []
maleProcessedData = []

# Run a loop that checks through every user (participant) in processedSelectedData (list)
for participant in processedSelectedData:
    # Checks the 2nd column of each participant list, which corresponds to their gender

    # If the number is 1, then they are female, and appended to femaleProcessedData
    if participant[2] == 1: 
        femaleProcessedData.append(participant)

    # If the number is 1, then they are female, and appended to femaleProcessedData
    if participant[2] == 2: 
        maleProcessedData.append(participant)

# This is the Python built-in function to sort a list
# The default parameter will sort the first column from small to big, which is the average daily smarphone usage (hrs)
processedSelectedData.sort()
femaleProcessedData.sort()
maleProcessedData.sort()

# Remove outliers
processedSelectedDataCleaned = processedSelectedData
processedSelectedDataCleaned.pop(-4)

dfCleaned = pd.DataFrame(processedSelectedDataCleaned, columns = ["x", "checks", "gender", "y", "age"])

# How to format data into usable MatPlotLib format

df = pd.DataFrame(femaleProcessedData, columns = ["x", "checks", "gender", "y", "age"])
df1 = pd.DataFrame(maleProcessedData, columns = ["x", "checks", "gender", "y", "age"])

# lineAgeConstant = 0.015 # For transparency relating to the average age
# averageFemaleAge = 0
# count = 0

# for female in femaleProcessedData: 
#     count += female[4]
# averageFemaleAge = count / len(maleProcessedData)

# count = 0
# for male in maleProcessedData: 
#     count += male[4]
# averageMaleAge = count / len(maleProcessedData)

yStart = 50
yTicks = []
while yStart <= 200:
    yTicks.append(yStart)
    yStart += 10

xStart = 0
xTicks = []
while xStart <= 12:
    xTicks.append(xStart)
    xStart += 1

ax[1].set_xticks(xTicks)
ax[1].set_yticks(yTicks)
ax[1].set_title("Correlation of Smartphone Usage \nto Mobile Phone Problem Use Scale", fontname="Silom", size=16, fontweight="bold", pad=15.0)
ax[1].set_xlabel("Average Daily Smartphone Usage (hrs)", fontname="Silom", size=12, fontweight="bold", labelpad=10)
ax[1].set_ylabel("Mobile Phone Problem Use Scale (MPPUS)", fontname="Silom", size=12, fontweight="bold", labelpad=10)
ax[1].set_position([0.65,0.1,0.3,0.77])
ax[1].set_facecolor('xkcd:very light blue')
labels = ax[1].get_xticklabels() + ax[1].get_yticklabels()
[label.set_fontname("Silom") for label in labels]

femaleScatter = ax[1].scatter(df.x, df.y, color='xkcd:scarlet', s=df.checks * 10, alpha=df.age ** 2 * 0.0008)
maleScatter = ax[1].scatter(df1.x, df1.y, color='xkcd:bright blue', s=df1.checks * 10, alpha=df.age ** 2 * 0.0008)
# ax[1].plot(df.x, df.y, color='red', alpha=averageFemaleAge*lineAgeConstant) 
# ax[1].plot(df1.x, df1.y, color='blue', alpha=averageMaleAge*lineAgeConstant)

slope, intercept = np.polyfit(dfCleaned.x, dfCleaned.y, 1)
ax[1].plot(dfCleaned.x, slope*dfCleaned.x+intercept, color='xkcd:jade green', lw=5.0, alpha=0.8)

# Overall plot
ax[0].text(0.35, 0.64, 'Upward Trend', horizontalalignment='center', verticalalignment='center', 
           rotation=-20, transform=ax[0].transAxes, 
           bbox = {'facecolor': 'xkcd:viridian', 'alpha': 0.5, 'boxstyle': "rarrow,pad=0.3", 'ec': 'xkcd:deep teal'}, 
           fontname="Silom", size=12, fontweight="bold")
ax[0].text(0.82, 0.13, 'Outliers', horizontalalignment='center', verticalalignment='center', 
           rotation=0, transform=ax[0].transAxes, 
           bbox = {'facecolor': 'xkcd:dark periwinkle', 'alpha': 0.5, 'boxstyle': "darrow,pad=0.3", 'ec': 'xkcd:indigo'}, 
           fontname="Silom", size=9, fontweight="bold")
ax[0].text(1.4, 1, 'Legend', horizontalalignment='center', verticalalignment='center', 
           rotation=0, transform=ax[0].transAxes,  
           fontname="Silom", size=12, fontweight="bold")
ax[0].text(0.78, 0.93, 'Size correlates to \nSleep Duration', horizontalalignment='center', verticalalignment='center', 
           rotation=0, transform=ax[0].transAxes, 
           bbox = {'facecolor': 'xkcd:light burgundy', 'alpha': 0.5, 'boxstyle': "roundtooth,pad=0.6", 'ec': 'xkcd:plum'}, 
           fontname="Silom", size=10.5, fontweight="bold")
ax[0].text(0.74, 0.3, 'Opacity correlates to \nSleep Quality', horizontalalignment='center', verticalalignment='center', 
           rotation=0, transform=ax[0].transAxes, 
           bbox = {'facecolor': 'xkcd:aquamarine', 'alpha': 0.5, 'boxstyle': "sawtooth,pad=0.6", 'ec': 'xkcd:blue green'}, 
           fontname="Silom", size=10.5, fontweight="bold")
ax[1].text(2.6, 0.5, 'Upward Trend', horizontalalignment='center', verticalalignment='center', 
           rotation=-45, transform=ax[0].transAxes, 
           bbox = {'facecolor': 'xkcd:viridian', 'alpha': 0.5, 'boxstyle': "larrow,pad=0.3", 'ec': 'xkcd:deep teal'}, 
           fontname="Silom", size=12, fontweight="bold")
ax[1].text(2.4, 0.05, 'Outlier', horizontalalignment='center', verticalalignment='center', 
           rotation=0, transform=ax[0].transAxes, 
           bbox = {'facecolor': 'xkcd:dark periwinkle', 'alpha': 0.5, 'boxstyle': "rarrow,pad=0.3", 'ec': 'xkcd:indigo'}, 
           fontname="Silom", size=9, fontweight="bold")
ax[1].text(2.55, 0.2, 'Size correlates to \nNumber of \nSmartphone Checks', horizontalalignment='center', verticalalignment='center', 
           rotation=0, transform=ax[0].transAxes, 
           bbox = {'facecolor': 'xkcd:light burgundy', 'alpha': 0.5, 'boxstyle': "roundtooth,pad=0.6", 'ec': 'xkcd:plum'}, 
           fontname="Silom", size=10.5, fontweight="bold")
ax[1].text(2.0, 0.85, 'Opacity \ncorrelates \nto Age', horizontalalignment='center', verticalalignment='center', 
           rotation=0, transform=ax[0].transAxes, 
           bbox = {'facecolor': 'xkcd:aquamarine', 'alpha': 0.5, 'boxstyle': "sawtooth,pad=0.6", 'ec': 'xkcd:blue green'}, 
           fontname="Silom", size=10.5, fontweight="bold")

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()



