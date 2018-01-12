import unittest
from app import formatDate
from datetime import date
import database_api
from sqlalchemy import create_engine
from database import ExchangeRateModel,Base
from sqlalchemy.orm import sessionmaker

class DateTestCases(unittest.TestCase):

	def test_date(self):
		self.assertEqual(date(2018,1,1),formatDate("2018-01-01"))
		self.assertEqual(date(2018,9,2),formatDate("2018-9-02"))
		self.assertEqual(date(2018,8,2),formatDate("2018-8-02"))
		self.assertEqual(date(2017,11,1),formatDate("2017-11-1"))


class DatabaseTestCases(unittest.TestCase):
	engine = create_engine('sqlite:///test_rate.db')
	Base.metadata.create_all(engine)
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	model = ExchangeRateModel(base='USD',currency='EUR',date=date(2018,1,1),rate=2.1)

	@classmethod
	def setUpClass(cls):
		cls.session.add(cls.model)
		cls.session.commit()
	
	@classmethod
	def tearDownClass(cls):
		Base.metadata.drop_all(cls.engine)

	def test_query_rate(self):
		result = database_api.getRateForDate(session = self.session,base=self.model.base,currency=self.model.currency,date=self.model.date)
		self.assertEqual(self.model,result)

	def test_insert_rate(self):
		model = ExchangeRateModel(base='USD',currency='EUR',date=date(2018,1,2),rate=2.1)
		database_api.insert(self.session,model)
		result = database_api.getRateForDate(session = self.session,base=model.base,currency=model.currency,date=model.date)
		self.assertEqual(model,result)


if __name__ == '__main__':
	unittest.main()