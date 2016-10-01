import numpy as np

class NearPoints:

	def __init__(self, lat, lon):
		"""Helper class to find nearby points.

		The MVP will blindly find points in a circle. Subsequent
		editions should be more intelligent, finding key landmarks,
		only walking through safe spaces, etc.

		Known limitations: We do not expect this to work at the poles
		or near the international date line.

		The sunflower algorithm is inspired by 
		http://stackoverflow.com/questions/28567166/uniformly-distribute-x-points-inside-a-circle

		Args:
			lat: latittude of the epicenter.
			lon: longitude of the epicenter.
		"""
		self.lat = lat
		self.lon = lon

	def _radius(self, k, num_points, b):
		"""
		Args:
		k: current point being written.
		num_points: total number of points.
		b: number of non perimiter points.
		"""
		if k > (num_points - b):
			return 1
		else:
		    return np.sqrt(k-1/2) / np.sqrt(num_points-(b+1)/2)

	def get_nearby_points(self, num_points, max_radius, alpha=1):
		"""Finds specified number of nearby points within radius.

		The returned points are currently spread out uniformly within
		the constrains of the radius.

		Args:
		num_points: number of points to be returned.
		max_radius: max distance a point can lie from epicenter.
		alpha: uniformity of the points.

		Returns:
		iterable of n (lat,long) points.
		"""
		nearby_points = []

		b = int(max_radius * np.sqrt(num_points))
		phi = (np.sqrt(5)+1)/2
		for k in range(1, num_points+1):
			r = self._radius(k,num_points,b)
			theta = 2*np.pi*k/phi**2
			nearby_points.append((r*np.cos(theta), r*np.sin(theta)))

		return [(self.lat + lat * max_radius, self.lon + lon * max_radius) for lat,lon in nearby_points]