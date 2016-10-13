import _mysql

DB_HOST = 'uberpricehistory.c2pcqvbwz3cq.us-west-2.rds.amazonaws.com'
DB_PORT = 3306
DB_USER = 'theboys'
DB_PASSWORD = 'quarterchub'
DB_DATABASE_NAME = 'uberprices'
DB_PRICES_TABLE = 'prices_history'

def main():
    db = _mysql.connect(host=DB_HOST,port=DB_PORT,user=DB_USER,passwd=DB_PASSWORD,db=DB_DATABASE_NAME)
    last_thirty_days_query = """SELECT AVG(min_price), STD(min_price), AVG(max_price), STD(max_price), HOUR(time), MINUTE(time)
               FROM prices_history WHERE date(time) < curdate() AND date(time) > curdate() - 30 GROUP BY HOUR(time), ROUND(MINUTE(time)/5);""" 
    db.query(last_thirty_days_query)
    last_thirty_days_result = db.store_result()
    all_rows = last_thirty_days_result.fetch_row(maxrows=0)
    print "Last 30 days data: ", all_rows
    
    todays_query = """SELECT min_price, max_price, HOUR(time), MINUTE(time) FROM prices_history WHERE date(time) = curdate();"""
    db.query(todays_query)
    todays_result = db.store_result()
    all_rows = todays_result.fetch_row(maxrows=0)
    print "Today's data: ", all_rows

if __name__ == '__main__':
    main()
