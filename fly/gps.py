import math
import tkMessageBox
from tkFileDialog import askopenfilename, asksaveasfilename
from decimal import *
import tkFont
import xlrd
from Tkinter import *








###CONNECTING GUI WITH CORE
def runCode(openFilePath,saveFilePath,massInput,var,checkVariable1,checkVariable2,checkVariable3,unitsVarible,checkVariable4,fileVar):
    writeKMLfile(openFilePath,saveFilePath,massInput,var,checkVariable1,checkVariable3,unitsVarible,checkVariable4,fileVar)
    if checkVariable2 == 1:
        writeCoordinateFile(openFilePath,saveFilePath,massInput,fileVar)



###CORE OF SOFTWARE
def readFile(openFilePath,fileVar):

    ##GPS Reader
    if fileVar == 1:    
        ## Opening and reading File
        file = open(openFilePath,'r')
        fileLists = file.readlines()
        file.close()

        ## Declaring Lists
        tempList = []
        xList = []
        yList = []
        zList = []
        timeList = []
        zoneList = []
        dateList = []
        

        
        numberOfStrings = len(fileLists)
        
        ## Brake each Line into a List
        for i in range(5,numberOfStrings):
            string = fileLists[i]     
            stringArray = string.split(',')
            numberOfElements = len(stringArray)

        
            ## Checking for very last string that signals the end        
            if len(stringArray)<= 1:
                break

            
           
            ## Reading each Line and finding target values
            for w in range(0, numberOfElements):
                
                ## Find String with the UTM zone (works only in Georgia so Far)
                if stringArray[w].find('S') != -1:
                    zoneList.append(stringArray[w])

                ##Find string with the date            
                if stringArray[w].find('/') != -1:
                    dateList.append(stringArray[w])

                    
                ## Find String with "." in it
                if stringArray[w].find('.') != -1:        
                    tempList.append(stringArray[w])
                ## Find String with ":" in it
                elif stringArray[w].find(':') != -1:
                    timeStamp = stringArray[w]

            ## Getting values from tempString and putting them in their respective lists                
            tempList.append(timeStamp)
            xList.append(tempList[0])
            yList.append(tempList[1])
            zList.append(tempList[2])
            timeList.append(tempList[3])
            del tempList[0:4]
            
     ##EXCEL Reader
    if fileVar == 3:
        
        wb = xlrd.open_workbook(openFilePath)
        sh = wb.sheet_by_index(0)
        
        xList = sh.col_values(0)
        yList = sh.col_values(1)
        zList = sh.col_values(2)
        timeList = []
        zoneList = []
        dateList = []
        zoneListExcelFormat = []

        
        timeListExcelFormat = sh.col_values(3)
        dateListExcelFormat = sh.col_values(4)
        
        ##Algorithm to fix when zone is splitted into two columns ex: 17 S
        if sh.ncols == 7:
            fiveList = sh.col_values(5)
            lambdaValue=lambda x:type(fiveList[0])==type(3.0)
            lambdaValue2=lambda x:type(fiveList[0])==type(3)
            isFloat = lambdaValue(0)
            isInt = lambdaValue(0)
            
            sixList = sh.col_values(6)
            
            
            if isInt or isFloat== 1:
                for i in range(0,len(fiveList)):
                    if fiveList[i] == "":
                        if sixList[i] == "":
                            zoneListExcelFormat.append(str(int(fiveList[0]))+str(sixList[0]))
                        else:
                            zoneListExcelFormat.append(str(int(fiveList[0]))+str(sixList[i]))
                    elif sixList[i] == "":
                        zoneListExcelFormat.append(str(int(fiveList[i]))+str(sixList[0]))
                    else:
                        zoneListExcelFormat.append(str(int(fiveList[i]))+str(sixList[i]))
 
                
            else:
                for i in range(0,len(fiveList)):
                    if fiveList[i] == "":
                        if sixList[i] == "":
                            zoneListExcelFormat.append(str(int(sixList[0]))+str(fiveList[0]))
                        else:
                            zoneListExcelFormat.append(str(int(sixList[0]))+str(fiveList[i]))
                    elif sixList[i] == "":
                        zoneListExcelFormat.append(str(int(sixList[i]))+str(fiveList[0]))
                    else:
                        zoneListExcelFormat.append(str(int(sixList[i]))+str(fiveList[i]))                   



        else:
            zoneListExcelFormat = sh.col_values(5)

        
        


        
        hourPrevious = 0
        minutePrevious = 0
        secondPrevious = 0        

        for i in range(0,len(timeListExcelFormat)):
            ##Gregorian (year (0), month (1), day (2), hour(3), minute(4), nearest_second(5)).
            
            #########TIME
            if timeListExcelFormat[0] < 1 and timeListExcelFormat[0] > 0:
                
                timeTemp = xlrd.xldate_as_tuple(timeListExcelFormat[i], 0)
                         
                hour = str(timeTemp[3])
                minute = str(timeTemp[4])
                second = str(timeTemp[5])

                
                ##algorithm to add "0" to time when number is below "10"           
                if len(str(timeTemp[3]))<2:
                    hour = "0"+str(timeTemp[3])
                if len(str(timeTemp[4]))<2:
                    minute = "0"+str(timeTemp[4])
                if len(str(timeTemp[5]))<2:
                    second = "0"+str(timeTemp[5])

                    
                ##print hourPrevious,hour,minutePrevious,minute,secondPrevious,second
                ##Algorithm that fixes issue of two values of time being equal! 
                if int(hourPrevious) == int(hour) and int(minutePrevious) == int(minute) and int(secondPrevious) == int(second):
                    if int(second[0]) == 0 and int(second) != 9:
                        second = "0"+str(int(second)+1)
                        ##print "sec1"
                    elif int(second) == 59:
                        second = "00"
                        ##print "sec2"
                        if int(minute) == 59:
                            minute = "00"
                            ##print "min1"
                            if int(hour[0]) == 0:
                                hour = "0"+str(int(hour)+1)
                                ##print "hour1"
                            else:
                                hour = str(int(hour)+1)
                                ##print "hour2"
                            
                        elif int(minute[0]) == 0 and int(minute) != 9:
                            minute = "0"+str(int(minute)+1)
                            ##print "min2"
                        else:
                            minute = str(int(minute)+1)
                            ##print "min3"
                    else:
                        second = str(int(second)+1)
                        ##print "sec3"






                hourPrevious = hour
                minutePrevious = minute
                secondPrevious = str(second)                
                timeTempFormatted = str(hour)+":"+ str(minute)+":"+ str(second)
                timeList.append(timeTempFormatted)



                        
            else:
                totalSeconds = float(timeListExcelFormat[i])
                totalHours = totalSeconds / 3600.0
                totalHoursArray = str(totalHours).split('.')
                hour2 = str(totalHoursArray[0])
                
                totalMinutes = (totalHours-float(hour2))*60
                totalMinutesArray = str(totalMinutes).split('.')
                minutes2 = str(totalMinutesArray[0])

                seconds2 = str(int(round((totalMinutes-float(minutes2))*60)))

                ##algorithm to add "0" to time when number is below "10"           
                if len(hour2)<2:
                    hour2 = "0"+hour2
                if len(minutes2)<2:
                    minutes2 = "0"+minutes2
                if len(seconds2)<2:
                    seconds2 = "0"+seconds2

                timeCombinedFormatted = str(hour2)+":"+ str(minutes2)+":"+ str(seconds2)
                timeList.append(timeCombinedFormatted)                  
                
               
                


                   
            ###################DATE
            if dateListExcelFormat[i] == "":
                dateTemp = xlrd.xldate_as_tuple(dateListExcelFormat[0], 0)          
            else:
                dateTemp = xlrd.xldate_as_tuple(dateListExcelFormat[i], 0)
            
            year = str(dateTemp[0])
            month = str(dateTemp[1])
            day = str(dateTemp[2])
            
            ##algorithm to add "0" to date when number is below "10" 
            if len(str(dateTemp[1]))<2:
                month = "0"+str(dateTemp[1])
            if len(str(dateTemp[2]))<2:
                day = "0"+str(dateTemp[2])            

            dateTempFormatted = str(month+"/"+ day+"/"+ year)
            dateList.append(dateTempFormatted)




            ########################Zone List
            if zoneListExcelFormat[i] == "":
                zoneList.append(str(zoneListExcelFormat[0]))
            else:
                zoneList.append(str(zoneListExcelFormat[i]))

    return xList,yList, zList, timeList, zoneList, dateList
    

##Calculate values

