import json
from NearPoints import NearPoints
from UberConnector import UberConnector
from GeoConnector import GeoConnector
import numpy as np

UBER_SERVER_TOKEN = '7x_AZ2eWSn7nIekfylveYt3Hgb0juotM1JaPoawG'
GEO_SERVER_TOKEN = 'AIzaSyB1uLNtaLr9V8nGj0E9EfYa2-S2ilEac7I'
START_POINT = (37.77, -122.41)
END_POINT = (37.81, -122.41)
NUM_NEIGHBOR_POINTS = 5
RADIUS = .01 # in lat long units.

PRICE_WEIGHT = 20
WALKING_TIME_WEIGHT = 3
DRIVING_TIME_WEIGHT = 1

def cost_function(min_price,
				  max_price,
				  walking_time_mins,
				  walking_distance_miles,
				  driving_time_mins,
				  driving_distance_miles,
				  wait_time = 0):
	"""Cost is an aritrary unit that we desire to minimize.

	Args:
		min_price: minimum price of ride.
		max_price: maximum price of ride.
		walking_time: time to walk to uber pickup location.
		driving_time: time spent in uber to destination.
		wait_time: time spent between arrival at walking and uber pickup.

	Returns:
		cost of the trip.
	"""
	price = np.mean([max_price, min_price])
	return PRICE_WEIGHT * price + WALKING_TIME_WEIGHT * walking_time_mins + DRIVING_TIME_WEIGHT * driving_time_mins


def main():
	near_points = NearPoints(START_POINT[0], START_POINT[1])
	uber_connector = UberConnector(UBER_SERVER_TOKEN)
	geo_connector = GeoConnector(GEO_SERVER_TOKEN)
	pts = near_points.get_nearby_points(NUM_NEIGHBOR_POINTS, RADIUS)
	location_to_cost = {}
	for pt in pts:
		min_price, max_price = uber_connector.get_min_and_max(pt, END_POINT)
		(walking_time_mins,
		 walking_distance_miles) = geo_connector.get_walking_time(START_POINT,
		 												  pt)
		if not walking_time_mins:
			continue
		driving_time_mins, driving_distance_miles = geo_connector.get_driving_time(pt, 
																		 END_POINT)
		if not driving_time_mins:
			continue

		cost = cost_function(min_price,
							 max_price,
							 walking_time_mins,
							 walking_distance_miles,
							 driving_time_mins,
							 driving_distance_miles)
		location_to_cost[pt] = cost

	location, cost = min(location_to_cost.items(), key=lambda x: x[1]) 
	print location, cost

if __name__ == '__main__':
    main()