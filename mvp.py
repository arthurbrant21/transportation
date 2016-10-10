from NearPoints import NearPoints
from UberConnector import UberConnector
from GeoConnector import GeoConnector
from PickupDeets import PickupDeets
from HeatMap import HeatMap

import threading
import math

UBER_SERVER_TOKEN = '7x_AZ2eWSn7nIekfylveYt3Hgb0juotM1JaPoawG'
GEO_SERVER_TOKEN = 'AIzaSyB1uLNtaLr9V8nGj0E9EfYa2-S2ilEac7I'
START_POINT = (37.77, -122.41)
END_POINT = (37.81, -122.41)

NUM_NEIGHBOR_POINTS = 5
RADIUS_MILES = 1
NUM_THREADS = 5


def get_prices(uber_connector, loc_to_pickup_deets):
	def _get_shards_prices(shard):
		for pt in shard:
			min_price, max_price = uber_connector.get_min_and_max(pt, END_POINT)
			loc_to_pickup_deets[pt].min_price = min_price
			loc_to_pickup_deets[pt].max_price = max_price

	pts = loc_to_pickup_deets.keys()
	shard_size = int(math.ceil(len(pts) / float(NUM_THREADS)))
	threads = []
	for shard_index in range(NUM_THREADS):
		shard = pts[shard_index * shard_size : (shard_index+1) * shard_size]
		if not shard:
			continue
		t = threading.Thread(group = None, target = _get_shards_prices, args = [shard])
		threads.append(t)
		t.start()
	for thread in threads:
		thread.join()

def get_walking_deets(geo_connector, loc_to_pickup_deets):
	loc_to_walking_deets = \
		geo_connector.get_walking_deets(START_POINT, loc_to_pickup_deets.keys())
	for pt, walking_deets in loc_to_walking_deets.iteritems():
		loc_to_pickup_deets[pt].walking_time_mins = walking_deets['mins']
		loc_to_pickup_deets[pt].walking_distance_miles = walking_deets['miles']

def	get_driving_deets(geo_connector, loc_to_pickup_deets):
	loc_to_driving_deets = \
		geo_connector.get_driving_deets(loc_to_pickup_deets.keys(), END_POINT)
	for pt, driving_deets in loc_to_driving_deets.iteritems():
		loc_to_pickup_deets[pt].driving_time_mins = driving_deets['mins']
		loc_to_pickup_deets[pt].driving_distance_miles = driving_deets['miles']

def	filter_non_complete_deets(loc_to_pickup_deets):
	return {pt: deets for pt, deets in loc_to_pickup_deets.iteritems() if deets.is_valid()}

def main():
	near_points = NearPoints(START_POINT[0], START_POINT[1])
	uber_connector = UberConnector(UBER_SERVER_TOKEN)
	geo_connector = GeoConnector(GEO_SERVER_TOKEN)
	pts = near_points.get_nearby_points(NUM_NEIGHBOR_POINTS, RADIUS_MILES)
	loc_to_pickup_deets = {pt: PickupDeets() for pt in pts}
	get_prices(uber_connector, loc_to_pickup_deets)
	get_walking_deets(geo_connector, loc_to_pickup_deets)
	get_driving_deets(geo_connector, loc_to_pickup_deets)

	loc_to_pickup_deets = filter_non_complete_deets(loc_to_pickup_deets)
	location_to_cost = {}
	for pt in loc_to_pickup_deets:
		location_to_cost[pt] = loc_to_pickup_deets[pt].get_cost()
	location, cost = min(location_to_cost.items(), key=lambda x: x[1]) 
	print location, cost

	HeatMap(loc_to_pickup_deets).show()

if __name__ == '__main__':
    main()