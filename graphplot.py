import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import matplotlib.animation as animation

def init():
	# ax.set_ylim(-1.1, 1.1)
	# ax.set_xlim(0, 1)
	del xdata[:]
	del ydata[:]
	line.set_data(xdata, ydata)
	return line,


style.use('ggplot')

df = pd.read_csv('Automatic_Hourly_Pedestrian_Count.csv')

df.columns = [col.lower() for col in df]

df.set_index('objectid',inplace=True)
df.shortdate = df.shortdate.apply(lambda date : date.rstrip('+0: '))

grouped_df = df.groupby(['shortdate'])['totalcount'].sum().reset_index()
grouped_df2 = pd.DataFrame(grouped_df)
grouped_df2.shortdate = pd.to_datetime(grouped_df2.shortdate,format='%Y/%m/%d')
grouped_df2.shortdate = grouped_df2.shortdate.dt.date
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.grid()

xdata, ydata = [], []
ax.set_xlabel('Date')
ax.set_ylabel('Total Count')
ax.set_title('City of Sydney pedestrian count')

plt.xticks(rotation=45, ha="right", rotation_mode="anchor")

def animate(i):
	xdata.append(grouped_df2.shortdate[i])
	ydata.append(grouped_df2.totalcount[i])
	
	line.set_data(xdata, ydata)

	return line,


ani = animation.FuncAnimation(fig,animate,interval=1000,init_func=init)
ani.save('test_ani3.gif', writer='pillow')
# ani.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])


