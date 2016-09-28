import googlemaps
from datetime import datetime

class GeoConnector:
	OK_STATUS = 'OK'
	WALKING_MODE = 'walking'

	def __init__(self, service_key):
		self.client = googlemaps.Client(service_key)

	def get_driving_time(self, start_pt, end_pt):
		return 0

	def get_walking_dist(self, start_pt, end_pt):
		distance_matrix = self.client.distance_matrix(start_pt, end_pt, self.WALKING_MODE)

		# Check for error with API call
		if distance_matrix['status'] != self.OK_STATUS:
			return 0, False

		result = distance_matrix['rows'][0]['elements'][0]

		# Check if it is possible to walk to this coordinate
		if result['status'] != self.OK_STATUS:
			return 0, False

		distance_in_mins = result['duration']['value'] / 60.0 # value is in seconds

		return distance_in_mins, True