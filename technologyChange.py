# Import modules
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

# Some colours use xkcd 
# Reference: https://xkcd.com/color/rgb/

# Open computerCost.csv from this website: 
# https://ourworldindata.org/technological-change#interactive-charts-on-technological-change 
with open('computerCost.csv', newline='') as computerCostRawData:
    reader = csv.reader(computerCostRawData)
    computerCostData = list(reader)

computerCostData.pop(0)

# Empty list for all 4 categories
processedMemoryData = []
processedFlashData = []
processedDiskdriveData = []
processedSSDData = []

# Indices for csv file columns
year = 2
memory = 3
flash = 4
diskdrive = 5
ssd = 6

# Add data to all 4 lists
i = 0
while i < len(computerCostData):
    if computerCostData[i][memory] != '':
        processedYear = float(computerCostData[i][year])
        processedMemory = float(computerCostData[i][memory])
        processedMemoryData.append([processedYear, processedMemory])
    if computerCostData[i][flash] != '':
        processedYear = float(computerCostData[i][year])
        processedFlash = float(computerCostData[i][flash])
        processedFlashData.append([processedYear, processedFlash])
    if computerCostData[i][diskdrive] != '':
        processedYear = float(computerCostData[i][year])
        processedDiskdrive = float(computerCostData[i][diskdrive])
        processedDiskdriveData.append([processedYear, processedDiskdrive])
    if computerCostData[i][ssd] != '':
        processedYear = float(computerCostData[i][year])
        processedSSD = float(computerCostData[i][ssd])
        processedSSDData.append([processedYear, processedSSD])
    i += 1 

# Sort
processedMemoryData.sort()
processedFlashData.sort()
processedDiskdriveData.sort()
processedSSDData.sort()

# Format data using Pandas dataframe
dfMemory = pd.DataFrame(processedMemoryData, columns=["year", "memory"])
dfFlash = pd.DataFrame(processedFlashData, columns=["year", "flash"])
dfDiskdrive = pd.DataFrame(processedDiskdriveData, columns=["year", "diskdrive"])
dfSSD = pd.DataFrame(processedSSDData, columns=["year","ssd"])

# Y Axis Ticks (Exponential)
yStart = 100
yTicks = []
while yStart <= 100000000000000:
    yTicks.append(yStart)
    yStart *= 100

# X Axis Ticks (Linear)
xStart = 1970
xTicks = [1956]
while xStart <= 2010:
    xTicks.append(xStart)
    xStart += 10
xTicks.append(2022)

# Labels for ticks
tickLabels = ["100 $/TB", "10,000 $/TB", "1 million $/TB", "100 million $/TB", "10 billion $/TB", "1 trillion $/TB", "100 trillion $/TB"]

# Plot parameters
fig, ax = plt.subplots()
ax.set_xticks(ticks=xTicks)
ax.set_yscale('log')
ax.set_yticks(ticks=yTicks, labels=tickLabels)
ax.set_xlabel("Year", fontname="Silom", size=12, fontweight="bold", labelpad=10)
ax.set_ylabel("Cost (USD)", fontname="Silom", size=12, fontweight="bold", labelpad=10)
ax.set_title("Historical Cost of Computer Technology", fontname="Silom", size=16, fontweight="bold", pad=15.0)
ax.set_facecolor('xkcd:marine blue')

# Set font for all labels
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname("Silom") for label in labels]

# Legend elements
legend_elements = [
                    Line2D([0], [0], color='xkcd:light blue green', lw=4, label='Memory'),
                    Line2D([0], [0], color='xkcd:very light blue', lw=4, label='Flash'),
                    Line2D([0], [0], color='xkcd:neon blue', lw=4, label='Disk Drive'),
                    Line2D([0], [0], color='xkcd:watermelon', lw=4, label='SSD')
                    ]

# Set legend
legend = ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.95, 0.9), ncol=1, frameon=True, borderpad=1.0, labelspacing=0.8, prop={'family':"Silom"})

# Legend parameters
for text in legend.get_texts():
    text.set_color('white')
