# -*- coding: utf-8 -*-
"""
Created on Wed May 16 21:24:00 2018

@author: Robert Bauer
"""
from pymongo import MongoClient
client = MongoClient(port=27017)
db = client.admin
#Function of Discounted Cashflow Model for Business
#price from market price guessing algorithm
#rent from rent guessing algorithm

def ERV(price, expectedrent, propid):
    marketprice = price
    rent = expectedrent
    apr = .0485 #loan apr
    mortlength = 30 #Number of years on the mortgage
    downpaymentpercentage = 0.1 #your downpayment percentage 
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

    x = 0
    mortinterest = {}
    while x <= numberofmonths:
        mortinterest[x] = (mortgageammount*(((1+monthlyapr)**numberofmonths)-((1+monthlyapr)**x))/(((1+monthlyapr)**numberofmonths)-1))*monthlyapr
        x += 1
    
    year = 0
    value = 0
    fedtax = 0
    n=1
    runningtotal = {}
    while n <= numberofmonths:
        if n % 12 == 0:
            year += 1 
        #Removing number of vacant months per year
        if n % 12 == (12-vacancy):
            vacancycost = -1*(rent+unrentedfee)*vacancy
        else:
            vacancycost = 0       
        #Quarterly Federal Estimted Tax Payments   
        if n-((12*(year-1))-12) == 1: 
            if (taxincome-quarterly) < 0:
                fednettax = (taxincome-(quarterly+mortinterest[n-1]+mortinterest[n-2])+mortinterest[n-3]+mortinterest[n-4])
            else:
                fednettax = (taxincome-(quarterly+mortinterest[n-1]+mortinterest[n-2])+mortinterest[n-3]+mortinterest[n-4])*0.35
            fedtax = fednettax
        elif n-(12*year) == 4:
            if (taxincome-quarterly) < 0:
                fednettax = (taxincome-(quarterly+mortinterest[n-1]+mortinterest[n-2])+mortinterest[n-3]+mortinterest[n-4])
            else:
                fednettax = (taxincome-(quarterly+mortinterest[n-1]+mortinterest[n-2])+mortinterest[n-3]+mortinterest[n-4])*0.35
            fedtax = fednettax
        elif n-(12*year) == 7:
            if (taxincome-quarterly) < 0:
                fednettax = (taxincome-(quarterly+mortinterest[n-1]+mortinterest[n-2])+mortinterest[n-3]+mortinterest[n-4])
            else:
                fednettax = (taxincome-(quarterly+mortinterest[n-1]+mortinterest[n-2])+mortinterest[n-3]+mortinterest[n-4])*0.35
            fedtax = fednettax
        elif n-(12*year) == 10:
            if (taxincome-quarterly) < 0:
                fednettax = (taxincome-(quarterly+mortinterest[n-1]+mortinterest[n-2])+mortinterest[n-3]+mortinterest[n-4])
            else:
                fednettax = (taxincome-(quarterly+mortinterest[n-1]+mortinterest[n-2])+mortinterest[n-3]+mortinterest[n-4])*0.35
            fedtax = fednettax
        else:
            fedtax = 0
            
        #Twice Yearly Property Tax Payment
        if n % 12 == proptaxdate or n % 12 == (proptaxdate+proptaxfrequency):
            propertytaxexpense = semiprop
        else:
            propertytaxexpense = 0
            
        #Summation of Present Values of Cashflows
        expense = (propertytaxexpense + fedtax + normmonth + vacancycost)*((1+(expensegrowth/12))**n)
        income = rent*((1+(incomegrowth/12))**n)
        value += (income-expense)/(((1+monthlydiscount)**n))
        runningtotal[n-1] = value
        n += 1
    value = value - closingcost - repaircost - totalmortfee
    test = value - (downpayment + closingcost + repaircost + totalmortfee)

    if test > 0:
        properties = {
                'propid' : propid,
                'valuve' : value,
                'residual' : test 
                }
        result=db.prop.insert_one(properties)
        

    
ERV(200000, 3000, 123)

