# CurrencyTool
Tool for getting Exchange rate from fixer API 
[ Interview Task for Backend Developer Position ]
## Usage

First create database by running

    python database.py
Run test to make sure everything is ready

    python test_app.py
Then you are ready to use it, Examples:

    python app.py 
    python app.py -b EUR
    python app.py -b EUR -c USD
    python app.py -b EUR -c USD -d 2018-01-01
Note default value is -b EUR - c USD
(if Date is not set the default is the lastest data available from fixer.io)
## Install Guide

Install [Python3.6](https://askubuntu.com/a/865569).

Install [virtualenv](https://virtualenv.pypa.io/en/stable/installation/).

Create a new virtualenv called `my_env`: `virtualenv -p python3 my_env`.

Activate virtualenv : `source my_env/bin/activate`.

Install packages : `pip install -r requirements.txt`.