def calculate(x1, x2 , y1 ,y2, z1, z2, time1, time2, massInput, zone1, zone2):
    
    ##Converting Time to seconds
    
    ##Time1
    time1Array = time1.split(':')
    hours1 = float(time1Array[0]) * (3600.0)
    minutes1 = float(time1Array[1]) * (60)
    seconds1 = float(time1Array[2])
    t1 = hours1+minutes1+seconds1

    ##Time2
    time2Array = time2.split(':')
    hours2 = float(time2Array[0]) * (3600.0)
    minutes2 = float(time2Array[1]) * (60)
    seconds2 = float(time2Array[2])
    t2 = hours2+minutes2+seconds2

    
    ##Converting string imputs to Floats
    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)
    z1 = float(z1)
    z2 = float(z2)


    
    ##Calculating Velocities given the x,y,z,t components.
    if zone2 != zone1:
        ## This algorithm eliminates huge velocities being shown due to change in geographic zone
        vx = (x1-float(xList[-2]))/(t1-float(timeList[-2]))
        vy = (y1-float(yList[-2]))/(t1-float(timeList[-2]))
        vz = (z1-float(zList[-2]))/(t1-float(timeList[-2]))
        vTotal = math.sqrt((vx**2)+(vy**2)+(vz**2))
    else:
        vx = (x2-x1)/(t2-t1)
        vy = (y2-y1)/(t2-t1)
        vz = (z2-z1)/(t2-t1)
        vTotal = math.sqrt((vx**2)+(vy**2)+(vz**2))

    ##Calculating Acceleration
    ax = (vx-xVelocityList[-1])/(t2-t1)
    ay = (vy-yVelocityList[-1])/(t2-t1)
    az = (vz-zVelocityList[-1])/(t2-t1)
    aTotal = (vTotal-totalVelocityList[-1])/(t2-t1)

    
    ##aTotal = math.sqrt((ax**2)+(ay**2)+(az**2))

    ##Calculating Force
    mass = float(massInput)
    fx = mass * ax
    fy = mass * ay
    fz = mass * az
    fTotal = mass * aTotal

    ##Kinetic Energy
    ke = 0.5*mass*(vTotal*vTotal)

    ##Potential Energy
    pe = mass*9.81*z1



    ##Calculating Power Net
    pNet = fTotal*vTotal

    ##pTotal = abs(pNet)    

    
    

    ##Work
    workX = fx*(x2-x1)
    workY = fy*(y2-y1)
    workZ = fz*(z2-z1)
    workTotal = math.sqrt((workX**2)+(workY**2)+(workZ**2)) ##add workX...Z (scalar)
    work = pNet * (t2-t1)





    ##Appending Values to the different Lists
    xList.append(x2)
    yList.append(y2)
    zList.append(z2)
    timeList.append(t2)
    
    ##Velocities
    xVelocityList.append(vx)
    yVelocityList.append(vy)
    zVelocityList.append(vz)
    totalVelocityList.append(vTotal)

    ##Acceleration
    xAccelerationList.append(ax)
    yAccelerationList.append(ay)
    zAccelerationList.append(az)
    totalAccelerationList.append(aTotal)

    ##Forces
    xForceList.append(fx)
    yForceList.append(fy)
    zForceList.append(fz)
    totalForceList.append(fTotal)

    ##Kinetic Energy
    keList.append(ke)
    ##Potential Energy
    peList.append(pe)







    ##Power
    pNetList.append(pNet)

    ##Work
    xWorkList.append(workX)
    yWorkList.append(workY)
    zWorkList.append(workZ)
    totalWorkList.append(workTotal)
    workList.append(work)

    

    return vx, vy, vz, vTotal, ax, ay, az, aTotal, fx, fy, fz, fTotal, pNet, workX, workY, workZ, workTotal, work, ke, pe


##X List
xList = [0.0]
yList = [0.0]
zList = [0.0]

##Time List
timeList = [0.0]

##Velocities Lists
xVelocityList = [0.0]
yVelocityList = [0.0]
zVelocityList = [0.0]
totalVelocityList = [0.0]

##Acceleration
xAccelerationList=[]
yAccelerationList=[]
zAccelerationList=[]
totalAccelerationList=[]


##Forces
xForceList = []
yForceList = []
zForceList = []
totalForceList = []

##Kinetic Energy
keList = []


##Potential Energy
peList = []



##Power
pNetList = []

##Work
xWorkList = []
yWorkList = []
zWorkList = []
totalWorkList = []
workList = []

#input_mass = raw_input("Mass: ");
#mass = float(input_mass)


      
        

#Read and Calculate the file
            
def readAndCalculate(filePath,massInput,fileVar):
    
    ## Extract lists from TXT file using readFile function
    listsFromFile = readFile(filePath,fileVar)
    xList = listsFromFile[0]
    yList = listsFromFile[1]
    zList = listsFromFile[2]
    timeList = listsFromFile[3]
    zoneList = listsFromFile[4]

    ## Values to return
        ##Velocities Lists
    xVeloList = []
    yVeloList = []
    zVeloList = []
    totalVeloList = []
    
        ##Acceleration Lists
    xAccelList = []
    yAccelList = []
    zAccelList = []
    totalAccelList = []
    
        ##Forces Lists
    xForList = []
    yForList = []
    zForList = []
    totalForList = []

        ##Kinetic Energy
    kEnergyList = []
        ##Potential Energy
    pEnergyList = []

        ##Power
    netPowList = []

        ##Work
    xxWorkList = []
    yyWorkList = []
    zzWorkList = []
    ttotalWorkList = []
    wworkList = []
    
    numberOfLoops = len(xList)
    temp = []
    for i in range(0, numberOfLoops-1):
        
        temp = calculate(xList[i], xList[i+1], yList[i], yList[i+1], zList[i], zList[i+1], timeList[i], timeList[i+1],massInput, zoneList[i],zoneList[i+1])

        ## Appending values to list
            ##Velocities
        xVeloList.append(temp[0])
        yVeloList.append(temp[1])
        zVeloList.append(temp[2])
        totalVeloList.append(temp[3])
        
            ##Acceleration
        xAccelList.append(temp[4])
        yAccelList.append(temp[5])
        zAccelList.append(temp[6])
        totalAccelList.append(temp[7])

            ##Forces
        xForList.append(temp[8])
        yForList.append(temp[9])
        zForList.append(temp[10])
        totalForList.append(temp[11])

            ##Kinetic Energy
        kEnergyList.append(temp[18])
        
            ##Potential Energy
        pEnergyList.append(temp[19])
            ##Power
        netPowList.append(temp[12])

            ##Work
        xxWorkList.append(temp[13])
        yyWorkList.append(temp[14])
        zzWorkList.append(temp[15])
        ttotalWorkList.append(temp[16])
        wworkList.append(temp[17])


    ##Removing first values from lists (they get lost because of the ladder effect when calculating acceleration of an object that is alredy moving)

    del xVeloList[0]
    del yVeloList[0]
    del zVeloList[0]
    del totalVeloList[0]

    del xAccelList[0]
    del yAccelList[0]
    del zAccelList[0]
    del totalAccelList[0]

    del xForList[0]
    del yForList[0]
    del zForList[0]
    del totalForList[0]

    del kEnergyList[0]
    del pEnergyList[0]

    del netPowList[0]

    del xxWorkList[0]
    del yyWorkList[0]
    del zzWorkList[0]
    del ttotalWorkList[0]
    del wworkList[0]


    ##print len(xList), len(xVeloList), len(xAccelList), len(xForList),len(netPowList)    
    #return "xVeloList: ", xVeloList, "yVeloList: ", yVeloList, "zVeloList: ", zVeloList, "totalVeloList: ", totalVeloList, "xAccelList: ", xAccelList, "yAccelList: ", yAccelList, "zAccelList: ", zAccelList, "totalAccelList: ", totalAccelList, "xForList: ", xForList, "yForList: ", yForList, "zForList: ", zForList, "totalForList: ", totalForceList, "netPowList: ", netPowList

    return xVeloList,yVeloList,zVeloList,totalVeloList,xAccelList,yAccelList,zAccelList,totalAccelList,xForList, yForList, zForList, totalForList, netPowList, xxWorkList, yyWorkList, zzWorkList, ttotalWorkList, wworkList, kEnergyList,pEnergyList

##______________________________________________________________

# Lat Long - UTM, UTM - Lat Long conversions

from math import pi, sin, cos, tan, sqrt

#LatLong- UTM conversion..h
#definitions for lat/long to UTM and UTM to lat/lng conversions
#include <string.h>

_deg2rad = pi / 180.0
_rad2deg = 180.0 / pi

_EquatorialRadius = 2
_eccentricitySquared = 3

_ellipsoid = [
#  id, Ellipsoid name, Equatorial Radius, square of eccentricity	
# first once is a placeholder only, To allow array indices to match id numbers
    [ -1, "Placeholder", 0, 0],
    [ 1, "Airy", 6377563, 0.00667054],
    [ 2, "Australian National", 6378160, 0.006694542],
    [ 3, "Bessel 1841", 6377397, 0.006674372],
    [ 4, "Bessel 1841 (Nambia] ", 6377484, 0.006674372],
    [ 5, "Clarke 1866", 6378206, 0.006768658],
    [ 6, "Clarke 1880", 6378249, 0.006803511],
    [ 7, "Everest", 6377276, 0.006637847],
    [ 8, "Fischer 1960 (Mercury] ", 6378166, 0.006693422],
    [ 9, "Fischer 1968", 6378150, 0.006693422],
    [ 10, "GRS 1967", 6378160, 0.006694605],
    [ 11, "GRS 1980", 6378137, 0.00669438],
    [ 12, "Helmert 1906", 6378200, 0.006693422],
    [ 13, "Hough", 6378270, 0.00672267],
    [ 14, "International", 6378388, 0.00672267],
    [ 15, "Krassovsky", 6378245, 0.006693422],
    [ 16, "Modified Airy", 6377340, 0.00667054],
    [ 17, "Modified Everest", 6377304, 0.006637847],
    [ 18, "Modified Fischer 1960", 6378155, 0.006693422],
    [ 19, "South American 1969", 6378160, 0.006694542],
    [ 20, "WGS 60", 6378165, 0.006693422],
    [ 21, "WGS 66", 6378145, 0.006694542],
    [ 22, "WGS-72", 6378135, 0.006694318],
    [ 23, "WGS-84", 6378137, 0.00669438]
]



