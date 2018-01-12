import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String,Date,Float,UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class ExchangeRateModel(Base):
	__tablename__ = 'exchange_rate'
	id = Column(Integer, primary_key=True)
	base = Column(String(5),nullable=False)
	currency = Column(String(5),nullable=False)
	date = Column(Date)
	rate = Column(Float)
	# Make  sure we do n't have two same records
	__table_args__ =(UniqueConstraint('date','base','currency',name='_date_base_currency_uc'),)

engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.create_all(engine)
