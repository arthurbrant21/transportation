import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


class HistoryVisualizer():

	def get_history(self):
		history = {}
		history[(6,0)] = (5,7)
		history[(6,10)] = (5,7)
		history[(6,20)] = (5,7)

		history[(7,0)] = (5,8)
		history[(7,10)] = (5,8)
		history[(7,20)] = (5,9)

		history[(8,0)] = (5,10)
		history[(8,10)] = (5,20)
		history[(8,20)] = (5,20)
		return history

	def get_today(self):
		today = {}

		today[(6,0)] = (5,20)
		today[(6,10)] = (5,20)
		today[(6,20)] = (5,25)

		today[(7,0)] = (5,15)
		today[(7,10)] = (5,5)
		today[(7,20)] = (5,7)
		return today

	def visualize(self, history, today):
		"""
		Args:
			history:
				dict with keys = (hour, minute) and val = (avg min, avg max) price.
		"""
		# First, we order by hour and minute.
		history = self.get_history()
		today = self.get_today()

		# data values.
		history_list = sorted(history.items(), key=lambda x: x[0])
		today_list = sorted(today.items(), key=lambda x: x[0])
		historical_avgs = [np.mean([time_and_price[1][0], time_and_price[1][1]]) for time_and_price in history_list]
		today_avgs = [np.mean([time_and_price[1][0], time_and_price[1][1]]) for time_and_price in today_list]

		# x axis.
		my_xticks = ["%s:%s" % (time_and_price[0][0], time_and_price[0][1]) for time_and_price in history_list]
		x = np.array(range(len(history_list)))
		plt.xticks(x, my_xticks)

		# y axis.
		axes = plt.gca()
		price_min = min(min(historical_avgs), min(today_avgs))
		price_max = max(max(historical_avgs), max(today_avgs))
		axes.set_ylim([max(0, price_min - 2), price_max + 2])

		# legend.
		historical_legend = mpatches.Patch(color='b', label='historical')
		today_legend = mpatches.Patch(color='r', label='today')
		plt.legend(handles=[historical_legend, today_legend])

		# plot lines.
		plt.plot(range(len(history_list)), historical_avgs, 'b', label="historical")
		plt.plot(range(len(today_list)), today_avgs, 'r', label="today")

		plt.show()
