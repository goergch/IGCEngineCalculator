import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
filename = "/Users/goergch/Downloads/756V7XF5.igc"
#filename = "/Users/goergch/Downloads/73uv7xf1.igc"
#filename = "/Users/goergch/Downloads/75lv7xf1.igc"
lines = open(filename,"r").readlines()
timeList = []
enlList = []
mopList = []
started = False
mop = 0
enl = 0
for line in lines:
    #print(line)
    if line.startswith("HFPLTPILOT"):
        pilotname = line.split(":")[1]
        print("Pilotname: %s" % (pilotname))
    elif line.startswith("HFDTE"):
        today = datetime.datetime.strptime(line[5:11],"%d%m%y")
        print("Date: %s" % (today.strftime("%d.%m.%y")))
    elif line.startswith("I"):
        iCount = line[1:3]
        iCount = int(iCount)
        for i in range(0, iCount):
            startbit = int(line[3 + (i * 7):5 + (i * 7)])
            stopbit = int(line[5 + (i * 7):7 + (i * 7)])
            name = line[7 + (i * 7):10 + (i * 7)]
            if name == "ENL":
                enlStart = startbit
                enlStop = stopbit
            elif name == "MOP":
                mopStart = startbit
                mopStop = stopbit
    elif line.startswith("LLXVTAKEOFF"):
        started = True
    elif line.startswith("LLXVFINISH"):
        started = False
    elif line.startswith("B"):
        if started:
            hour = int(line[1:3])
            minute = int(line[3:5])
            second = int(line[5:7])
            time = datetime.datetime.combine(today,datetime.time(hour,minute,second))
            enl = (int(line[enlStart:enlStop+1]) + 6 * enl) / 7
            mop = (line[mopStart:mopStart + 1])
            enlList.append(enl)
            mopList.append(mop)
            timeList.append(time)
            #print("%s: MOP: %s ENL %s" % (time.strftime("%H:%M"), mop, enl))


enlList = enlList[15:-30]
timeList = timeList[15:-30]
mopList = mopList[15:-30]

engineOn = False;
engineOnList = []
engineOnSeconds = 0;
#Evaluate time:
for i in range(0, len(enlList)):
    if engineOn == False and (enlList[i] > 100):
        engineOn = True
        startTime = timeList[i]
    elif engineOn == True and (enlList[i] <= 100):
        engineOn = False
        stopTime = timeList[i]
        engineOnList = engineOnList + [(startTime, stopTime)]
        print("Engine On: %s, Engine Of %s, Duration: %ds"
              % (startTime.strftime("%H:%M:%S"),stopTime.strftime("%H:%M:%S"),
                 (stopTime - startTime).total_seconds()))

        engineOnSeconds += (stopTime - startTime).total_seconds()

print("Total engine time is %.1f minutes" % (engineOnSeconds / 60.0))




fig, (ax1,ax2) = plt.subplots(2, sharex=True)
ax1.plot(timeList,mopList,'r')
ax2.plot(timeList,enlList,'r')
fig.autofmt_xdate()
myFmt = DateFormatter("%H:%M")
ax1.xaxis.set_major_formatter(myFmt)


#ax1.plot(timeList,enlStop,'g')
plt.show()




