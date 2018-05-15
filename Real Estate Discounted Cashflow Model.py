# -*- coding: utf-8 -*-
"""
Created on Fri May 11 16:43:01 2018

@author: Scott Bauer
"""

#Discounted Cashflow Model for Pricing Rental Properties

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
totalmortfee = mortgagefee + mortgagepoints
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
montlycapx = capx/12
unrentedfee = ((bills+propmanagefee)*0.5) #"sum of montly fees when the property is vacant"
insurance = 75 #"monthly home insurance and other insurance"

#Expected Taxes
depreciation = (marketprice+repaircost)/27.5 #Federal Straitline Depreciation
proptax = (marketprice+repaircost)*0.8*0.02 #"annual property tax"
semiprop = proptax/2 #semi annual property tax due

#Dates
HOAdate = 0 #"Date of first HOA fee"
HOAfrequency = 3 #"how far apart in months are the hoa fees"
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
n=1
while n <= numberofmonths:
    if n % 12 == 0:
        year += 1
    if n-(12*year)==4 or n-(12*year)==10:
        value += 1
    n += 1

print(year)
print(value)
    
    