#Convertion function
#void UTMtoLL(int ReferenceEllipsoid, const double UTMNorthing, const double UTMEasting, const char* UTMZone,
#			  double& Lat,  double& Long )

def UTMtoLL(ReferenceEllipsoid, northing, easting, zone):

#converts UTM coords to lat/long.  Equations from USGS Bulletin 1532 
#East Longitudes are positive, West longitudes are negative. 
#North latitudes are positive, South latitudes are negative
#Lat and Long are in decimal degrees. 
#Written by Chuck Gantz- chuck.gantz@globalstar.com
#Converted to Python by Russ Nelson <nelson@crynwr.com>

    k0 = 0.9996
    a = _ellipsoid[ReferenceEllipsoid][_EquatorialRadius]
    eccSquared = _ellipsoid[ReferenceEllipsoid][_eccentricitySquared]
    e1 = (1-sqrt(1-eccSquared))/(1+sqrt(1-eccSquared))
    #NorthernHemisphere; //1 for northern hemispher, 0 for southern

    x = easting - 500000.0 #remove 500,000 meter offset for longitude
    y = northing

    ZoneLetter = zone[-1]
    ZoneNumber = int(zone[:-1])
    if ZoneLetter >= 'N':
        NorthernHemisphere = 1  # point is in northern hemisphere
    else:
        NorthernHemisphere = 0  # point is in southern hemisphere
        y -= 10000000.0         # remove 10,000,000 meter offset used for southern hemisphere

    LongOrigin = (ZoneNumber - 1)*6 - 180 + 3  # +3 puts origin in middle of zone

    eccPrimeSquared = (eccSquared)/(1-eccSquared)

    M = y / k0
    mu = M/(a*(1-eccSquared/4-3*eccSquared*eccSquared/64-5*eccSquared*eccSquared*eccSquared/256))

    phi1Rad = (mu + (3*e1/2-27*e1*e1*e1/32)*sin(2*mu) 
               + (21*e1*e1/16-55*e1*e1*e1*e1/32)*sin(4*mu)
               +(151*e1*e1*e1/96)*sin(6*mu))
    phi1 = phi1Rad*_rad2deg;

    N1 = a/sqrt(1-eccSquared*sin(phi1Rad)*sin(phi1Rad))
    T1 = tan(phi1Rad)*tan(phi1Rad)
    C1 = eccPrimeSquared*cos(phi1Rad)*cos(phi1Rad)
    R1 = a*(1-eccSquared)/pow(1-eccSquared*sin(phi1Rad)*sin(phi1Rad), 1.5)
    D = x/(N1*k0)

    Lat = phi1Rad - (N1*tan(phi1Rad)/R1)*(D*D/2-(5+3*T1+10*C1-4*C1*C1-9*eccPrimeSquared)*D*D*D*D/24
                                          +(61+90*T1+298*C1+45*T1*T1-252*eccPrimeSquared-3*C1*C1)*D*D*D*D*D*D/720)
    Lat = Lat * _rad2deg

    Long = (D-(1+2*T1+C1)*D*D*D/6+(5-2*C1+28*T1-3*C1*C1+8*eccPrimeSquared+24*T1*T1)
            *D*D*D*D*D/120)/cos(phi1Rad)
    Long = LongOrigin + Long * _rad2deg
    return (Lat, Long)
        


# Extract data from file to write KML google file

def getDataForKML(openFilePath,fileVar):
    ## Extract lists from TXT file using readFile function
    listsFromFile = readFile(openFilePath,fileVar)  
    xListUTM = listsFromFile[0]
    yListUTM = listsFromFile[1]
    zListUTM = listsFromFile[2]
    timeList = listsFromFile[3]
    zoneList = listsFromFile[4]
    dateList = listsFromFile[5]

    latList = []
    longList = []


    ##Note: Ignore the last coordinates due to losing values bc of the ladder effect of the velocity and acceleration
    del xListUTM[0]
    del xListUTM[-1]
    del yListUTM[0]
    del yListUTM[-1]
    del zListUTM[0]
    del zListUTM[-1]
    del timeList[0]
    del timeList[-1]
    del zoneList[0]
    del zoneList[-1]
    del dateList[0]
    del dateList[-1]
     
    ##Convert UTM to Degrees
    numberOfElements = len(xListUTM)
    
    for i in range(0, numberOfElements):   
        latLongListTemporal = UTMtoLL(23, float(yListUTM[i]), float(xListUTM[i]), zoneList[i])
        latList.append(latLongListTemporal[0])
        longList.append(latLongListTemporal[1])
 
    return latList, longList, dateList, timeList,zListUTM
              

    
##********************Write KML file******************************************************************

