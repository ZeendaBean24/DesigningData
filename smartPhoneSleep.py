# Import modules
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import csv
from matplotlib.lines import Line2D

# Some colours use xkcd 
# Reference: https://xkcd.com/color/rgb/

# First graph:
# Open sleepHealthLifestyle.csv from this website: 
# https://www.research.lancs.ac.uk/portal/en/datasets/typical-smartphone-usage-dataset(24cc8151-a0fc-4753-8fd9-efb0313a8651).html 
with open('sleepHealthLifestyle.csv', newline='') as sleepHealthRawData:
    reader = csv.reader(sleepHealthRawData)
    sleepHealthData = list(reader)

sleepHealthData.pop(0)

# Empty list for processed health data
processedHealthData = []

# Indices for csv file columns
gender = 1
sleepDuration = 4
qualitySleep = 5
dailySteps = 11

# Add data to processed health list
i = 0
while i < len(sleepHealthData):
    # Store the processed data into separate variables
    processedGender = sleepHealthData[i][gender]
    processedSleepDuration = float(sleepHealthData[i][sleepDuration])
    processedQualitySleep = int(sleepHealthData[i][qualitySleep])
    processedDailySteps = int(sleepHealthData[i][dailySteps])
    processedHealthData.append([processedDailySteps, processedSleepDuration, processedQualitySleep, processedGender]) 
    i += 1 
 
    # Removes duplicates
    processedHealthData = list(set(map(tuple, processedHealthData))) 

# Create separate health lists for Female and Male
femaleSleepHealthData = []
maleSleepHealthData = []

# Add participants by gender accordingly
for participant in processedHealthData:
    if participant[3] == "Female": 
        femaleSleepHealthData.append(participant)
    if participant[3] == "Male": 
        maleSleepHealthData.append(participant)

# Sort
processedHealthData.sort()
femaleSleepHealthData.sort()
maleSleepHealthData.sort()

# Remove outliers
processedHealthDataCleaned = processedHealthData
for i in range(5):
    processedHealthDataCleaned.pop(-2)
for i in range(2):
    processedHealthDataCleaned.pop(-16)

# Format data using Pandas dataframe
# Cleaned = outliers removed (for trendline later)
dfCleaned = pd.DataFrame(processedHealthDataCleaned, columns = ["dailySteps", "sleepDuration", "sleepQuality", "gender"])
dfOverallHealthData = pd.DataFrame(processedHealthData, columns=["dailySteps", "sleepDuration", "sleepQuality", "gender"])
dfFemaleHealthData = pd.DataFrame(femaleSleepHealthData, columns = ["dailySteps", "sleepDuration", "sleepQuality", "gender"])
dfMaleHealthData = pd.DataFrame(maleSleepHealthData, columns = ["dailySteps", "sleepDuration", "sleepQuality", "gender"])

# Creates subplots: 2 columns, 1 row
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6,6))
fig.tight_layout(pad=5.0)

# Y Axis Ticks (Linear)
yStart = 5.5
yTicks = []
while yStart <= 8.5:
    yTicks.append(yStart)
    yStart += 0.5

# X Axis Ticks (Linear)
xStart = 3000
xTicks = []
while xStart <= 10000:
    xTicks.append(xStart)
    xStart += 1000

# Plot parameters
ax[0].set_xticks(xTicks)
ax[0].set_yticks(yTicks)
ax[0].set_title("How Physical Activity \nAffects Sleep Duration", fontname="Silom", size=16, fontweight="bold", pad=15.0)
ax[0].set_xlabel("Average Daily Steps", fontname="Silom", size=12, fontweight="bold", labelpad=10)
ax[0].set_ylabel("Average Sleep Duration (hr)", fontname="Silom", size=12, fontweight="bold", labelpad=10)
ax[0].set_position([0.1,0.1,0.3,0.77])
ax[0].set_facecolor('xkcd:very light blue')

# Set font for all labels
labels = ax[0].get_xticklabels() + ax[0].get_yticklabels()
[label.set_fontname("Silom") for label in labels]

# Scatter plots (female and male)
femaleScatter = ax[0].scatter(dfFemaleHealthData.dailySteps, dfFemaleHealthData.sleepDuration, color='xkcd:scarlet', s=dfFemaleHealthData.sleepDuration ** 8 / 40000, alpha=dfFemaleHealthData.sleepQuality ** 2 * 0.01)
maleScatter = ax[0].scatter(dfMaleHealthData.dailySteps, dfMaleHealthData.sleepDuration, color='xkcd:bright blue', s=dfMaleHealthData.sleepDuration ** 8 / 40000, alpha=dfMaleHealthData.sleepQuality ** 2 * 0.01) 

# Trendline Calculation
# Reference: https://www.statology.org/matplotlib-trendline/
slope, intercept = np.polyfit(dfCleaned.dailySteps, dfCleaned.sleepDuration, 1)
ax[0].plot(dfCleaned.dailySteps, slope*dfCleaned.dailySteps+intercept, color='xkcd:jade green', lw=5.0, alpha=0.8)

