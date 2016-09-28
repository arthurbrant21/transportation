import numpy as np

class NearPoints:

	def __init__(self, lat, lon):
		self.lat = lat
		self.lon = lon

	def _radius(self, k, num_points, b):
		if k > (num_points - b):
			return 1
		else:
		    return np.sqrt(k-1/2) / np.sqrt(num_points-(b+1)/2)

	def get_nearby_points(self, num_points, max_radius, alpha=1):

		nearby_points = []

		b = int(max_radius * np.sqrt(num_points))
		phi = (np.sqrt(5)+1)/2
		for k in range(1, num_points+1):
			r = self._radius(k,num_points,b)
			theta = 2*np.pi*k/phi**2
			nearby_points.append((r*np.cos(theta), r*np.sin(theta)))

		return [(self.lat + lat * max_radius, self.lon + lon * max_radius) for lat,lon in nearby_points]