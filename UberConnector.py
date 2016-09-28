from uber_rides.session import Session
from uber_rides.client import UberRidesClient

class UberConnector:

	def __init__(self, service_key):
		self.service_key = service_key
		session = Session(server_token=service_key)
		self.client = UberRidesClient(session)

	def get_min_and_max(self, start_pt, end_pt):
		response = self.client.get_price_estimates(start_pt[0], start_pt[1], end_pt[0], end_pt[1])
		products = response.json
		# print json.dumps(products,
		# 			 indent=4,
		# 			 sort_keys=True)
		return products["prices"][1]["low_estimate"], products["prices"][1]["high_estimate"]