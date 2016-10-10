import datetime
from pytz import timezone
import sys
from UberConnector import UberConnector
import _mysql

UBER_SERVER_TOKEN = '7x_AZ2eWSn7nIekfylveYt3Hgb0juotM1JaPoawG'
START_POINT = (37.403675, -122.057824)
END_POINT = (37.421264, -122.211321)
TIMEZONE = 'US/Pacific'
START_HOUR = 6
END_HOUR = 9

DB_HOST = 'uberpricehistory.c2pcqvbwz3cq.us-west-2.rds.amazonaws.com'
DB_PORT = 3306
DB_USER = 'theboys'
DB_PASSWORD = 'quarterchub'
DB_DATABASE_NAME = 'uberprices'
DB_PRICES_TABLE = 'prices_history'


def main():
	pacific = timezone(TIMEZONE)
	now = datetime.datetime.now(pacific)
	if now.hour < START_HOUR or now.hour > END_HOUR:
		sys.exit(0)

	uber_connector = UberConnector(UBER_SERVER_TOKEN)
	min_price, max_price = uber_connector.get_min_and_max(START_POINT, END_POINT, 'POOL')

	db = _mysql.connect(host=DB_HOST,port=DB_PORT,user=DB_USER,passwd=DB_PASSWORD,db=DB_DATABASE_NAME)
	data = {'year': now.year,
	        'month': now.month,
	        'day': now.day,
	        'hour': now.hour,
	        'minute': now.minute,
	        'second': now.second,
	        'minprice': min_price,
	        'maxprice': max_price,
	        'table': DB_PRICES_TABLE,
	        'latstart': START_POINT[0],
	        'longstart': START_POINT[1],
	        'latend': END_POINT[0],
	        'longend': END_POINT[1]}

	query = "INSERT INTO %(table)s VALUES (%(latstart)s, %(longstart)s, \'%(year)s:%(month)s:%(day)s %(hour)s:%(minute)s:%(second)s\', %(minprice)s, %(maxprice)s, %(latend)s, %(longend)s);" % data
	db.query(query)

if __name__ == '__main__':
    main()