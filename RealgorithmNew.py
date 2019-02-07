"""
Robert Bauer
New Realgorithm Test
Running Different Iterations Over CFs for Monthly & Semiannual Cashflows, Taxes (Will only include federal tax if getting a return)
"""
#import pymongo and set database targets
import pymongo as pm
import datetime

db = pm.test
#Creating Dictionary for Cashflows to be stored in 10 Years worth
CFs = {}
M = 0
while M < 123:
    M += 1
    CFs[M] = 0

#print(CFs)

#Final Property Value Variable
Price = 100000#"Expected Market Price of Property" "Get from Database"
MOS = 0.20 #"Margin of Saftey off 'Market Price'/'Bank Appraisal Value' in order to Purchase Home" "Get from Datbase"
RenovationRate = 0.10 #"Get from Database"
ERV = 0
DiscountRate = 0.10 #"Get from Database"
MonthlyDiscount = (1+DiscountRate)**(1/12)
InsuranceRate = 0.00035 #"Get from Database"#Monthly Insurance Rate as a ratio of price
PropManageRate = 0.15 #"Get from Database"
BillRate = 0.10
#Variables from database
ExpectedRent = 1250#"Total Proprety Rent from database" "Adjust if rent could be seasonally impacted"
#Starting Month
CurrentMonth = datetime.datetime.now().month#"The Current Month"
CurrentYear = datetime.datetime.now().year #"The Current Year"
#Month Number of current forecasted month
MonthNum = 1#"referenceing current iteration of CFs (something like x in CFs on the global iteration)" "Not a Variable"
#Month being forecasted at the moment
RentMonth = (MonthNum + CurrentMonth) % 12

#Mortgage Variables
HardAPR = 0.10 #"Get from Database"
SoftAPR = 0.048 #"Get from Database"
MHAPR = HardAPR/12
MSAPR = SoftAPR/12
MortPoints = 0.02 #"Get from Database"
MortFees = 0.05 #"Get From Database"
HardMortYears = 5 #"Get from database"
SoftMortYears = 30 #"Get from Database"
DownPaymentPercentage = 0.10 #"Get from Database"
SMIR = 0.005 #"Get from Datbase" #Soft Mortgage Insurance Rate

#Set of Functions Called in Iteration

#Mortgage Calculations Function NOT FINISHED NEEDS TO ITERATE OVER ITSELF
def Mortify(Price):
    MortStartMonth = 2 #"Get From Database"
    MortRefiMonth = 6 #"Get From Database"
    MortgageCFs = {}
    SoftMortgageAmmount = Price*(1-DownPaymentPercentage)
    HardMortgageAmmount = Price*(1-MOS) + RenovationRate*Price
    HardMortMonthly = HardMortgageAmmount*MHAPR/(1-((1+MHAPR)**(-12*HardMortYears)))
    SoftMortMonthly = SoftMortgageAmmount*MSAPR/(1-((1+MSAPR)**(-12*SoftMortYears)))
    HardRemainingPrincipal = HardMortgageAmmount * (1+MortFees+MortPoints)
    SoftRemainingPrincipal = SoftMortgageAmmount * (1+MortFees+MortPoints)
    for x in range(MortStartMonth,(MortStartMonth+MortRefiMonth)):
        InterestExpense = HardRemainingPrincipal * MHAPR
        HardRemainingPrincipal -= (HardMortMonthly - InterestExpense)
        MortgageCFs[x] = [HardMortMonthly,HardRemainingPrincipal,InterestExpense]
    for x in range((MortStartMonth+MortRefiMonth),124):
        InterestExpense = SoftRemainingPrincipal * MSAPR
        SoftRemainingPrincipal -= (SoftMortMonthly - InterestExpense)
        MortgageCFs[x] = [SoftMortMonthly,SoftRemainingPrincipal,InterestExpense]
    HardMortRemaining = MortgageCFs[MortRefiMonth+MortStartMonth-1][1]
    MortOver = SoftMortgageAmmount - HardMortRemaining
    RefinancePayoff = [MortStartMonth + MortRefiMonth, MortOver]
    return MortgageCFs, RefinancePayoff

#Property Tax Functions
def PropertyTaxes(Price):
    PropTaxCfs = {}
    PropertyTaxRate = 0.01 #"Get from Database" #High but not Atypical Property Tax Rate
    for x in 123:
        if x % 12 == 3:
            PropTaxCfs[x] = Price*PropertyTaxRate
            PropTaxCfs[x+6] = Price*PropertyTaxRate
        else:
            PropTaxCfs[x] = 0
    return PropTaxCfs

#Function Call
#Iteration 1
def StaticCFs(Price):
    MortgageCFs = Mortify(Price)[0]
    RefinancePayoff = Mortify(Price)[1]
    CFs[2] = -(ExpectedRent*BillRate) - (InsuranceRate*Price) - MortgageCFs[2][0] #First mortgage month

    for month in range(3,124):
        if MonthNum % 13 == 3:
            CFs[month] = -1*ExpectedRent*(PropManageRate + BillRate) - (InsuranceRate*Price) - MortgageCFs[month][0]
        else:
            CFs[month] = (ExpectedRent * (1 - PropManageRate - BillRate)) - (InsuranceRate*Price) - MortgageCFs[month][0]

    CFs[RefinancePayoff[0]] += RefinancePayoff[1] #Refinancing Payoff Adjustment
    return CFs
#Iteration 2 Taxes including property taxes
#Non Monthly Cashflows
#Quarterly Variables (Quarterly Tax Estimate Payments) April, June, September, January Take Annual Tax and Divide it by 4
#Only make quarterly payments if you expect to owe $1000 over taxes on wages & normal income
#Deductions (Depreciaton, Mortgage Interest, Expenses, Attorneys, property managers, accountants etc.)
#Estimated tax rate of 24% as that bracket extends from $82,500 to $157,500 and I am likely to fall into a lower bracket
#Include Property Tax CFs in this step
TaxRate = 0.24
def depreciation(price):
    assesment = price * 0.70
    annualdepr = assesment/27.5
    return annualdepr

#Annual taxes -Only count if you are going to get a return and you assume it is payed out in may
#Calc should just be (Income-Expenses-Depreciation)=final if final > 0 then taxexpense = final*0.24 QuarterlyTax = taxexpense/4
#if taxexpense is over $1000 or final over $4150
PropTaxCFs = PropertyTaxes(Price)
CFs = StaticCFs(Price)

for month in range(3,124):
    CFs[month] -= PropTaxCFs[month]

#Final Values
#Present Value of CFs
#Make a different script for evaluating MOS, Refi Limits and Viable Price
for y in CFs:
    ERV += CFs[y]/(MonthlyDiscount**y)

print(ERV)
