import googlemaps
from datetime import datetime

class GeoConnector:
	OK_STATUS = 'OK'
	WALKING_MODE = 'walking'
	MILES_TO_KM_RATIO = 0.6213

	def __init__(self, service_key):
		self.client = googlemaps.Client(service_key)

	def get_driving_time(self, start_pt, end_pt):
		return 0

	def get_walking_dist(self, start_pt, end_pt):
		'''Get the walking distance from start_pt to end_pt.
		If walking between the two points is not possible, None is returned.
		Returns a 2 element tuple where the first element is the travel duration in
		minutes and the 2nd is the distance in miles.
		'''
		distance_matrix = self.client.distance_matrix(start_pt, end_pt, self.WALKING_MODE)

		# Check for error with API call
		if distance_matrix['status'] != self.OK_STATUS:
			return None

		result = distance_matrix['rows'][0]['elements'][0]

		# Check if it is possible to walk to this coordinate
		if result['status'] != self.OK_STATUS:
			return None

		travel_duration_mins = result['duration']['value'] / 60.0 # value is in seconds
		distance_meters = result['distance']['value']
		distance_miles = distance_meters / 1000.0 * self.MILES_TO_KM_RATIO

		return travel_duration_mins, distance_miles