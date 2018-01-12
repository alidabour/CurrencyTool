from database import ExchangeRateModel
 
# helper fun to insert in database
def insert(session,model):
	session.add(model)
	session.commit()

# query db by base & currency & date
def getRateForDate(session,base,currency,date):
	# print("database loading...")
	rateModel = session.query(ExchangeRateModel).filter(ExchangeRateModel.base==base,
		ExchangeRateModel.currency==currency,ExchangeRateModel.date==date).first()
	return rateModel