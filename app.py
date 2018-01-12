import requests
import sys, getopt
from network import FixerAPI
import database_api
from database import ExchangeRateModel
from datetime import datetime,date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import ExchangeRateModel, Base
 
engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def main(argv):
	# initialization with default values
	base = 'EUR'
	currency = 'USD'
	date = ''
	# Commend line interface
	try:
		opts, args = getopt.getopt(argv,"hb:c:d:",["base","currency","date"])
	except getopt.GetoptError:
		print('app.py -b <base> -c <currency> -d <date>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('''Welcome to Fixer Api\n
usage: app.py [option] ... [-b] [-c] [-d] [arg] ..\n
-b <base> : Quote against a different currency by setting the base parameter.\n
-c <currency> : specific exchange rates by setting the currency parameter.\n
-d <date> : Format YYYY-MM-DD Get historical rates for any day since 1999.\n''')
			sys.exit()
		elif opt in ("-d","--date"):
			date= arg
		elif opt in ("-b", "--base"):
			base = arg.upper()
		elif opt in ("-c", "--currency"):
			currency = arg.upper()

	fixerAPI = FixerAPI()
	# Check if user enter specific date
	if date:
		dateQuery = formatDate(date)
		# Query Database to see if we had cache the same request
		rate = database_api.getRateForDate(session=session,base=base,currency=currency,date=dateQuery)
		# if rate is cached print it
		if rate:
			print(rate.rate)
		else:
			# otherwise make request to get data
			rate = fixerAPI.getExchangeRate(base=base,currency=currency,date=date)
			if rate['rates']:
				print(rate['rates'][currency])
				insertRate(rate)
			else:
				print("Error : %s Currency not found" %currency)
	else:
		# If no date enter request API with the lastest data avaiable 
		rate = fixerAPI.getExchangeRate(base=base,currency=currency);
		if rate['rates']:
			print(rate['rate'][currency])
			insertRate(rate)
		else:
			print("Error : %s Currency not found" %currency)

def insertRate(rate):
	# Query database to see if we had cache the same request before
	# create instant of date on YYYY-MM-DD format
	dateQuery = formatDate(rate['date'])
	base = rate['base']
	if rate['rates'].keys():
		currency = list(rate['rates'].keys())[0]
		rateValue = rate['rates'][currency]
		rateQuery = database_api.getRateForDate(session=session,base=base,currency=currency,date=dateQuery)
		if not rateQuery:
			# Save the rate response in database
			rateModel = ExchangeRateModel(base=base,currency=currency,date=dateQuery,rate=rateValue)
			database_api.insert(session=session,model=rateModel)

def formatDate(date):
	return datetime.strptime(date,'%Y-%m-%d').date()

if __name__ == "__main__":
	main(sys.argv[1:])