def writeKMLfile(openFilePath,saveFilePath,massInput,var,checkVariable1,checkVariable3,unitsVariable,checkVariable4,fileVar):
    ##Number of Decimal places
    getcontext().prec = 3


    ##Create lists
    listsFromFile = getDataForKML(openFilePath,fileVar)
    latList = listsFromFile[0]
    longList = listsFromFile[1]
    dateList = listsFromFile[2]
    timeList = listsFromFile[3]
    altList = listsFromFile[4]


    ## Kinematics List
    
    calcList = readAndCalculate(openFilePath,massInput,fileVar)
    
    vxList = calcList[0]
    vyList = calcList[1]
    vzList = calcList[2]
    vTotalList = calcList[3]
    
    axList = calcList[4]
    ayList = calcList[5]
    azList = calcList[6]
    aTotalList = calcList[7]

    fxList = calcList[8]
    fyList = calcList[9]
    fzList = calcList[10]
    fTotalList = calcList[11]
    
    keList = calcList[18]
    peList = calcList[19]



    

    numberOfElements = len(latList)


    ##Algorithm to find breaks in the DATA (it does so by comparing dates)
    dateListBase = dateList[0]
    timeListBase = timeList[0]
    splitList = [0]
    ##checking date List    
    for i in range(0, numberOfElements-1):
        
       
        if dateList[i] != dateListBase:
            splitList.append(i)
            dateListBase = dateList[i]
            
        
    splitList.append(numberOfElements)

            

    ## This loop ensures that different animations are created for different data breaks
    dataBreaks = len(splitList)
    for i in range(0, dataBreaks-1):
        initial = splitList[i]
        final = splitList [i+1]
        







        file = open(saveFilePath+"GoogleEarth.kml", 'w')
    
        ##Coordinate Icon style
        file.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>'+'\n'+'\n'+'\n')
        file.write('<open>1</open>'+'\n')
        file.write('<Style id="icon"><IconStyle><Icon>')
        if var == 1:
            file.write('<href>http://maps.google.com/mapfiles/kml/shapes/hiker.png</href>')
        if var == 2:
            file.write('<href>http://maps.google.com/mapfiles/kml/shapes/cabs.png</href>')
        if var == 3:
            file.write('<href>http://maps.google.com/mapfiles/kml/shapes/motorcycling.png</href>')
        if var == 4:
            file.write('<href>http://maps.google.com/mapfiles/kml/shapes/sailing.png</href>')
        if var == 5:
            file.write('<href>http://maps.google.com/mapfiles/kml/shapes/airports.png</href>')
        file.write('</Icon></IconStyle></Style>'+'\n')



        
        ##Path Style
        file.write('<Style id="pathStyle"><LineStyle><color>beff8000</color><width>3</width></LineStyle></Style>'+'\n'+'\n'+'\n')
        file.write('<Style id="pathStyle2"><LineStyle><color>7f00ffff</color><width>3</width></LineStyle><PolyStyle><color>9600ff00</color></PolyStyle></Style>'+'\n'+'\n'+'\n')
        file.write('<Style id="end"><IconStyle><Icon>http://maps.google.com/mapfiles/kml/paddle/grn-diamond.png</Icon></IconStyle></Style>'+'\n')
        file.write('<Style id="start"><IconStyle><Icon>http://maps.google.com/mapfiles/kml/paddle/red-square.png</Icon></IconStyle></Style>'+'\n')
        
        ##Labels style
        file.write('<Style id="xLabel"><LabelStyle><color>ff00ff00</color><scale>0.8</scale></LabelStyle><IconStyle><scale>0</scale></IconStyle></Style>'+'\n')
        file.write('<Style id="yLabel"><LabelStyle><color>ff00ffff</color><scale>0.8</scale></LabelStyle><IconStyle><scale>0</scale></IconStyle></Style>'+'\n')
        file.write('<Style id="zLabel"><LabelStyle><color>ff0000ff</color><scale>0.8</scale></LabelStyle><IconStyle><scale>0</scale></IconStyle></Style>'+'\n')
        file.write('<Style id="netLabel"><LabelStyle><color>ffffff00</color><scale>0.8</scale></LabelStyle><IconStyle><scale>0</scale></IconStyle></Style>'+'\n')
        ##Vectors Style
        file.write('<Style id="windowVector"><LineStyle><color>ff00ffff</color><width>3</width></LineStyle></Style>'+'\n')
        file.write('<Style id="vectorXstyle"><LineStyle><color>ff00ff00</color><width>2</width></LineStyle></Style>'+'\n')
        file.write('<Style id="vectorYstyle"><LineStyle><color>ff00ffff</color><width>2</width></LineStyle></Style>'+'\n')
        file.write('<Style id="vectorZstyle"><LineStyle><color>ff0000ff</color><width>2</width></LineStyle></Style>'+'\n')
        file.write('<Style id="vectorTotalVelocityStyle"><LineStyle><color>ffffff00</color><width>2</width></LineStyle></Style>'+'\n')
        

        ##Yellow: 7d00ffff
        ##Blue: 7dff0000
        ##Blue sea:ffffff00
        ##Orange: 7d2274f8
        ##7dff8000 (old-current)

        ##http://www.sugarcreek.co.za/images/man.png
        ##http://maps.google.com/mapfiles/ms/icons/hiker.png
        ##http://maps.google.com/mapfiles/kml/paddle/A.png
        ##http://maps.google.com/mapfiles/kml/paddle/B.png
        ##http://www.britishairways.com/cms/global/assets/images/site/icon/planeIconSml.gif
        ##http://maps.google.com/mapfiles/kml/shapes/airports.png
        ##http://maps.google.com/mapfiles/kml/shapes/cabs.png
        ##http://maps.google.com/mapfiles/kml/paddle/grn-diamond.png  (end)
        ##http://maps.google.com/mapfiles/kml/paddle/red-square.png    (start)

        
        ##-----PATH LOOP
        file.write('<Folder><name>Path-Linear</name>'+'\n')

        ##Start-mark
        file.write('<Placemark>'+'\n')
        file.write('<styleUrl>#start</styleUrl>'+'\n')
        if var == 5:
            file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[initial])+','+str(latList[initial])+','+str(altList[initial])+'</coordinates></Point>'+'\n')
        if var != 5:
            file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[initial])+','+str(latList[initial])+','+str(altList[initial])+'</coordinates></Point>'+'\n')
        file.write('</Placemark>'+'\n')

        ##End-mark
        file.write('<Placemark>'+'\n')
        file.write('<styleUrl>#end</styleUrl>'+'\n')
        if var == 5:
            file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[final-1])+','+str(latList[final-1])+','+str(altList[final-1])+'</coordinates></Point>'+'\n')
        if var != 5:
            file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[final-1])+','+str(latList[final-1])+','+str(altList[final-1])+'</coordinates></Point>'+'\n')
        file.write('</Placemark>'+'\n')
        

        ##Path-Linear
        for i in range(initial, final-1):
            file.write('<Placemark>'+'\n')
            file.write('<styleUrl>#pathStyle</styleUrl>'+'\n')
            if var == 5:
                file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                ##<extrude>1</extrude><tessellate>1</tessellate>
            if var != 5:
                file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
            file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i+1])+','+str(latList[i+1])+','+str(altList[i+1])+'\n')
            file.write('</coordinates></LineString></Placemark>'+'\n')
        file.write('</Folder>'+'\n'+'\n')

        if var == 5:
            ##Path-Planar
            file.write('<Folder><visibility>1</visibility><name>Path-Planar</name>'+'\n')

            ##Start-mark
            file.write('<Placemark><visibility>1</visibility>'+'\n')
            file.write('<styleUrl>#start</styleUrl>'+'\n')
            file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[initial])+','+str(latList[initial])+','+str(altList[initial])+'</coordinates></Point>'+'\n')
            file.write('</Placemark>'+'\n')

            ##End-mark
            file.write('<Placemark><visibility>1</visibility>'+'\n')
            file.write('<styleUrl>#end</styleUrl>'+'\n')
            file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[final-1])+','+str(latList[final-1])+','+str(altList[final-1])+'</coordinates></Point>'+'\n')
            file.write('</Placemark>'+'\n')
            
            for i in range(initial, final-1):
                file.write('<Placemark><visibility>0</visibility>'+'\n')
                file.write('<styleUrl>#pathStyle2</styleUrl>'+'\n')
                file.write('<LineString><altitudeMode>absolute</altitudeMode><extrude>1</extrude><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i+1])+','+str(latList[i+1])+','+str(altList[i+1])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
            file.write('</Folder>'+'\n'+'\n')
   



        ##------COORDINATES Loop
        file.write('<Folder><name>Icon</name>'+'\n')
        file.write('<visibility>0</visibility>'+'\n')     
        for i in range(initial, final-1):
            ##Split the Date string into Month day and Year
            splittedDateList = dateList[i].split('/')
            month = splittedDateList[0]
            day = splittedDateList[1]
            year = splittedDateList[2]

            file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
            file.write('<styleUrl>#icon</styleUrl>'+'\n')
            if var == 5:
                file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+'</coordinates></Point>'+'\n')
            if var != 5:
                file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+'</coordinates></Point>'+'\n')
            file.write('</Placemark>'+'\n')
        file.write('</Folder>'+'\n'+'\n')





        longListTemp = longList[initial:(final-1)]
        latListTemp = latList[initial:(final-1)]
        altListTemp = altList[initial:(final-1)]


        ##------Window Loop
        longMin = min(longListTemp)
        latMax = max(latListTemp)
        altMax = max(altListTemp)
        
        
        
        file.write('<Folder><name>Window</name>'+'\n')
        file.write('<visibility>0</visibility>'+'\n')   
        
        file.write('<Folder><visibility>0</visibility><name>Borders</name>'+'\n')
        ##Up
        file.write('<Placemark><visibility>0</visibility>'+'\n')
        file.write('<styleUrl>#windowVector</styleUrl>'+'\n')
        if var == 5:
            file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
        if var != 5:
            file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
        file.write('<coordinates>'+str(longMin-0.02)+','+str(latMax+0.005)+','+str(altMax)+' '+str(longMin-0.06)+','+str(latMax+0.005)+','+str(altMax)+'\n')
        file.write('</coordinates></LineString></Placemark>'+'\n')



       ##Down
        file.write('<Placemark><visibility>0</visibility>'+'\n')
        file.write('<styleUrl>#windowVector</styleUrl>'+'\n')
        if var == 5:
            file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
        if var != 5:
            file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
        file.write('<coordinates>'+str(longMin-0.02)+','+str(latMax-0.028)+','+str(altMax)+' '+str(longMin-0.06)+','+str(latMax-0.028)+','+str(altMax)+'\n')
        file.write('</coordinates></LineString></Placemark>'+'\n')    


        ##Right
        file.write('<Placemark><visibility>0</visibility>'+'\n')
        file.write('<styleUrl>#windowVector</styleUrl>'+'\n')
        if var == 5:
            file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
        if var != 5:
            file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
        file.write('<coordinates>'+str(longMin-0.02)+','+str(latMax+0.005)+','+str(altMax)+' '+str(longMin-0.02)+','+str(latMax-0.028)+','+str(altMax)+'\n')
        file.write('</coordinates></LineString></Placemark>'+'\n')    

        ##Left
        file.write('<Placemark><visibility>0</visibility>'+'\n')
        file.write('<styleUrl>#windowVector</styleUrl>'+'\n')
        if var == 5:
            file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
        if var != 5:
            file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
        file.write('<coordinates>'+str(longMin-0.06)+','+str(latMax+0.005)+','+str(altMax)+' '+str(longMin-0.06)+','+str(latMax-0.028)+','+str(altMax)+'\n')
        file.write('</coordinates></LineString></Placemark>'+'\n')
        file.write('</Folder>'+'\n')


        ##Kinetic Energy (Label)
        file.write('<Folder><visibility>0</visibility><name>Kinetic Energy</name>'+'\n')
        
        file.write('<Placemark><visibility>0</visibility><name>:K.E:    </name>')
        file.write('<styleUrl>#yLabel</styleUrl>'+'\n')
        if var == 5:
            file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n')
        if var != 5:
            file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n')
        file.write('<coordinates>'+str(longMin-0.05)+','+str(latMax-0.003)+','+str(altMax)+'\n')
        file.write('</coordinates></Point></Placemark>'+'\n')



            
             
        ##Values inside box
        ##(Kinetic Energy)



        for i in range(initial, final-1):
            ##Split the Date string into Month day and Year
            splittedDateList = dateList[i].split('/')
            month = splittedDateList[0]
            day = splittedDateList[1]
            year = splittedDateList[2]

            file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(keList[i]))*(Decimal(str(1.0))))+' J'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
            file.write('<styleUrl>#yLabel</styleUrl>'+'\n')
            if var == 5:
                file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n')
            if var != 5:
                file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n')
            file.write('<coordinates>'+str(longMin-0.03)+','+str(latMax-0.003)+','+str(altMax)+'\n')
            file.write('</coordinates></Point></Placemark>'+'\n')
        file.write('</Folder>'+'\n')

        
         




        ##Potential Energy (Label)
        file.write('<Folder><visibility>0</visibility><name>Potential Energy</name>'+'\n')
        file.write('<Placemark><visibility>0</visibility><name>:P.E:     </name>')
        file.write('<styleUrl>#yLabel</styleUrl>'+'\n')

        if var == 5:
            file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n')
        if var != 5:
            file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n')
        file.write('<coordinates>'+str(longMin-0.05)+','+str(latMax-0.020)+','+str(altMax)+'\n')
        file.write('</coordinates></Point></Placemark>'+'\n')
        
        ##Values (Potential Energy)
        for i in range(initial, final-1):
            ##Split the Date string into Month day and Year
            splittedDateList = dateList[i].split('/')
            month = splittedDateList[0]
            day = splittedDateList[1]
            year = splittedDateList[2]

            file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(peList[i]))*(Decimal(str(1.0))))+' J'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
            file.write('<styleUrl>#yLabel</styleUrl>'+'\n')
            if var == 5:
                file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n')
            if var != 5:
                file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n')
            file.write('<coordinates>'+str(longMin-0.03)+','+str(latMax-0.020)+','+str(altMax)+'\n')
            file.write('</coordinates></Point></Placemark>'+'\n')
        file.write('</Folder>'+'\n')
        
        file.write('</Folder>'+'\n'+'\n')









































        ##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@^%$#$%^&*(*&^%$#@#$%^&*()_)(*&^%$#@@#$%^&*()(*&^%$#@#$%^&*
        #### *********************************Acceleration VECTORS *********************************************
        if checkVariable3 == 1:

            ##Create Factor Numbers
            xNumber = 0.0017
            yNumber = 0.0014
            zNumber = 155



            ##print axList[0], ayList[0], azList[0], aTotalList[0]

            file.write('<Folder><visibility>1</visibility><name>Acceleration_Vectors</name>'+'\n')
            
                
            ####LONGITUD Vector (x)
            file.write('<Folder><visibility>0</visibility><name>Easting_Component</name>'+'\n')

            ##Values
            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]

                xFactor = 2 *(axList[i] * xNumber)
                yFactor = 2 *(ayList[i] * yNumber)
                zFactor = 2 *(azList[i] * zNumber)
                
                file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(axList[i]))*(Decimal(str(1.0))))+' m/(s*s)'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#yLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.3*xFactor))+','+str(latList[i])+','+str(altList[i])+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.3*xFactor))+','+str(latList[i])+','+str(altList[i])+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')
            file.write('</Folder>'+'\n'+'\n')


            ##Data Points
            file.write('<Folder><visibility>0</visibility><name>Data_Points</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]


                ## ----IMPORTANT REMINDER: To calibrate vectors, set vxList, vyList, vzList equal to the same number. Then measure vectors on the screen, and adjust xNumber, yNumber, zNumber above accoordinly. 

                ##Length of vectors
                xFactor = 2 *(axList[i] * xNumber)
                yFactor = 2 *(ayList[i] * yNumber)
                zFactor = 2 *(azList[i] * zNumber)
                
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorYstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i])+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
                ##**Finishing of Longitud vector
                xlengthOfPoint = xFactor/10
                ##Down
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorYstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xFactor-xlengthOfPoint)+','+str(latList[i]-(0.3*xlengthOfPoint))+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i])+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
                ##Up
                lengthOfPoint = xFactor/10
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorYstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xFactor-xlengthOfPoint)+','+str(latList[i]+(0.3*xlengthOfPoint))+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i])+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')





            
            ####LATITUD Vector (x)
            file.write('<Folder><visibility>0</visibility><name>Northing_Component</name>'+'\n')
            
            ##Values
            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]

                xFactor = 2*(axList[i] * xNumber)
                yFactor = 2*(ayList[i] * yNumber)
                zFactor = 2*(azList[i] * zNumber)
                
                file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(ayList[i]))*(Decimal(str(1.0))))+' m/(s*s)'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#xLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i]+(1.1*yFactor))+','+str(altList[i])+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i]+(1.1*yFactor))+','+str(altList[i])+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')
            file.write('</Folder>'+'\n'+'\n')


            ##Data Points
            file.write('<Folder><visibility>0</visibility><name>Data_Points</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]



                ##Length of vectors
                xFactor = 2 *(axList[i] * xNumber)
                yFactor = 2 *(ayList[i] * yNumber)
                zFactor = 2 *(azList[i] * zNumber)

                
                ##LATITUD Vector (y)
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorXstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i]+yFactor)+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')

                ##**Finishing of Latitud vector
                ##Right
                ylengthOfPoint = yFactor/10
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorXstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+(0.3*ylengthOfPoint))+','+str(latList[i]+yFactor-ylengthOfPoint)+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i]+yFactor)+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
                ##Left
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorXstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]-(0.3*ylengthOfPoint))+','+str(latList[i]+yFactor-ylengthOfPoint)+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i]+yFactor)+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
                           
            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')







        
            ##ALTITUD Vector(z)  
            file.write('<Folder><visibility>0</visibility><name>Altitude_Component</name>'+'\n')

            
            ##Values
            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]

                xFactor = 2 *(axList[i] * xNumber)
                yFactor = 2 *(ayList[i] * yNumber)
                zFactor = 2 *(azList[i] * zNumber)
                
                file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(azList[i]))*(Decimal(str(1.0))))+' m/(s*s)'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#netLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')
            file.write('</Folder>'+'\n'+'\n')


            ##Data Points
            file.write('<Folder><visibility>0</visibility><name>Data_Points</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]



                ##Length of vectors
                xFactor = 2 *(axList[i] * xNumber)
                yFactor = 2 *(ayList[i] * yNumber)
                zFactor = 2 *(azList[i] * zNumber)
                
                      
                if var == 5:
                    file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                    file.write('<styleUrl>#vectorTotalVelocityStyle</styleUrl>'+'\n')
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                    file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+zFactor)+'\n')
                    file.write('</coordinates></LineString></Placemark>'+'\n'+'\n')

                ##Finishing of Altitude Vector
                    zlengthOfPoint = zFactor/10
                ##Left
                    file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                    file.write('<styleUrl>#vectorTotalVelocityStyle</styleUrl>'+'\n')
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                    file.write('<coordinates>'+str(longList[i]+(0.00001096*zlengthOfPoint))+','+str(latList[i]+(0.000009032*zlengthOfPoint))+','+str(float(altList[i])+zFactor-zlengthOfPoint)+' '+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+zFactor)+'\n')
                    file.write('</coordinates></LineString></Placemark>'+'\n'+'\n')
                
                ##Right
                    file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                    file.write('<styleUrl>#vectorTotalVelocityStyle</styleUrl>'+'\n')
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                    file.write('<coordinates>'+str(longList[i]-(0.00001096*zlengthOfPoint))+','+str(latList[i]-(0.000009032*zlengthOfPoint))+','+str(float(altList[i])+zFactor-zlengthOfPoint)+' '+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+zFactor)+'\n')
                    file.write('</coordinates></LineString></Placemark>'+'\n'+'\n')

            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')








            ##Net Acceleration Vector
            file.write('<Folder><visibility>0</visibility><name>Net_Acceleration</name>'+'\n')

            ##Values
            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]

                xFactor = 2 *(axList[i] * xNumber)
                yFactor = 2 *(ayList[i] * yNumber)
                zFactor = 2 *(azList[i] * zNumber)
                
                ##Net Velocity Values               
                file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(aTotalList[i]))*(Decimal(str(1.0))))+' m/(s*s)'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#zLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.1*xFactor))+','+str(latList[i]+(1.1*yFactor))+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.1*xFactor))+','+str(latList[i]+(1.1*yFactor))+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')
            file.write('</Folder>'+'\n'+'\n')


            ##Data Points
            file.write('<Folder><visibility>0</visibility><name>Data_Points</name>'+'\n')        
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]



                ##Length of vectors
                xFactor = 2 *(axList[i] * xNumber)
                yFactor = 2 *(ayList[i] * yNumber)
                zFactor = 2 *(azList[i] * zNumber)
                

                ###Net Acceleration Vector
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorZstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i]+yFactor)+','+str(float(altList[i])+zFactor)+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')


                ##**Finishing of Net Acceleration vector
                netLengthOfPoint = (sqrt((xFactor*xFactor)+(yFactor*yFactor)))

                if xFactor == 0:
                    thetta = 90
                else:
                    thetta = math.atan(abs(yFactor)/abs(xFactor))*(180/pi)
                newHeigth = zFactor*0.9*math.cos(2*(pi/180))

                ##Down
                ganma = thetta - 2
                xx = math.cos(ganma*(pi/180))*(0.9*netLengthOfPoint)
                yy = math.sin(ganma*(pi/180))*(0.9*netLengthOfPoint)
                ##Locating Quadrant
                if xFactor <= 0:
                    xx = xx * (-1)
                if yFactor <= 0:
                    yy = yy * (-1)

                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorZstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xx)+','+str(latList[i]+yy)+','+str(float(altList[i])+newHeigth)+' '+str(longList[i]+xFactor)+','+str(latList[i]+yFactor)+','+str(float(altList[i])+zFactor)+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')

            
                ##Up
                ganma2 = thetta + 2
                xx2 = math.cos(ganma2*(pi/180))*(0.9*netLengthOfPoint)
                yy2 = math.sin(ganma2*(pi/180))*(0.9*netLengthOfPoint)
                ##Locating Quadrant
                if xFactor <= 0:
                    xx2 = xx2 * (-1)
                if yFactor <= 0:
                    yy2 = yy2 * (-1)
                    
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorZstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xx2)+','+str(latList[i]+yy2)+','+str(float(altList[i])+newHeigth)+' '+str(longList[i]+xFactor)+','+str(latList[i]+yFactor)+','+str(float(altList[i])+zFactor)+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')

            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')

        


        













        ##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@^%$#$%^&*(*&^%$#@#$%^&*()_)(*&^%$#@@#$%^&*()(*&^%$#@#$%^&*
        #### *********************************FORCE VECTORS *********************************************
        if checkVariable4 == 1:

            
            ##Create Factor Numbers
            xNumber = 0.0017
            yNumber = 0.0014
            zNumber = 155



            file.write('<Folder><visibility>0</visibility><name>Force_Vectors</name>'+'\n')
            
                
            ####LONGITUD Vector (x)
            file.write('<Folder><visibility>0</visibility><name>Easting_Component</name>'+'\n')

            ##Values
            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]

                xFactor = 0.002 * (fxList[i] * xNumber)
                yFactor = 0.002 * (fyList[i] * yNumber)
                zFactor = 0.002 * (fzList[i] * zNumber)
                
                file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(fxList[i]))*(Decimal(str(1.0))))+' N'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#zLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.3*xFactor))+','+str(latList[i])+','+str(altList[i])+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.3*xFactor))+','+str(latList[i])+','+str(altList[i])+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')
            file.write('</Folder>'+'\n'+'\n')


            ##Data Points
            file.write('<Folder><visibility>0</visibility><name>Data_Points</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]


                ## ----IMPORTANT REMINDER: To calibrate vectors, set vxList, vyList, vzList equal to the same number. Then measure vectors on the screen, and adjust xNumber, yNumber, zNumber above accoordinly. 

                ##Length of vectors
                xFactor = 0.002 * (fxList[i] * xNumber)
                yFactor = 0.002 * (fyList[i] * yNumber)
                zFactor = 0.002 * (fzList[i] * zNumber)
                
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorZstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i])+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
                ##**Finishing of Longitud vector
                xlengthOfPoint = xFactor/10
                ##Down
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorZstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xFactor-xlengthOfPoint)+','+str(latList[i]-(0.3*xlengthOfPoint))+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i])+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
                ##Up
                lengthOfPoint = xFactor/10
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorZstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xFactor-xlengthOfPoint)+','+str(latList[i]+(0.3*xlengthOfPoint))+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i])+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')









            
            ####LATITUD Vector (x)
            file.write('<Folder><visibility>0</visibility><name>Northing_Component</name>'+'\n')
            
            ##Values
            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]

                xFactor = 0.002 * (fxList[i] * xNumber)
                yFactor = 0.002 * (fyList[i] * yNumber)
                zFactor = 0.002 * (fzList[i] * zNumber)
                
                file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(fyList[i]))*(Decimal(str(1.0))))+' N'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#yLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i]+(1.1*yFactor))+','+str(altList[i])+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i]+(1.1*yFactor))+','+str(altList[i])+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')
            file.write('</Folder>'+'\n'+'\n')


            ##Data Points
            file.write('<Folder><visibility>0</visibility><name>Data_Points</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]



                ##Length of vectors
                xFactor = 0.002 * (fxList[i] * xNumber)
                yFactor = 0.002 * (fyList[i] * yNumber)
                zFactor = 0.002 * (fzList[i] * zNumber)
                
                ##LATITUD Vector (y)
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorYstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i]+yFactor)+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')

                ##**Finishing of Latitud vector
                ##Right
                ylengthOfPoint = yFactor/10
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorYstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+(0.3*ylengthOfPoint))+','+str(latList[i]+yFactor-ylengthOfPoint)+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i]+yFactor)+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
                ##Left
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorYstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]-(0.3*ylengthOfPoint))+','+str(latList[i]+yFactor-ylengthOfPoint)+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i]+yFactor)+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
                           
            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')









            ##ALTITUD Vector(z)  
            file.write('<Folder><visibility>0</visibility><name>Altitude_Component</name>'+'\n')

            
            ##Values
            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]

                xFactor = 0.002 * (fxList[i] * xNumber)
                yFactor = 0.002 * (fyList[i] * yNumber)
                zFactor = 0.002 * (fzList[i] * zNumber)
                
                file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(fzList[i]))*(Decimal(str(1.0))))+' N'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#netLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')
            file.write('</Folder>'+'\n'+'\n')


            ##Data Points
            file.write('<Folder><visibility>0</visibility><name>Data_Points</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]



                ##Length of vectors
                xFactor = 0.002 * (fxList[i] * xNumber)
                yFactor = 0.002 * (fyList[i] * yNumber)
                zFactor = 0.002 * (fzList[i] * zNumber)

                
                      
                if var == 5:
                    file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                    file.write('<styleUrl>#vectorTotalVelocityStyle</styleUrl>'+'\n')
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                    file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+zFactor)+'\n')
                    file.write('</coordinates></LineString></Placemark>'+'\n'+'\n')

                ##Finishing of Altitude Vector
                    zlengthOfPoint = zFactor/10
                ##Left
                    file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                    file.write('<styleUrl>#vectorTotalVelocityStyle</styleUrl>'+'\n')
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                    file.write('<coordinates>'+str(longList[i]+(0.00001096*zlengthOfPoint))+','+str(latList[i]+(0.000009032*zlengthOfPoint))+','+str(float(altList[i])+zFactor-zlengthOfPoint)+' '+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+zFactor)+'\n')
                    file.write('</coordinates></LineString></Placemark>'+'\n'+'\n')
                
                ##Right
                    file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                    file.write('<styleUrl>#vectorTotalVelocityStyle</styleUrl>'+'\n')
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                    file.write('<coordinates>'+str(longList[i]-(0.00001096*zlengthOfPoint))+','+str(latList[i]-(0.000009032*zlengthOfPoint))+','+str(float(altList[i])+zFactor-zlengthOfPoint)+' '+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+zFactor)+'\n')
                    file.write('</coordinates></LineString></Placemark>'+'\n'+'\n')

            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')








            ##Net Force Vector
            file.write('<Folder><visibility>0</visibility><name>Net_Force</name>'+'\n')

            ##Values
            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]

                
                xFactor = 0.002 * (fxList[i] * xNumber)
                yFactor = 0.002 * (fyList[i] * yNumber)
                zFactor = 0.002 * (fzList[i] * zNumber)
                
                ##Net Velocity Values               
                file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(fTotalList[i]))*(Decimal(str(1.0))))+' N'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#xLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.1*xFactor))+','+str(latList[i]+(1.1*yFactor))+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.1*xFactor))+','+str(latList[i]+(1.1*yFactor))+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')
            file.write('</Folder>'+'\n'+'\n')


            ##Data Points
            file.write('<Folder><visibility>0</visibility><name>Data_Points</name>'+'\n')        
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]



                ##Length of vectors
                xFactor = 0.002 * (fxList[i] * xNumber)
                yFactor = 0.002 * (fyList[i] * yNumber)
                zFactor = 0.002 * (fzList[i] * zNumber)
                

                ###Net Velocity Vector
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorXstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i]+yFactor)+','+str(float(altList[i])+zFactor)+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')


                ##**Finishing of Net Acceleration vector
                netLengthOfPoint = (sqrt((xFactor*xFactor)+(yFactor*yFactor)))

                if xFactor == 0:
                    thetta = 90
                else:
                    thetta = math.atan(abs(yFactor)/abs(xFactor))*(180/pi)
                newHeigth = zFactor*0.9*math.cos(2*(pi/180))

                ##Down
                ganma = thetta - 2
                xx = math.cos(ganma*(pi/180))*(0.9*netLengthOfPoint)
                yy = math.sin(ganma*(pi/180))*(0.9*netLengthOfPoint)
                ##Locating Quadrant
                if xFactor <= 0:
                    xx = xx * (-1)
                if yFactor <= 0:
                    yy = yy * (-1)

                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorXstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xx)+','+str(latList[i]+yy)+','+str(float(altList[i])+newHeigth)+' '+str(longList[i]+xFactor)+','+str(latList[i]+yFactor)+','+str(float(altList[i])+zFactor)+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')

            
                ##Up
                ganma2 = thetta + 2
                xx2 = math.cos(ganma2*(pi/180))*(0.9*netLengthOfPoint)
                yy2 = math.sin(ganma2*(pi/180))*(0.9*netLengthOfPoint)
                ##Locating Quadrant
                if xFactor <= 0:
                    xx2 = xx2 * (-1)
                if yFactor <= 0:
                    yy2 = yy2 * (-1)
                    
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorXstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xx2)+','+str(latList[i]+yy2)+','+str(float(altList[i])+newHeigth)+' '+str(longList[i]+xFactor)+','+str(latList[i]+yFactor)+','+str(float(altList[i])+zFactor)+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')

            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')


            
            file.write('</Folder>'+'\n')










































        #### *********************************VELOCITY VECTORS *********************************************
        if checkVariable1 == 1:
            
            ##Create Factor Numbers
            ##xNumber = 0.0017
            ##yNumber = 0.0014
            ##zNumber = 155

            xNumber = 0.0017
            yNumber = 0.0014
            zNumber = 155


            
            file.write('<Folder><visibility>1</visibility><name>Velocity_Vectors</name>'+'\n')

            
            ##----VELOCITY VECTORS LOOP






            ##LONGITUD Vector (x)        
            file.write('<Folder><visibility>0</visibility><name>Easting_Component</name>'+'\n')
            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]


                #Calibrating
                ##vxList[i] = 8.94
                ##vyList[i] = 8.94
                ##vzList[i] = 8.94


                xFactor = 0.5 * (vxList[i] * xNumber)
                yFactor = 0.5 * (vyList[i] * yNumber)
                zFactor = 0.5 * (vzList[i] * zNumber)
                
                ##Longitud Velocity Values
                if unitsVariable == 1:
                    file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(vxList[i]))*(Decimal(str(1.0))))+' m/s'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                else:
                    file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(vxList[i]*(3600/1609.344)))*(Decimal(str(1.0))))+' mph'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#xLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.1*xFactor))+','+str(latList[i])+','+str(altList[i])+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.1*xFactor))+','+str(latList[i])+','+str(altList[i])+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')

            file.write('</Folder>'+'\n')
                

            file.write('<Folder><visibility>0</visibility><name>Data_Points</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]


                ## ----IMPORTANT REMINDER: To calibrate vectors, set vxList, vyList, vzList equal to the same number. Then measure vectors on the screen, and adjust xNumber, yNumber, zNumber above accoordinly. 


                #Calibrating
                ##vxList[i] = 8.94
                ##vyList[i] = 8.94
                ##vzList[i] = 8.94
                
                ##Length of vectors
                xFactor = 0.5 * (vxList[i] * xNumber)
                yFactor = 0.5 * (vyList[i] * yNumber)
                zFactor = 0.5 * (vzList[i] * zNumber)
                
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorXstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i])+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')

                ##**Finishing of Longitud vector
                xlengthOfPoint = xFactor/10
                ##Down
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorXstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xFactor-xlengthOfPoint)+','+str(latList[i]-(0.3*xlengthOfPoint))+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i])+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
                ##Up
                lengthOfPoint = xFactor/10
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorXstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xFactor-xlengthOfPoint)+','+str(latList[i]+(0.3*xlengthOfPoint))+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i])+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')

            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')








            ##LATITUD Vector (x)
            file.write('<Folder><visibility>0</visibility><name>Northing_Component</name>'+'\n')

            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]


                xFactor = 0.5 * (vxList[i] * xNumber)
                yFactor = 0.5 * (vyList[i] * yNumber)
                zFactor = 0.5 * (vzList[i] * zNumber)
                

                if unitsVariable == 1:
                    file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(vyList[i]))*(Decimal(str(1.0))))+' m/s'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                else:
                    file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(vyList[i]*(3600/1609.344)))*(Decimal(str(1.0))))+' mph'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#yLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i]+(1.1*yFactor))+','+str(altList[i])+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i]+(1.1*yFactor))+','+str(altList[i])+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')

            file.write('</Folder>'+'\n')
                

            file.write('<Folder><visibility>0</visibility><name>Data_Points</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]


                ##Length of vectors
                xFactor = 0.5 * (vxList[i] * xNumber)
                yFactor = 0.5 * (vyList[i] * yNumber)
                zFactor = 0.5 * (vzList[i] * zNumber)

                
                ##LATITUD Vector (y)
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorYstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i]+yFactor)+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')

                ##**Finishing of Latitud vector
                ##Right
                ylengthOfPoint = yFactor/10
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorYstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+(0.3*ylengthOfPoint))+','+str(latList[i]+yFactor-ylengthOfPoint)+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i]+yFactor)+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
                ##Left
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorYstyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]-(0.3*ylengthOfPoint))+','+str(latList[i]+yFactor-ylengthOfPoint)+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i]+yFactor)+','+str(altList[i])+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')
                           
            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')







            
            ##ALTITUD Vector(z)  
            file.write('<Folder><visibility>1</visibility><name>Altitude_Component</name>'+'\n')

            ##Values        
            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]

                
                xFactor = 0.5 * (vxList[i] * xNumber)
                yFactor = 0.5 * (vyList[i] * yNumber)
                zFactor = 0.5 * (vzList[i] * zNumber)
                

               
                if unitsVariable == 1:
                    file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(vzList[i]))*(Decimal(str(1.0))))+' m/s'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                else:
                    file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(vzList[i]*(3600/1609.344)))*(Decimal(str(1.0))))+'mph'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#zLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')

            file.write('</Folder>'+'\n')
                

            file.write('<Folder><visibility>1</visibility><name>Data_Points</name>'+'\n')
            
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]


                ##Length of vectors
                xFactor = 0.5 * (vxList[i] * xNumber)
                yFactor = 0.5 * (vyList[i] * yNumber)
                zFactor = 0.5 * (vzList[i] * zNumber)

                
                      
                if var == 5:
                    file.write('<Placemark><visibility>1</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                    file.write('<styleUrl>#vectorZstyle</styleUrl>'+'\n')
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                    file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+zFactor)+'\n')
                    file.write('</coordinates></LineString></Placemark>'+'\n'+'\n')

                ##Finishing of Altitude Vector
                    zlengthOfPoint = zFactor/10
                ##Left
                    file.write('<Placemark><visibility>1</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                    file.write('<styleUrl>#vectorZstyle</styleUrl>'+'\n')
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                    file.write('<coordinates>'+str(longList[i]+(0.00001096*zlengthOfPoint))+','+str(latList[i]+(0.000009032*zlengthOfPoint))+','+str(float(altList[i])+zFactor-zlengthOfPoint)+' '+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+zFactor)+'\n')
                    file.write('</coordinates></LineString></Placemark>'+'\n'+'\n')
                
                ##Right
                    file.write('<Placemark><visibility>1</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                    file.write('<styleUrl>#vectorZstyle</styleUrl>'+'\n')
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                    file.write('<coordinates>'+str(longList[i]-(0.00001096*zlengthOfPoint))+','+str(latList[i]-(0.000009032*zlengthOfPoint))+','+str(float(altList[i])+zFactor-zlengthOfPoint)+' '+str(longList[i])+','+str(latList[i])+','+str(float(altList[i])+zFactor)+'\n')
                    file.write('</coordinates></LineString></Placemark>'+'\n'+'\n')

            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')






            ##Net_Vector
            file.write('<Folder><visibility>0</visibility><name>Net_Velocity</name>'+'\n')

            ##Values        
            file.write('<Folder><visibility>0</visibility><name>Values</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]


                xFactor = 0.5 * (vxList[i] * xNumber)
                yFactor = 0.5 * (vyList[i] * yNumber)
                zFactor = 0.5 * (vzList[i] * zNumber)
                

      
                if unitsVariable == 1:
                    file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(vTotalList[i]))*(Decimal(str(1.0))))+' m/s'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                else:
                    file.write('<Placemark><visibility>0</visibility><name>'+str(Decimal(str(vTotalList[i]*(3600/1609.344)))*(Decimal(str(1.0))))+' mph'+'</name><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#netLabel</styleUrl>'+'\n')
                if var == 5:
                    file.write('<Point><altitudeMode>absolute</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.1*xFactor))+','+str(latList[i]+(1.1*yFactor))+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                if var != 5:
                    file.write('<Point><altitudeMode>clampToGround</altitudeMode>'+'\n'+'<coordinates>'+str(longList[i]+(1.1*xFactor))+','+str(latList[i]+(1.1*yFactor))+','+str(float(altList[i])+(1.1*zFactor))+'</coordinates></Point>'+'\n')
                file.write('</Placemark>'+'\n')


            file.write('</Folder>'+'\n')
                

            file.write('<Folder><visibility>0</visibility><name>Data_Points</name>'+'\n')
            for i in range(initial, final-1):
                ##Split the Date string into Month day and Year
                splittedDateList = dateList[i].split('/')
                month = splittedDateList[0]
                day = splittedDateList[1]
                year = splittedDateList[2]


                ##Length of vectors
                xFactor = 0.5 * (vxList[i] * xNumber)
                yFactor = 0.5 * (vyList[i] * yNumber)
                zFactor = 0.5 * (vzList[i] * zNumber)
                

                ###Net Velocity Vector
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorTotalVelocityStyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i])+','+str(latList[i])+','+str(altList[i])+' '+str(longList[i]+xFactor)+','+str(latList[i]+yFactor)+','+str(float(altList[i])+zFactor)+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')


                ##**Finishing of Net Velocity vector
                netLengthOfPoint = (sqrt((xFactor*xFactor)+(yFactor*yFactor)))

                if xFactor == 0:
                    thetta = 90
                else:
                    thetta = math.atan(abs(yFactor)/abs(xFactor))*(180/pi)
                newHeigth = zFactor*0.9*math.cos(2*(pi/180))

                ##Down
                ganma = thetta - 2
                xx = math.cos(ganma*(pi/180))*(0.9*netLengthOfPoint)
                yy = math.sin(ganma*(pi/180))*(0.9*netLengthOfPoint)
                ##Locating Quadrant
                if xFactor <= 0:
                    xx = xx * (-1)
                if yFactor <= 0:
                    yy = yy * (-1)

                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorTotalVelocityStyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xx)+','+str(latList[i]+yy)+','+str(float(altList[i])+newHeigth)+' '+str(longList[i]+xFactor)+','+str(latList[i]+yFactor)+','+str(float(altList[i])+zFactor)+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')

            
                ##Up
                ganma2 = thetta + 2
                xx2 = math.cos(ganma2*(pi/180))*(0.9*netLengthOfPoint)
                yy2 = math.sin(ganma2*(pi/180))*(0.9*netLengthOfPoint)
                ##Locating Quadrant
                if xFactor <= 0:
                    xx2 = xx2 * (-1)
                if yFactor <= 0:
                    yy2 = yy2 * (-1)
                    
                file.write('<Placemark><visibility>0</visibility><TimeStamp><when>'+year+'-'+month+'-'+day+'T'+timeList[i]+'Z</when></TimeStamp>'+'\n')
                file.write('<styleUrl>#vectorTotalVelocityStyle</styleUrl>'+'\n')
                if var == 5:
                    file.write('<LineString><altitudeMode>absolute</altitudeMode>'+'\n')
                if var != 5:
                    file.write('<LineString><altitudeMode>clampToGround</altitudeMode><tessellate>1</tessellate>'+'\n')
                file.write('<coordinates>'+str(longList[i]+xx2)+','+str(latList[i]+yy2)+','+str(float(altList[i])+newHeigth)+' '+str(longList[i]+xFactor)+','+str(latList[i]+yFactor)+','+str(float(altList[i])+zFactor)+'\n')
                file.write('</coordinates></LineString></Placemark>'+'\n')

            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')
            file.write('</Folder>'+'\n')

            
        file.write('</Document></kml>')
        file.close()
    # tkMessageBox.showinfo("Operation Completed","Files have been created @:"+"\n"+"\n"+saveFilePath)

