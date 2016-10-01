import googlemaps
from datetime import datetime

class GeoConnector:
	OK_STATUS = 'OK'
	WALKING_MODE = 'walking'
	DRIVING_MODE = 'driving'
	MILES_TO_KM_RATIO = 0.6213

	def __init__(self, service_key):
		self.client = googlemaps.Client(service_key)

	def get_dist(self, start_pt, end_pt, mode):
		'''Get the distance from start_pt to end_pt. Mode must either be
		WALKING_MODE or DRIVING_MODE. If traveling between the two points is not
		possible, None is returned. Returns a 2 element tuple where the first
		element is the travel duration in minutes and the 2nd is the distance in
		miles.
		'''
		if mode != self.WALKING_MODE and mode != self.DRIVING_MODE:
			print 'Invalid mode: ' + mode
			return None

		distance_matrix = self.client.distance_matrix(start_pt, end_pt, mode)

		# Check for error with API call
		if distance_matrix['status'] != self.OK_STATUS:
			return None

		result = distance_matrix['rows'][0]['elements'][0]

		# Check if it is possible to walk to this coordinate
		if result['status'] != self.OK_STATUS:
			return None

		# 'value' is in seconds
		travel_duration_mins = result['duration']['value'] / 60.0
		distance_meters = result['distance']['value']
		distance_miles = distance_meters / 1000.0 * self.MILES_TO_KM_RATIO

		# Truncate to 2 decimal places
		return (float('%.2f' % travel_duration_mins), 
			    float('%.2f' % distance_miles))