import numpy as np

class NearPoints:
	MILES_PER_LAT_DEGREE = 68.6863716
	MILES_PER_LONG_DEGREE_AT_EQUATOR = 69.1710411

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

		# Convert distance in miles to degrees difference (this conversion
		# is different for latitude and longitude)
		return [(self.lat + self._convert_vertical_dist_to_lat(dist_y * \
			     max_radius), self.lon + \
				 self._convert_horizontal_dist_to_longitude(self.lat, dist_x * max_radius)) \
				 for dist_y,dist_x in nearby_points]

	def _convert_vertical_dist_to_lat(self, vertical_dist_miles):
		'''Converts a given distance (in miles) to its equivalent value
		in latidude degrees.

		See https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-km-distance/1253545#1253545

		Args:
		vertical_dist_miles: distance in miles going north/south
		'''
		return vertical_dist_miles / self.MILES_PER_LAT_DEGREE

	def _convert_horizontal_dist_to_longitude(self, current_latitude, 
											  horizontal_dist_miles):
		'''Converts a given distance (in miles) to its equivalent value
		in longitude degrees.

		See https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-km-distance/1253545#1253545

		Args:
		current_latitude: current latitude degrees
		horizontal_dist_miles: distance in miles going east/west
		'''
		return horizontal_dist_miles / self.MILES_PER_LONG_DEGREE_AT_EQUATOR \
			* np.cos(current_latitude)


