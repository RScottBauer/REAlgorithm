"""
Database Backed ERV Solution
Robert Bauer 1/7/2019
"""

#importing packages
from pymongo import MongoClient
import datetime as dt
#Database Conneciton
client = MongoClient(port=27017)
db = client.Housing

"""
variables
Locdata
    Zip - zip code
    InsRate - Insurance Rate
    VacancyMonths - Estimated Number of Months Vacant Each year
    PropTax - Prop Tax rate

Propdata
    id - prop id
    Zip - zip code
    price - market price or expected sale price
    rent - expected rent
    proptaxappraisal - current tax appraisal

Fixed Data
    apr - loan apr
    morttype - fixed,variable
    mortfee - fee for mortgage
    mortpoints - mortgage points charged by bank
    inflaiton - estimated national inflation
    marginofsaftey - personal saftey rate
    downpayment - percent of sales price as a down payment
    managementfee - general rate for property management
"""
#DefinedVariables
vacancy = 1
insrate = 0.05
apr = 0.05
morttype = "fixed"
mortpoints = 0.02
inflation = 0.03
marginofsaftey = 0.25
downpayment = 0.1
managementfee = 0.1
#function start
def ERV(propid, rent, price, proptaxdate, proptaxfrequency, proptaxrate, proptaxappraisal, insrate, zip):

    currentyear = dt.datetime.now().year
    currentmonth = dt.datetime.now().month
    currentday = dt.datetime.now().month
    if currentmonth > 10
        firstmonth = (currentmonth + 2) % 12
        firstyear = currentyear + 1
    else
        firstmonth = currentmonth + 2
        firstyear = currentyear

    
