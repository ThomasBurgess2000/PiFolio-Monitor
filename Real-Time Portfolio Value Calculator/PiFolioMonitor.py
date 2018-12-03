from alpha_vantage.timeseries import TimeSeries
import sys
from datetime import datetime as dt
from datetime import timedelta
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause

#Variables for calculation
currentDT = dt.now()
currentYMD = str(currentDT.year) + '-' + str(currentDT.month) + '-' + str(currentDT.day)

delta = timedelta(days = 1)
yesterdayUnformatted = currentDT-delta
yesterdayYMD = yesterdayUnformatted.strftime('%Y-%m-%d')
yesterdayClose = yesterdayYMD + ' ' + '15:30:00'

currentHour = currentDT.hour
currentHourIndex = currentDT.hour-9
times = [currentYMD+' '+'09:30:00', currentYMD+' '+'10:30:00', currentYMD+' '+'11:30:00', currentYMD+' '+'12:30:00', currentYMD+' '+'13:30:00', currentYMD+' '+'14:30:00', currentYMD+' '+'15:30:00']

portfolioValues = []
portfolioChanges = []

#Variables for Sense HAT
sense = SenseHat()
yellow = (255,255,0)
red = (255,0,0)
green = (0,255,0)
toggleValue = False

#Portfolio ['SYMBOL',# of shares]
portfolio = [['TSLA',16],['OLED',6],['NTDOY',2]]

#Takes a symbol and time as input, prints that hour's price, and returns that hour's price
#I need to make this so that when 15:30:00 is input for column 6 it gets the open value, but when it is after 16:30:00
def stockPrice(symbol, time):
    ts = TimeSeries(key = 'WJOFY5CTSKEC2VSP')
    data = ts.get_intraday(symbol = symbol, interval = '60min', outputsize = 'compact')
    if ((currentDT.hour==16 and currentDT.minute>29) or (currentDT.hour>16) or (time==yesterdayClose)):
        if ('15:30:00' in time):
            varStockPrice=data[0][time]['4. close']
    else:
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
    print ("Portfolio value is: " + str(portfolioValue))
    return portfolioValue

#Takes past portfolio values and changes lights accordingly
def lightChange():
    startTime = 9
    hourIndex = 0
    #puts portfolio values for each hour into the portfolioValues list
    if ((currentDT.weekday()==6) or (currentDT.weekday()==5)):
        ts = TimeSeries(key = 'WJOFY5CTSKEC2VSP')
        data = ts.get_intraday(symbol = 'TSLA', interval = '60min', outputsize = 'compact')
        lastRefreshed = data[1]['3. Last Refreshed']
        lastRefreshedPriceString=str(round(portCalc(lastRefreshed),2))
        sense.show_message(lastRefreshedPriceString)
    else:
        while ((startTime<(currentDT.hour+1)) and (startTime<16)):
            portfolioValues[hourIndex] = portCalc(times[hourIndex])
            hourIndex += 1
            startTime += 1
