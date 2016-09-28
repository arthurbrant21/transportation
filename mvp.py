from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import json
import re
from NearPoints import NearPoints


UBER_SERVER_TOKEN = '7x_AZ2eWSn7nIekfylveYt3Hgb0juotM1JaPoawG'
START_POINT = (37.77, -122.41)
END_POINT = (37.81, -122.41)
NUM_NEIGHBOR_POINTS = 5
RADIUS = .02

def main():
	near_points = NearPoints(START_POINT[0], START_POINT[1])
	pts = near_points.get_nearby_points(NUM_NEIGHBOR_POINTS, RADIUS)
	session = Session(server_token=UBER_SERVER_TOKEN)
	client = UberRidesClient(session)
	prices = set()
	for pt in pts:
		response = client.get_price_estimates(pt[0], pt[1], END_POINT[0], END_POINT[1])
		products = response.json
		price = products["prices"][1]["estimate"]
		# TODO(arthurbrant) make this more robust.

		m = re.search('\$([0-9]*)-([0-9]*)', price)
		min_price = float(m.group(1))
		max_price = float(m.group(2))
		prices.add((min_price, max_price))

	for price in prices:
		print price
	# print json.dumps(products,
	# 				 indent=4,
	# 				 sort_keys=True)


if __name__ == '__main__':
    main()