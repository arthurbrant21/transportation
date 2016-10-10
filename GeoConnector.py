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
		'''
		Returns a map where the keys are starting point coordinates and the
		values are the walking details to get from that starting point to the
		provided end point.

		Example of a key-value pair in this map:
		(123.1234, 63.1234): {"mins": 5, "miles": 0.3}

		If there is no way to walk from one of the starting points provided
		to the end point, it will not be included in the map.
		'''
		distance_matrix = self.client.distance_matrix(start_pt, end_pts, 
													  self.WALKING_MODE)

		# Check for error with API call
		if distance_matrix['status'] != self.OK_STATUS:
			return None

		pt_to_deets = {}
		for idx, element in enumerate(distance_matrix['rows'][0]['elements']):
			deets = self._get_deets_from_element(element)
			if deets:
				pt_to_deets[end_pts[idx]] = deets
		return pt_to_deets

	def get_driving_deets(self, start_pts, end_pt):
		'''
		Returns a map where the keys are starting point coordinates and the
		values are the driving details to get from that starting point to the
		provided end point.

		Example of a key-value pair in this map:
		(123.1234, 63.1234): {"mins": 10, "miles": 4.2}

		If there is no way to drive from one of the starting points provided
		to the end point, it will not be included in the map.
		'''
		distance_matrix = self.client.distance_matrix(start_pts, end_pt, 
												      self.DRIVING_MODE)

		# Check for error with API call
		if distance_matrix['status'] != self.OK_STATUS:
			return None

		pt_to_deets = {}
		for idx, row in enumerate(distance_matrix['rows']):
			deets = self._get_deets_from_element(row['elements'][0])
			if deets:
				pt_to_deets[start_pts[idx]] = deets
		return pt_to_deets

	def _get_deets_from_element(self, element):
		'''
		Given an element (defined in the Google Maps API response),
		will return an object of the following shape:
		{'mins': <mins to get to the destination>,
		 'miles': <miles to destination>}

		Returns None if the element does not hae a status of self.OK_STATUS
		'''
		# Check if it is possible to walk to this coordinate
		if element['status'] != self.OK_STATUS:
			return None

		# 'value' is in seconds
		travel_duration_mins = element['duration']['value'] / 60.0
		distance_meters = element['distance']['value']
		distance_miles = distance_meters / 1000.0 * self.MILES_TO_KM_RATIO

		# Truncate to 2 decimal places
		return {'mins': float('%.2f' % travel_duration_mins), \
				'miles': float('%.2f' % distance_miles)}
