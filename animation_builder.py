import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.dates as mdates
# csv file was taken 
df = pd.read_csv('Automatic_Hourly_Pedestrian_Count.csv')
#check the top
df.head(5)

df.drop_duplicates()
# get data shape looks the same as previous shape

# make all columns lower case
df.columns = [col.lower() for col in df]
df.set_index('objectid',inplace=True)
# change the formatting of shortdate, has unessary fluff
df.shortdate =  df.shortdate.apply(lambda x : x.rstrip(' 0:+'))
# group by date and sum the total count for each date from each location
grouped_items = df.groupby('shortdate')['totalcount'].sum().reset_index()
#convert index to date formate for easier useage and ordering
grouped_items.shortdate = pd.to_datetime(grouped_items.shortdate )
# as you see above it's not ordered by dates thus order by date
grouped_items.sort_values(by='shortdate', inplace=True)

# we see thre is one out lying in the first one so we will remove it
grouped_items = grouped_items.iloc[1:]
# reset the index
grouped_items = grouped_items.reset_index(drop=True)

grouped_items = grouped_items.set_index('shortdate')

# going to resample the data to weekly to reduce data size the string 'W-Mon' means week starting Monday
weekly_group_df = grouped_items.resample('W-Mon').sum()
weekly_group_df = weekly_group_df.reset_index()

def init():
	del xs[:]
	del ys[:]
	line.set_data(xs, ys)
	return line,
# set figures 
fig = plt.figure(figsize=(25,7))
ax = fig.add_subplot(1,1,1)
 #rotate the x-axis values
plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
# set the titles
ax.set_title('Weekly Sydney Pedestrian Count')
ax.set_ylabel('Pedestrian Traffic')
ax.set_xlabel('Dates')
# set the xtick frequencies
ax.set_xticks(weekly_group_df.shortdate[::4])
# formate the dates
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%m-%d"))
# initate line
line, = ax.plot([], [], lw=2)
# empty lists for the animation
xs,ys = [],[]
# animation function that loops through frames i
def run(i):
	xs.append(weekly_group_df.shortdate.iloc[i])
	ys.append(weekly_group_df.totalcount.iloc[i])
	line.set_data(xs, ys)
	ax.relim()
	ax.autoscale()
	return line,
# magic happens
animate = ani.FuncAnimation(fig, run, interval=100, frames = 148,init_func = init)
# save the animation in a gif using PillowWriter
animate.save("Weekly-Sydney-Pedestrian-Count.gif", dpi=300, writer=PillowWriter(fps=25))
# should be saved as fig in the same folder location