#Puts percentage changes (portfolioValues vs startingValue) into portfolioChanges array
        hourIndex=0
        startingValue = portCalc(yesterdayClose)
        while (hourIndex<(len(portfolioValues))):
            portfolioChanges[hourIndex] = ((portfolioValues[hourIndex]-startingValue)/startingValue)*100
            print (portfolioChanges[hourIndex])
            hourIndex += 1
    #while loop that runs through number of indexes in portfolioChanges and changes lights accordingly (hourIndex is column)
        hourIndex=0
        while (hourIndex<(len(portfolioChanges))):
            #For when the final displayed value is between -3.5% and 3.5%
            finalDisplayedChange = portfolioChanges[(len(portfolioChanges)-1)]
            currentChange=portfolioChanges[hourIndex]
            if (finalDisplayedChange<3.5 and finalDisplayedChange>-3.5):
                #For value changes between -3.5% and 3.5%
                if (currentChange<3.5 and currentChange>-3.5):
                    #Row 0
                    if (currentChange>2.5 and currentChange<3.5):
                        sense.set_pixel(hourIndex,0,yellow)
                    #Row 1
                    elif (currentChange>1.5 and currentChange<2.5):
                        sense.set_pixel(hourIndex,1,yellow)
                    #Row 2
                    elif (currentChange>0.5 and currentChange<1.5):
                        sense.set_pixel(hourIndex,2,yellow)
                    #Row 3
                    elif (currentChange>0 and currentChange<0.5):
                        sense.set_pixel(hourIndex,3,yellow)
                    #Row 4
                    elif (currentChange>-0.5 and currentChange<0):
                        sense.set_pixel(hourIndex,4,yellow)
                    #Row 5
                    elif (currentChange>-1.5 and currentChange<-0.5):
                        sense.set_pixel(hourIndex,5,yellow)
                    #Row 6
                    elif (currentChange>-2.5 and currentChange<-1.5):
                        sense.set_pixel(hourIndex,6,yellow)
                    #Row 7
                    elif (currentChange>-3.5 and currentChange<-2.5):
                        sense.set_pixel(hourIndex,7,yellow)
                #For value changes between 3.5% and 11.5%
                elif (currentChange>3.5 and currentChange<11.5):
                    sense.set_pixel(hourIndex,0,green)
                #For value changes between -3.5% and -11.5%
                elif (currentChange<-3.5 and currentChange>-11.5):
                    sense.set_pixel(hourIndex,7,red)
                #For values changes greater than 11.5% in either direction
                else:
                    print (currentChange)
                    sense.show_message(str(currentChange))
            #For when the final displayed value is between 3.5% and 11.5%
            elif (finalDisplayedChange>3.5 and finalDisplayedChange<11.5):
                #For value changes between -3.5% and 3.5%
                if (currentChange<3.5 and currentChange>-3.5):
                    sense.set_pixel(hourIndex, 7, yellow)
                #For value changes between -3.5% and -11.5%
                elif (currentChange<-3.5 and currentChange>-11.5):
                    sense.set_pixel(hourIndex, 7, red)
                #For value changes between 3.5% and 11.5%
                elif (currentChange>3.5 and currentChange<11.5):
                    #Row 7
                    if (currentChange>3.5 and currentChange<4.5):
                        sense.set_pixel(hourIndex,7,green)
                    #Row 6
                    elif (currentChange>4.5 and currentChange<5.5):
                        sense.set_pixel(hourIndex,6,green)
                    #Row 5
                    elif (currentChange>5.5 and currentChange<6.5):
                        sense.set_pixel(hourIndex,5,green)
                    #Row 4
                    elif (currentChange>6.5 and currentChange<7.5):
                        sense.set_pixel(hourIndex,4,green)
                    #Row 3
                    elif (currentChange>7.5 and currentChange<8.5):
                        sense.set_pixel(hourIndex,3,green)
                    #Row 2
                    elif (currentChange>8.5 and currentChange<9.5):
                        sense.set_pixel(hourIndex,2,green)
                    #Row 1
                    elif (currentChange>9.5 and currentChange<10.5):
                        sense.set_pixel(hourIndex,1,green)
                    #Row 0
                    elif (currentChange>10.5 and currentChange<11.5):
                        sense.set_pixel(hourIndex,0,green)
                else:
                    print (currentChange)
                    sense.show_message(str(currentChange))
            #For when the final displayed value is between -3.5% and -11.5%
            elif (finalDisplayedChange>-11.5 and finalDisplayedChange<-3.5):
                #For value changes between -3.5% and 3.5%
                if (currentChange>-3.5 and currentChange<3.5):
                    sense.set_pixel(hourIndex,0,yellow)
                #For value changes between 3.5% and 11.5%
                elif (currentChange>3.5 and currentChange<11.5):
                    sense.set_pixel(hourIndex,0,green)
                #For value changes between -3.5% and -11.5%
                elif (currentChange<-3.5 and currentChange>-11.5):
                    #Row 0
                    if (currentChange<-3.5 and currentChange>-4.5):
                        sense.set_pixel(hourIndex,0,red)
                    #Row 1
                    elif (currentChange<-4.5 and currentChange>-5.5):
                        sense.set_pixel(hourIndex,1,red)
                    #Row 2
                    elif (currentChange<-5.5 and currentChange>-6.5):
                        sense.set_pixel(hourIndex,2,red)
                    #Row 3
                    elif (currentChange<-6.5 and currentChange>-7.5):
                        sense.set_pixel(hourIndex,3,red)
                    #Row 4
                    elif (currentChange<-7.5 and currentChange>-8.5):
                        sense.set_pixel(hourIndex,4,red)
                    #Row 5
                    elif (currentChange<-8.5 and currentChange>-9.5):
                        sense.set_pixel(hourIndex,5,red)
                    #Row 6
                    elif (currentChange<-9.5 and currentChange>-10.5):
                        sense.set_pixel(hourIndex,6,red)
                    #Row 7
                    elif (currentChange<-10.5 and currentChange>-11.5):
                        sense.set_pixel(hourIndex,7,red)
                else:
                    print (currentChange)
                    sense.show_message(str(currentChange))
            #For when the final displayed value is beyond 11.5% in either direction
            else:
                print (finalDisplayedChange)
                sense.show_message(str(finalDisplayedChange))

            hourIndex += 1
 
#Turns off the matrix lights
def clear ():
    sense.clear()

#Main Function

print ("Powering up.")
sense.show_message("ON")
print ("Now running.\n")

#Accepts joystick as input and acts accordingly
while True:
    for event in sense.stick.get_events():
        if (event.action == 'pressed' and event.direction == 'up'):
            if (toggleValue == False):
                toggleValue = True
                lightChange()
            else:
                toggleValue = False
                print ("Cleared")
                clear()




