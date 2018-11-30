from alpha_vantage.timeseries import TimeSeries
import sys
from datetime import datetime, timedelta
from sense_hat import senseHat


#Variables for calculation
currentDT = datetime.datetime.now()
currentYMD= str(currentDT.year) + '-' + str(currentDT.month) + '-' + str(currentDT.day)
yesterdayYMD=datetime.strftime(datetime.now()-timedelta(1), '%Y-%M-%d')
currentHour = currentDT.hour
currentHourIndex=currentDT.hour-9
times=[currentYMD+' '+'09:30:00',currentYMD+' '+'10:30:00',currentYMD+' '+'11:30:00',currentYMD+' '+'12:30:00',currentYMD+' '+'13:30:00',currentYMD+' '+'14:30:00',currentYMD+' '+'15:30:00']
portfolioValues=[]

#Variables for Sense HAT
sense = senseHat()
yellow= (255,255,0)
red=(255,0,0)
green=(0,255,0)

#Portfolio ['SYMBOL',# of shares]
portfolio=[['TSLA',16],['OLED',6],['NTDOY',2]]

#Takes a symbol and time as input, prints that hour's price, and returns that hour's price
def stockPrice(symbol, time):
    ts = TimeSeries(key='WJOFY5CTSKEC2VSP')
    data = ts.get_intraday(symbol=symbol,interval='60min', outputsize='compact')
    print(data[0][time]['4. close'])
    return (float((data[0][time]['4. close'])))

#Runs stockPrice as many hours as the stock market has been open today
def getHourly():
    startTime=9
    hourIndex=0
    while ((startTime<currentDT.hour) and (startTime<16)):
       # stockPrice(ticker,times[hourIndex])
        hourIndex+=1
        startTime+=1

#Takes ticker symbol, number of stocks you have, and current stock price to calculate how much money you have in a certain stock
#I'm pretty sure currentHour-9 equals the index of the times variable
def stockCalc(symbol,shares,time):
    price=stockPrice(symbol,time)
    return (price*shares)

#Calculates the current value of your portfolio when run
def portCalc(time):
    portfolioValue=0
    portfolioIteration=0
    #calculate the value of each ticker I have (price * shares)
    while (portfolioIteration<(len(portfolio))):
        print ("Checking "+ portfolio[portfolioIteration][0])
        portfolioValue=portfolioValue+ (stockCalc(portfolio[portfolioIteration][0],portfolio[portfolioIteration][1],time))
        portfolioIteration+=1
    print (portfolioValue)
    return portfolioValue

#Takes past portfolio values and changes lights accordingly
def lightChange():
    startTime=9
    hourIndex=0
    #puts portfolio values for each hour into the portfolioValues list
    while ((startTime<currentDT.hour) and (startTime<16)):
        portfolioValues[hourIndex]=portCalc(times[hourIndex])
        hourIndex+=1
        startTime+=1
    #while loop that runs through number of indexes in portfolioValues and changes lights accordingly (needs to compare to starting value somehow)

    stockPrice('NTDOY',2)
portCalc(times[0])

