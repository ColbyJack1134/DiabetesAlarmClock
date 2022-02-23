import serial
import time
from datetime import datetime
import threading
from pydexcom import Dexcom

# * means high
# - means low 
# { means beep high
# } means beep low

#Dexcom login
dexcom = Dexcom("username", "password")

#Has to be the port your arduino is on, time.sleep so it can connect properly
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=0.1)
time.sleep(2)

#Global variables
lastTime = "00:00"
lastInput = "None"
currInput = "None"
lastDexcomValue = "None"

#Settings that you can change
timeInBadRange = 0
timeTilBeep = 300
beepAbove = 180
beepBelow = 80

#Just gets a string value for the Dexcom trend
def trendToStr(trend):
    if trend == 0 or trend == 8 or trend == 9:
        return "Trend N/A"
    elif trend == 1:
        return "Rising Fast"
    elif trend == 2:
        return "Rising"
    elif trend == 3:
        return "Rising Slow"
    elif trend == 4:
        return "Steady"
    elif trend == 5:
        return "Falling Slow"
    elif trend == 6:
        return "Falling"
    elif trend == 7:
        return "Falling Fast"
    else:
        return "Trend N/A"

#Main loop
def dataLoop():
    global lastTime, lastInput, currInput, lastDexcomValue, timeInBadRange, timeTilBeep, beepAbove, beepBelow
    now = datetime.now()
    currentTime = now.strftime("%I:%M %p")
    
    #Dexcom API to get the actual blood sugar
    bg = dexcom.get_current_glucose_reading() 
        
    #If anything has changed and the display needs to be updated
    if currentTime != lastTime or currInput != lastInput or (bg and str(bg.value) != lastDexcomValue):
        toSend = ""
        #If debug input has been entered
        if currInput != lastInput:
            lastInput = currInput
            toSend += currInput + " Going up"
            if(int(currInput) >= beepAbove):
                toSend += "*{"
            elif(int(currInput) <= beepBelow):
                toSend += "-}"
        #If there is a blood sugar reading
        elif bg:
            lastDexcomValue = str(bg.value)
            toSend += str(bg.value)             #BS value
            toSend += " "
            toSend += trendToStr(bg.trend)      #BS trend
            val = int(bg.value)
            if val >= beepAbove or val <= beepBelow:
                #Just got into bad range
                if timeInBadRange == 0:
                    timeInBadRange = time.time()
                    if val >= beepAbove:
                        toSend += "{"
                    else:
                        toSend += "}"
                #Has been bad but over the time until beep
                elif time.time() - timeInBadRange >= timeTilBeep:
                    timeInBadRange = time.time()
                    if val >= beepAbove:
                        toSend += "{"
                    else:
                        toSend += "}"
            else:
                timeInBadRange = 0
            if val >= beepAbove:
                toSend += "*"
            elif val <= beepBelow:
                toSend += "-"
        elif not bg:
            lastDexcomValue = "None"
            toSend += "None"
        lastTime = currentTime
        toSend += "\n"
        toSend += currentTime                   #Current time
        arduino.write(bytes(toSend, 'utf-8'))   #Send data to arduino
    time.sleep(2)
    dataLoop()                                  #Recursion

#Putting the main loop in a thread so you can still get debug input
threading1 = threading.Thread(target=dataLoop)
threading1.daemon = True
threading1.start()

#Debug input
while True:
    inp = input("Enter Blood Sugar: ")
    currInput = inp
    time.sleep(0.05)