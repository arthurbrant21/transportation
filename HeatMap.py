import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PickupDeets import PickupDeets



class HeatMap:

	GRANULARITY = 100

	def __init__(self, loc_to_pickup_deets):

		def _get_price(deets):
			return np.mean([deets.max_price, deets.min_price])


		def _scale_factor():
			"""
			Returns:
				min_score 
				scaling factor to scale adjusted numbers by
			"""
			return 0, 2
			# scores = [_get_price(deets) for _, deets in loc_to_pickup_deets.iteritems()]
			# min_score = min(scores)
			# adjusted = [score - min_score for score in scores]
			# max_adjusted = max(adjusted)
			# if not max_adjusted:
			#	max_adjusted = 1
			# return min_score, self.GRANULARITY * 1.0 / max_adjusted

		min_score, scale_factor = _scale_factor()
		self.x = []
		self.y = []
		for loc, deets in loc_to_pickup_deets.iteritems():
			x, y = loc[0], loc[1]
			freq = int((_get_price(deets) - min_score) * scale_factor)
			self.x += [x] * freq
			self.y += [y] * freq
			print freq


	def show(self):
		heatmap, xedges, yedges = np.histogram2d(self.x, self.y, bins=50)
		extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

		plt.clf()
		plt.imshow(heatmap, extent=extent)
		plt.show()