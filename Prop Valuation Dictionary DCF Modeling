"""
Databased Function for Determining Expected Real Value
"""

#importing packages
from pymongo import MongoClient

#Database Conneciton
client = MongoClient(port=27017)
db = client.Housing

#function start
def ERV(price, expectedrent, propid):

#variables defining
    marketprice = price
    rent = expectedrent
    apr = intrate #loan apr
    mortlength = mortyears #Number of years on the mortgage
    downpaymentpercentage =  #your downpayment percentage
    mortgagepoints = 0.02 #Percentage of Mortgage charged by lender at time of loan
    mortgagefee = 500 #Paperwork and other one time fees charged by lender
    inflation = 0.03 #rate of inflation yearly
    expensegrowth = 0.02 #rate of exense growth yearly
    incomegrowth = 0.02 #rate of income growth yearly
    vacancy = 1 #How many months of the year is this property vacant?
    closingcost = 2500 #"cost to close the property typically around $2500"
    repaircost = 5000 #"cost to bring the property into working condition amortized with market price"
    HOAfee = 0#"annual sum of HOA fees"
    bills = 200 #montly utility and upkeep bills
    othermonthly = 0 #"monthly fees i havent thought of"
    insurance = 150 #"monthly home insurance and other insurance"
    proptaxdate = 4 #Month of first property tax payment of the year
    proptaxfrequency = 6 #How many months between property tax payments
    requiredrate = 0.20 #investors required rate of return

#Derived Variables
    numberofmonths = 12*mortlength
    downpayment = marketprice * downpaymentpercentage
    mortgageammount = marketprice * (1-downpaymentpercentage)
    monthlyapr = apr/12
    monthlymortgage = mortgageammount*(monthlyapr*((1+monthlyapr)**(numberofmonths)))/(((1+monthlyapr)**(numberofmonths))-1) #"mortgage ammount"
    totalmortfee = mortgagefee + (mortgagepoints*mortgageammount)
    mortinsurance = (0.005*mortgageammount)/12
    capx = 12*(rent*0.08)
    propmanagefee = rent*.10
    monthlyhoafee = HOAfee/12
    monthlycapx = capx/12
    unrentedfee = ((bills+propmanagefee)*0.5) #"sum of montly fees when the property is vacant"
    normmonth = bills + propmanagefee + insurance + monthlycapx + monthlyhoafee + othermonthly + mortinsurance + monthlymortgage
    depreciation = ((marketprice*0.75)+repaircost+closingcost)/27.5 #Federal Straitline Depreciation with land value removed
    proptax = (marketprice+repaircost)*0.8*0.02 #"annual property tax"
    semiprop = proptax/2 #semi annual property tax due
    discountrate = requiredrate + inflation
    monthlydiscount = ((discountrate+1)**(1/12))-1
    taxnormmonth = bills + propmanagefee + insurance + monthlycapx + monthlyhoafee + othermonthly + mortinsurance
    quarterly = (depreciation + proptax + (taxnormmonth*(12-vacancy)) + (unrentedfee*(vacancy)))/4
    taxincome = (rent*(12-vacancy))/4

#Mortgage Calculation (Change out for table based calculation)

#Construct Dates for CF Dictionary
    currentdate = "Current Date Function"
    purchasedate = currentdate + "2 months"
    cashflows = {"MMYY":"Cashflow"}

#populating the CF Dictionary
    bills = "Unavoidable monthly costs (insurance, propertytax, etc.)"
    pdatecf = {"MMYY":"mortgage-price-mortgagefee-closingfee-repaircost-bills"}

ERV(200000, 3000, 123)
