import numpy as np

class PickupDeets:

	PRICE_WEIGHT = 20
	WALKING_TIME_WEIGHT = 3
	DRIVING_TIME_WEIGHT = 1

	def __init__(self,
				 min_price=None,
				 max_price=None,
				 walking_time_mins=None,
				 walking_distance_miles=None,
			     driving_time_mins=None,
				 driving_distance_miles=None,
				 wait_time=None):
		"""Cost is an aritrary unit that we desire to minimize.

		Args:
			min_price: minimum price of ride.
			max_price: maximum price of ride.
			walking_time_mins: time to walk to uber pickup location.
			walking_distance_miles: distance to walk to pickup
			driving_time_mins: time spent in uber to destination.
			driving_distance_miles: distance to drive.
			wait_time: time spent between arrival at walking and uber pickup.
		"""
		self.min_price = min_price
		self.max_price = max_price
		self.walking_time_mins = walking_time_mins
		self.walking_distance_miles = walking_distance_miles
		self.driving_time_mins = driving_time_mins
		self.driving_distance_miles = driving_distance_miles
		self.wait_time = wait_time

	def is_valid(self):
		"""Indicator for validity of a point. For example, if a point is in the
			water, we assume that its walking_time_mins is None and thus will
			return invalid.
		"""
		return (self.min_price
				and self.max_price
				and self.walking_time_mins
				and self.walking_distance_miles
				and self.driving_time_mins
				and self.driving_distance_miles)

	def get_cost(self):
		price = np.mean([self.max_price, self.min_price])
		return self.PRICE_WEIGHT * price + self.WALKING_TIME_WEIGHT * self.walking_time_mins + self.DRIVING_TIME_WEIGHT * self.driving_time_mins
