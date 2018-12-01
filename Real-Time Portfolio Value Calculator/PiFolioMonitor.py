from alpha_vantage.timeseries import TimeSeries
import sys
from datetime import datetime as dt
from datetime import timedelta
from sense_hat import SenseHat


#Variables for calculation
currentDT = dt.now()
currentYMD = str(currentDT.year) + '-' + str(currentDT.month) + '-' + str(currentDT.day)
delta = timedelta(days = 1)
yesterdayUnformatted = currentDT-delta
yesterdayYMD = yesterdayUnformatted.strftime('%Y-%m-%d')
yestderdayClose = yesterdayYMD+' '+'15:30:00'
currentHour = currentDT.hour
currentHourIndex = currentDT.hour-9
times = [currentYMD+' '+'09:30:00',currentYMD+' '+'10:30:00',currentYMD+' '+'11:30:00',currentYMD+' '+'12:30:00',currentYMD+' '+'13:30:00',currentYMD+' '+'14:30:00',currentYMD+' '+'15:30:00']
portfolioValues = []

#Variables for Sense HAT
sense = SenseHat()
yellow = (255,255,0)
red = (255,0,0)
green = (0,255,0)

#Portfolio ['SYMBOL',# of shares]
portfolio = [['TSLA',16],['OLED',6],['NTDOY',2]]

#Takes a symbol and time as input, prints that hour's price, and returns that hour's price
def stockPrice(symbol, time):
    ts = TimeSeries(key = 'WJOFY5CTSKEC2VSP')
    data = ts.get_intraday(symbol = symbol, interval = '60min', outputsize = 'compact')
    varStockPrice = data[0][time]['1. open']
    print(varStockPrice)
    return (float(varStockPrice))

#Takes ticker symbol, number of stocks you have, and current stock price to calculate how much money you have in a certain stock
#I'm pretty sure currentHour-9 equals the index of the times variable
def stockCalc(symbol,shares,time):
    price = stockPrice(symbol,time)
    return (price*shares)

#Calculates the value of your portfolio at time when run. The format of time should be "Y-M-D HOUR-MIN-SEC"
def portCalc(time):
    portfolioValue = 0
    portfolioIteration = 0
    #calculate the value of each ticker I have (price * shares)
    while (portfolioIteration<(len(portfolio))):
        currentSymbol = portfolio[portfolioIteration][0]
        currentShares = portfolio[portfolioIteration][1]
        print ("Checking " + currentSymbol)
        portfolioValue = portfolioValue+ (stockCalc(currentSymbol, currentShares, time))
        portfolioIteration += 1
    print (portfolioValue)
    return portfolioValue

#Takes past portfolio values and changes lights accordingly
def lightChange():
    startTime = 9
    hourIndex = 0
    #puts portfolio values for each hour into the portfolioValues list
    while ((startTime<currentDT.hour) and (startTime<16)):
        portfolioValues[hourIndex] = portCalc(times[hourIndex])
        hourIndex += 1
        startTime += 1
    #while loop that runs through number of indexes in portfolioValues and changes lights accordingly (needs to compare to starting value somehow)
    startingValue = portCalc(yesterdayYMD)

portCalc(times[0])

