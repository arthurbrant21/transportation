import json
from NearPoints import NearPoints
from UberConnector import UberConnector
from GeoConnector import GeoConnector

UBER_SERVER_TOKEN = '7x_AZ2eWSn7nIekfylveYt3Hgb0juotM1JaPoawG'
GEO_SERVER_TOKEN = 'TODO'
START_POINT = (37.77, -122.41)
END_POINT = (37.81, -122.41)
NUM_NEIGHBOR_POINTS = 5
RADIUS = .02

def get_walking_dist():
	# Use google maps to get walking dist between the two points.
	return 0

def get_drive_time():
	# Use google maps to get the driving time
	return 0

def main():
	near_points = NearPoints(START_POINT[0], START_POINT[1])
	uber_connector = UberConnector(UBER_SERVER_TOKEN)
	geo_connector = GeoConnector(GEO_SERVER_TOKEN)
	pts = near_points.get_nearby_points(NUM_NEIGHBOR_POINTS, RADIUS)
	prices = set()
	for pt in pts:
		min_price, max_price = uber_connector.get_min_and_max(pt, END_POINT)
		walking_time = geo_connector.get_walking_dist(START_POINT, pt)
		drive_time = geo_connector.get_driving_time(pt, END_POINT)
		#TODO(arthurbrant) use cost function
		prices.add((min_price, max_price))

	for price in prices:
		print price



if __name__ == '__main__':
    main()