def writeCoordinateFile(openFilePath,saveFilePath,massInput,fileVar):
    ## Extract lists from TXT file using readFile function
    listsFromFile = readFile(openFilePath,fileVar)
    xListUTM = listsFromFile[0]
    yListUTM = listsFromFile[1]
    zListUTM = listsFromFile[2]
    timeList = listsFromFile[3]
    zoneList = listsFromFile[4]
    dateList = listsFromFile[5]


    ##Note: Ignore the first two coordinates due to losing values bc of the ladder effect of the velocity and acceleration
    del xListUTM[0]
    del xListUTM[-1]
    del yListUTM[0]
    del yListUTM[-1]
    del zListUTM[0]
    del zListUTM[-1]
    del timeList[0]
    del timeList[-1]
    del zoneList[0]
    del zoneList[-1]
    del dateList[0]
    del dateList[-1]
    
    listsFromFile2 = readAndCalculate(openFilePath,massInput,fileVar)
    VxList = listsFromFile2[0]
    VyList = listsFromFile2[1]
    VzList = listsFromFile2[2]
    VtotalList = listsFromFile2[3]
    AxList = listsFromFile2[4]
    AyList = listsFromFile2[5]
    AzList = listsFromFile2[6]
    AtotalList = listsFromFile2[7]
    FxList = listsFromFile2[8]
    FyList = listsFromFile2[9]
    FzList = listsFromFile2[10]
    FtotalList = listsFromFile2[11]
    NetPowList = listsFromFile2[12]
    wworkXlist = listsFromFile2[13]
    wworkYlist = listsFromFile2[14]
    wworkZlist = listsFromFile2[15]
    wworkTotalList = listsFromFile2[16]
    wworkList = listsFromFile2[17]
    keList = listsFromFile2[18]
    peList = listsFromFile2[19]


  
    
    check1 = 0
    file = open(saveFilePath+"Coordinates.txt",'w')
    file.write("x_Coordinate,y_coordinate,z_coordinate,time_seconds"+"\n")
    ##file.write("x_Coordinate,y_coordinate,z_coordinate,time_seconds,Vx,Vy,Vz,Vtotal,Ax,Ay,Az,Atotal,Fx,Fy,Fz,Ftotal,NetPower,workXlist,workYlist,workZlist,workTotalList, work, KE, PE"+"\n")

    baseZone = zoneList[0]
    
    numberOfElements = len(xListUTM)
    for i in range(0, numberOfElements-1):
        
        ##Converting Time to seconds
        timeArray = timeList[i].split(':')
        hours = float(timeArray[0]) * (3600.0)
        minutes = float(timeArray[1]) * (60)
        seconds = float(timeArray[2])
        timeSeconds = str(hours+minutes+seconds)

        if zoneList[i] == baseZone:
            ##Writing out lists to Text file
            file.write(str(xListUTM[i])+','+str(yListUTM[i])+','+str(zListUTM[i])+','+str(timeSeconds)+'\n')
            ##(All the results)
            ##file.write(str(xListUTM[i])+','+str(yListUTM[i])+','+str(zListUTM[i])+','+str(timeSeconds)+','+str(VxList[i])+','+str(VyList[i])+','+str(VzList[i])+','+str(VtotalList[i])+','+str(AxList[i])+','+str(AyList[i])+','+str(AzList[i])+','+str(AtotalList[i])+','+str(FxList[i])+','+str(FyList[i])+','+str(FzList[i])+','+str(FtotalList[i])+','+str(NetPowList[i])+','+str(wworkXlist[i])+','+str(wworkYlist[i])+','+str(wworkZlist[i])+','+str(wworkTotalList[i])+','+str(wworkList[i])+','+str(keList[i])+','+str(peList[i])+'\n')
            check1 = 0
        else:
            ##Algorithm that corrects Data with Different zones problem
            if check1 == 0:
                diference = abs(float(xListUTM[i-1])-float(xListUTM[i]))
                check1 = 1
                ##file.write(str(abs((float(xListUTM[i])-diference)))+','+str(yListUTM[i])+','+str(zListUTM[i])+','+str(timeSeconds)+','+str(VxList[i])+','+str(VyList[i])+','+str(VzList[i])+','+str(VtotalList[i])+','+str(AxList[i])+','+str(AyList[i])+','+str(AzList[i])+','+str(AtotalList[i])+','+str(FxList[i])+','+str(FyList[i])+','+str(FzList[i])+','+str(FtotalList[i])+','+str(NetPowList[i])+','+str(wworkXlist[i])+','+str(wworkYlist[i])+','+str(wworkZlist[i])+','+str(wworkTotalList[i])+','+str(wworkList[i])+','+str(keList[i])+','+str(peList[i])+'\n')
                file.write(str(abs((float(xListUTM[i])-diference)))+','+str(yListUTM[i])+','+str(zListUTM[i])+','+str(timeSeconds)+'\n')
            else:
                file.write(str(abs((float(xListUTM[i])-diference)))+','+str(yListUTM[i])+','+str(zListUTM[i])+','+str(timeSeconds)+'\n')
                ##(All the results)
                ##file.write(str(abs((float(xListUTM[i])-diference)))+','+str(yListUTM[i])+','+str(zListUTM[i])+','+str(timeSeconds)+','+str(VxList[i])+','+str(VyList[i])+','+str(VzList[i])+','+str(VtotalList[i])+','+str(AxList[i])+','+str(AyList[i])+','+str(AzList[i])+','+str(AtotalList[i])+','+str(FxList[i])+','+str(FyList[i])+','+str(FzList[i])+','+str(FtotalList[i])+','+str(NetPowList[i])+','+str(wworkXlist[i])+','+str(wworkYlist[i])+','+str(wworkZlist[i])+','+str(wworkTotalList[i])+','+str(wworkList[i])+','+str(keList[i])+','+str(peList[i])+'\n')
        
            
    file.close()        










if __name__ == "__main__":
    guiFrame = GUIFramework()
    guiFrame.mainloop()












    