import datetime
from pytz import timezone
import sys
from UberConnector import UberConnector

FILEPATH = "/tmp/a.csv"
# This will not work for even numbers, must fix logic.
BUCKET_SIZE = 5
UBER_SERVER_TOKEN = '7x_AZ2eWSn7nIekfylveYt3Hgb0juotM1JaPoawG'
START_POINT = (37.403675, -122.057824)
END_POINT = (37.421264, -122.211321)
TIMEZONE = 'US/Pacific'
START_HOUR = 6
END_HOUR = 9


def get_bucket_minute(minute, second):
	remainder = minute % BUCKET_SIZE
	if remainder < (BUCKET_SIZE / 2):
		bucket_minute = minute - remainder
	elif remainder == 2:
		if second <  30:
			bucket_minute = minute - remainder
		else:
			bucket_minute = minute - remainder + BUCKET_SIZE
	else:
		bucket_minute = bucket_minute = minute - remainder + BUCKET_SIZE

	if bucket_minute == 60:
		bucket_minute = 0
	return bucket_minute

def main():
	pacific = timezone(TIMEZONE)
	now = pacific.localize(datetime.datetime.now())
	if now.hour < START_HOUR or now.hour > END_HOUR:
		sys.exit(0)
	minute = get_bucket_minute(now.minute, now.second)

	uber_connector = UberConnector(UBER_SERVER_TOKEN)
	min_price, max_price = uber_connector.get_min_and_max(START_POINT, END_POINT, 'POOL')


	with open(FILEPATH, 'a') as f:
		f.write(','.join([str(now.year),
						  str(now.month),
						  str(now.day),
						  str(now.hour),
						  str(minute),
						  str(min_price),
						  str(max_price)]))
		f.write('\n')

if __name__ == '__main__':
    main()