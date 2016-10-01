import googlemaps
from datetime import datetime

class GeoConnector:
	OK_STATUS = 'OK'
	WALKING_MODE = 'walking'
	DRIVING_MODE = 'driving'
	MILES_TO_KM_RATIO = 0.6213

	def __init__(self, service_key):
		self.client = googlemaps.Client(service_key)

	def get_walking_deets(self, start_pt, end_pts):
		distance_matrix = self.client.distance_matrix(start_pt, end_pts, self.WALKING_MODE)

		# Check for error with API call
		if distance_matrix['status'] != self.OK_STATUS:
			return None, None

		pt_to_deets = {}
		for idx, result in enumerate(distance_matrix['rows'][0]['elements']):
			pt_to_deets[end_pts[idx]] = self._get_deets_from_result(result)
		return pt_to_deets

	def get_driving_deets(self, start_pts, end_pt):
		distance_matrix = self.client.distance_matrix(start_pts, end_pt, self.DRIVING_MODE)

		# Check for error with API call
		if distance_matrix['status'] != self.OK_STATUS:
			return None, None

		pt_to_deets = {}
		for idx, row in enumerate(distance_matrix['rows']):
			pt_to_deets[start_pts[idx]] = \
				self._get_deets_from_result(row['elements'][0])
		return pt_to_deets

	def _get_deets_from_result(self, result):
		# Check if it is possible to walk to this coordinate
		if result['status'] != self.OK_STATUS:
			return None, None

		# 'value' is in seconds
		travel_duration_mins = result['duration']['value'] / 60.0
		distance_meters = result['distance']['value']
		distance_miles = distance_meters / 1000.0 * self.MILES_TO_KM_RATIO

		# Truncate to 2 decimal places
		return {'mins': float('%.2f' % travel_duration_mins), \
				'miles': float('%.2f' % distance_miles)}