# Legend elements
legend_elements = [
                    Line2D([0], [0], marker='o', color='xkcd:light sea green', label='Female, all ages',
                        markerfacecolor='xkcd:scarlet', markersize=15),
                    Line2D([0], [0], marker='o', color='xkcd:light sea green', label='Male, all ages',
                        markerfacecolor='xkcd:bright blue', markersize=15), 
                    Line2D([0], [0], color='xkcd:jade green', lw=4, label='Trendline')
                    ]

# Legend parameters
legend = ax[0].legend(handles=legend_elements, loc='center', bbox_to_anchor=(1.4, 0.9), ncol=1, frameon=True, borderpad=1.0, labelspacing=0.8, prop={'family':"Silom"})
frame = legend.get_frame()
frame.set_facecolor('xkcd:light sea green')
frame.set_edgecolor('black')


# Second Graph
# Open typicalSmartphoneUsage.csv from this website
# https://www.gigasheet.com/sample-data/sleep-health-and-lifestyle-dataset  

with open('typicalSmartphoneUsage.csv', newline='') as smartphoneRawData:
    reader = csv.reader(smartphoneRawData)
    smartphoneData = list(reader)

smartphoneData.pop(0)

# Empty list for all 
processedSmartphoneData = [] 
days = 13 
smartphoneUse = 34 
smartphoneChecks = 35 
gender = 3
mppus = 1 
age = 2 

# Add data to processed smartphone list
i = 0
while i < len(smartphoneData):
    processedData1 = float(smartphoneData[i][smartphoneUse]) / days # Important to convert string to float before calculation for average
    processedData2 = float(smartphoneData[i][smartphoneChecks]) / days
    genderData = int(smartphoneData[i][gender])
    mppusData = int(smartphoneData[i][mppus])
    ageData = int(smartphoneData[i][age])
    processedSmartphoneData.append([processedData1, processedData2, genderData, mppusData, ageData]) # Append the two variables in a list formal
    i += 1 

# Create separate health lists for Female and Male
femaleProcessedData = []
maleProcessedData = []

# Add participants by gender accordingly
for participant in processedSmartphoneData:
    if participant[2] == 1: 
        femaleProcessedData.append(participant)
    if participant[2] == 2: 
        maleProcessedData.append(participant)

# Sort
processedSmartphoneData.sort()
femaleProcessedData.sort()
maleProcessedData.sort()

# Remove outliers
processedSmartphoneDataCleaned = processedSmartphoneData
processedSmartphoneDataCleaned.pop(-4)

# Format data using Pandas dataframe
# Cleaned = outliers removed (for trendline later)
dfCleaned = pd.DataFrame(processedSmartphoneDataCleaned, columns = ["x", "checks", "gender", "y", "age"])
dfFemaleHealthData = pd.DataFrame(femaleProcessedData, columns = ["x", "checks", "gender", "y", "age"])
dfMaleHealthData = pd.DataFrame(maleProcessedData, columns = ["x", "checks", "gender", "y", "age"])

# Y Axis Ticks (Linear)
yStart = 50
yTicks = []
while yStart <= 200:
    yTicks.append(yStart)
    yStart += 10

# X Axis Ticks (Linear)
xStart = 0
xTicks = []
while xStart <= 12:
    xTicks.append(xStart)
    xStart += 1

# Plot parameters
ax[1].set_xticks(xTicks)
ax[1].set_yticks(yTicks)
ax[1].set_title("How Smartphone Usage Correlates to \nMobile Phone Problem Use Scale", fontname="Silom", size=16, fontweight="bold", pad=15.0)
ax[1].set_xlabel("Average Daily Smartphone Usage (hrs)", fontname="Silom", size=12, fontweight="bold", labelpad=10)
ax[1].set_ylabel("Mobile Phone Problem Use Scale (MPPUS)", fontname="Silom", size=12, fontweight="bold", labelpad=10)
ax[1].set_position([0.65,0.1,0.3,0.77])
ax[1].set_facecolor('xkcd:very light blue')

# Set font for all labels
labels = ax[1].get_xticklabels() + ax[1].get_yticklabels()
[label.set_fontname("Silom") for label in labels]

# Scatter plots (female and male)
femaleScatter = ax[1].scatter(dfFemaleHealthData.x, dfFemaleHealthData.y, color='xkcd:scarlet', s=dfFemaleHealthData.checks * 10, alpha=dfFemaleHealthData.age ** 2 * 0.0008)
maleScatter = ax[1].scatter(dfMaleHealthData.x, dfMaleHealthData.y, color='xkcd:bright blue', s=dfMaleHealthData.checks * 10, alpha=dfMaleHealthData.age ** 2 * 0.0008)

# Trendline Calculation
# Reference: https://www.statology.org/matplotlib-trendline/
slope, intercept = np.polyfit(dfCleaned.x, dfCleaned.y, 1)
ax[1].plot(dfCleaned.x, slope*dfCleaned.x+intercept, color='xkcd:jade green', lw=5.0, alpha=0.8)

# Annotations for SUBPLOT/GRAPH 1
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

# Annotations for SUBPLOT/GRAPH 2
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