frame = legend.get_frame()
frame.set_facecolor('xkcd:electric blue')
frame.set_edgecolor('white')

# Line graphs (4 categories)
memoryLine, = ax.plot(dfMemory.year, dfMemory.memory, color='xkcd:light blue green')
flashLine, = ax.plot(dfFlash.year, dfFlash.flash, color='xkcd:very light blue')
diskdriveLine, = ax.plot(dfDiskdrive.year, dfDiskdrive.diskdrive, color='xkcd:neon blue')
ssdLine, = ax.plot(dfSSD.year, dfSSD.ssd, color='xkcd:watermelon')

# Scatter graphs (4 categories)
memoryScatter = ax.scatter(dfMemory.year, dfMemory.memory, color='xkcd:light blue green', s=20)
flashScatter = ax.scatter(dfFlash.year, dfFlash.flash, color='xkcd:very light blue', s=20)
diskdriveScatter = ax.scatter(dfDiskdrive.year, dfDiskdrive.diskdrive, color='xkcd:neon blue', s=20)
ssdScatter = ax.scatter(dfSSD.year, dfSSD.ssd, color='xkcd:watermelon', s=20)

# Annotations
ax.text(0.5, 0.70, 'Downward Trend \nfor Cost', horizontalalignment='center', verticalalignment='center', 
           rotation=25, transform=ax.transAxes, 
           bbox = {'facecolor': 'xkcd:tangerine', 'alpha': 0.5, 'boxstyle': "larrow,pad=0.5", 'ec': 'xkcd:orange red'}, 
           fontname="Silom", size=12, fontweight="bold", color='white')
ax.text(0.2, 0.90, 'Over 100 trillion $/TB!', horizontalalignment='center', verticalalignment='center', 
           rotation=-10, transform=ax.transAxes, 
           bbox = {'facecolor': 'xkcd:scarlet', 'alpha': 0.5, 'boxstyle': "larrow,pad=0.5", 'ec': 'xkcd:blood red'}, 
           fontname="Silom", size=12, fontweight="bold", color='white')
ax.text(0.5, 0.2, 'Less than 100 $/TB! \n Much more affordable.', horizontalalignment='center', verticalalignment='center', 
           rotation=-10, transform=ax.transAxes, 
           bbox = {'facecolor': 'xkcd:viridian', 'alpha': 0.5, 'boxstyle': "rarrow,pad=0.5", 'ec': 'xkcd:deep teal'}, 
           fontname="Silom", size=12, fontweight="bold", color='white')
ax.text(0.88, 0.93, 'Legend', horizontalalignment='center', verticalalignment='center', 
           rotation=0, transform=ax.transAxes,  
           fontname="Silom", size=12, fontweight="bold", color='white')

# Create animations
# Reference: https://www.geeksforgeeks.org/using-matplotlib-for-animations/ 
def update(num, x, y, line):
    line.set_data(x[:num], y[:num])
    return line,

ani1 = animation.FuncAnimation(fig, update, len(dfMemory.year), interval=200, fargs=[dfMemory.year, dfMemory.memory, memoryLine],
                              blit=False)
ani1.save('memoryLineAnimation.gif', fps=60)
ani2 = animation.FuncAnimation(fig, update, len(dfMemory.year), interval=200, fargs=[dfFlash.year, dfFlash.flash, flashLine],
                              blit=False)
ani2.save('flashLineAnimation.gif', fps=60)
ani3 = animation.FuncAnimation(fig, update, len(dfMemory.year), interval=200, fargs=[dfDiskdrive.year, dfDiskdrive.diskdrive, diskdriveLine],
                              blit=False)
ani3.save('diskdriveLineAnimation.gif', fps=60)
ani4 = animation.FuncAnimation(fig, update, len(dfMemory.year), interval=200, fargs=[dfSSD.year, dfSSD.ssd, ssdLine],
                              blit=False)
ani4.save('ssdLineAnimation.gif', fps=60)

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()

# When running give it a couple seconds for the animations to render
