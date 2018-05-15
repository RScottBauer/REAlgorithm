# -*- coding: utf-8 -*-
"""
Created on Fri May 11 16:43:01 2018

@author: Scott Bauer
"""

#Discounted Cashflow Model for Pricing Rental Properties
#Any Vlaues can be Changed, Descriptions provided for possibly unclear variables
#Expected Price to Buy Property At
marketprice = 200000#"This will come from the property database"
paidprice = 150000#"price I expect to pay for the property"
ARV = 225000#"After Repair Value (Unkown if usefull)"
#Expected Rent - the expected rent the property will bring in monthly
rent = 3000#"This will come from the rental algorithm"


#Mortgage Info
apr = .0485
mortlength = 30 #Number of years on the mortgage
numberofmonths = 12*mortlength
downpaymentpercentage = 0.1
downpayment = marketprice * downpaymentpercentage
monthlyapr = apr/12
mortgageammount = marketprice * (1-downpaymentpercentage)
monthlymortgage = mortgageammount*(monthlyapr*((1+monthlyapr)**(numberofmonths)))/(((1+monthlyapr)**(numberofmonths))-1) #"mortgage ammount"
mortgagepoints = 0.02 #Percentage of Mortgage charged by lender at time of loan
mortgagefee = 500 #Paperwork and other one time fees charged by lender
totalmortfee = mortgagefee + (mortgagepoints*mortgageammount)
mortinsurance = (0.005*mortgageammount)/12
resamortize = 30 #Number of years to amortize residentail property
commamortize = 20 #Number of years to amortize commercial property

#Growth Rates
inflation = 0.03
expensegrowth = 0.02
incomegrowth = 0.02
propgrowth = 0.04 #"rate of appreciation of property value"

#Property Rates
vacancy = 1 #How many months of the year is this property vacant?


#One time Fees
closingcost = 2500 #"cost to close the property typically around $2500"
repaircost = 5000 #"cost to bring the property into working condition amortized with market price"

#Expected Annual and Semi-Annual Costs
capx = 12*(rent*0.08)#"expected yearly capx"
HOAfee = 0#"annual sum of HOA fees"

#Expected Monthly Costs
propmanagefee = rent*.10#monthly fee for property manager
bills = 200 #montly utility and upkeep bills
othermonthly = 0 #"monthly fees i havent thought of"
monthlyhoafee = HOAfee/12
monthlycapx = capx/12
unrentedfee = ((bills+propmanagefee)*0.5) #"sum of montly fees when the property is vacant"
insurance = 75 #"monthly home insurance and other insurance"

#Expected Taxes
depreciation = ((marketprice*0.75)+repaircost+closingcost)/27.5 #Federal Straitline Depreciation with land value removed
proptax = (marketprice+repaircost)*0.8*0.02 #"annual property tax"
semiprop = proptax/2 #semi annual property tax due
taxnormmonth = bills + propmanagefee + insurance + monthlycapx + monthlyhoafee + othermonthly + mortinsurance + monthlymortgage*0.75
quarterly = (depreciation + proptax + (taxnormmonth*11) + unrentedfee)/4
taxincome = (rent*11)/4
fedtaxnet = (taxincome - quarterly)*0.8*0.35

#Dates
proptaxdate = 4 #Month of first property tax payment of the year
proptaxfrequency = 6 #How many months between property tax payments


#Required Discount Rates
requiredrate = 0.20 #investors required rate of return
discountrate = requiredrate + inflation
monthlydiscount = ((discountrate+1)**(1/12))-1

#Now the actual Calculation

#presets
year = 0
value = 0
fedtax = 0
n=1
normmonth = bills + propmanagefee + insurance + monthlycapx + monthlyhoafee + othermonthly + mortinsurance + monthlymortgage
while n <= numberofmonths:
    #Year Counter
    if n % 12 == 0:
        year += 1
    #Removing number of vacant months per year
    if n-(12*year) == (12-vacancy):
        vacancycost = -1*(rent+unrentedfee)*vacancy
    else:
        vacancycost = 0
    #Quarterly Federal Estimted Tax Payments
    if n-(12*year) == 1 or n-(12*year) == 4 or n-(12*year) == 7 or n-(12*year) == 10:
        fedtax = fedtaxnet
    else:
        fedtax = 0
    #Twice Yearly Property Tax Payment
    if n-(12*year) == proptaxdate or n-(12*year) == (proptaxdate+proptaxfrequency):
        propertytaxexpense = semiprop
    else:
        propertytaxexpense = 0
    #Summation of Present Values of Cashflows
    expense = propertytaxexpense + fedtax + normmonth + vacancycost
    income = rent
    value += (income-expense)/(((1+monthlydiscount)**n)-1)
    n += 1

print(value)
print(value-paidprice)

    
