'''
This file was publicly available through the SANS institute
The author of this file is Rob VandenBrink

This presentation can be downloaded at 
https://isc.sans.edu/presentations/sansfire2012-Rob_Vandenbrink-obd-preso.pdf

The module can be accessed at
https://isc.sans.edu/presentations/sansfire2012-Rob_Vandenbrink-obd-final.zip
'''


def getvin(ser):
     chk = "09 02\r"
     ser.write(chk)
     val = ser.readline()             # dummy line read
     val1 = ser.readline().split(':').split('\r')
     val2 = ser.readline().split(':').split('\r')
     val3 = ser.readline().split(':').split('\r')
     val = val1[1] + " " + val2[1] + " " + val3[1]
     vin1 = val.split(' ').split('\r')
     for digit in range(3,19):
         vin = vin + int('0x'+vin1[digit] , 0)
     return vin

def getfuelsystemstatus(ser):      # retry
    chk = "01 03\r"
    write(chk)
    val = ser.readline().split(' ')
    val = "Not implemented"
    return val

def getengineload(ser):       #done
    chk = "01 04\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    pct = int('0x'+val[3] , 0 )*100/255 
    return pct


def getcoolanttemp(ser):   #done
    chk = "01 05\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    if len(val) > 3:
        degc = int('0x'+val[3] , 0 ) - 40
    else:
        degc = None
    return degc

def getshorttermfueltrim(ser):
    chk1 = "01 06\r"
    chk2 = "01 08\r"
    ser.write(chk1)
    val = ser.readline().split(' ')
    stftbank1pct = (int('0x'+val[3],0)-128) *100/128
    ser.write(chk2)
    val = ser.readline().split(' ')
    stftbank2pct = (int('0x'+val[3],0)-128) *100/128
    return stftbank1pct, stftbank2pct

def getlongtermfueltrim(ser):
    chk1 = "01 07\r"
    chk2 = "01 09\r"
    ser.write(chk1)
    val = ser.readline().split(' ')
    ltftbank1pct = (int('0x'+val[3],0)-128) *100/128
    ser.write(chk2)
    val = ser.readline().split(' ')
    ltftbank2pct = (int('0x'+val[3],0)-128) *100/128
    return ltftbank1pct, ltftbank2pct


def getfuelpressure(ser):            # done
    chk = "01 0A\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    if len(kpa) > 1:
        kpa = int('0x'+val[1] , 0 ) * 3
    else:
        kpa = None
    return kpa


def getintakemanifoldpressure(ser):       # problem - always returns 0xb = 11
    chk = "01 0B\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    if len(kpa) > 1:
        kpa = int('0x'+val[1] , 0 )
    else:
        kpa = None
    return kpa


def getrpm(ser):             # done
    chk = "01 0C\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    try:
		rpm = (int('0x'+val[3]+val[4] , 0 ) - 40) / 4      # check in low rpm situation
    except:
		rpm = 100
    return rpm
 
def getspeed(ser):         # done
    chk = "01 0D\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    kph = int('0x'+val[3] , 0 )

    return kph
 
def gettimingadvance(ser):     # done
    chk = "01 0E\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    if len(val) > 2:
        degrees = ( int('0x'+val[3] , 0 ) / 2) - 64
    else:
        degrees = None
    return degrees

def getintaketemp(ser):       # done
    chk = "01 0f\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    degc = int('0x'+val[3] , 0 ) - 40
    return degc

def getMAFrate(ser):              # done
    chk = "01 10\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    gramspersec = int('0x'+val[3]+ val[4] , 0 ) /100
    return gramspersec

def getOBDStandard(ser):              # done
    std = [ "",  "OBD-II as defined by the CARB", "OBD as defined by the EPA" , \
    "OBD and OBD-II", "OBD-I" , "Not meant to comply with any OBD standard", \
    "EOBD (Europe)" , "EOBD and OBD-II", "EOBD and OBD", "EOBD, OBD and OBD II" ,\
    "JOBD (Japan)", "JOBD and OBD II", "JOBD and EOBD", "JOBD EOBD and OBD II" ]
    chk = "01 1C\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    standard = std[ int('0x'+val[3],0) ]
    return standard


def getruntime(ser):             #done 
    chk = "01 1F\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    seconds = int('0x'+val[3],+ val[4] , 0 )
    return seconds

def getbarometricpressure(ser):        # done
    chk = "01 33\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    kPa = int('0x'+val[3] , 0 )
    return kPa

def getambienttemp(ser):              # done
    chk = "01 46\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    degc = int('0x'+val[3] , 0 ) - 40
    return degc

def getfueltype(ser):           # problem - returns 01 51
    fuel = [ "", "Gasoline" , "Methanol" , "Ethanol" , "Diesel" , "LPG" , "CNG" ,\
    "Propane" , "Electric" ,  "Bifuel running Gasoline" , "Bifuel running Methanol" ,\
    "Bifuel running Ethanol" , "Bifuel running LPG" , "Bifuel running CNG" , \
    "Bifuel running Propane" , "Bifuel running Electricity" , "Bifuel mixed gas/electric", \
    "Hybrid gasoline" , "Hybrid Ethanol" , "Hybrid Diesel" , "Hybrid Electric" , \
    "Hybrid Mixed fuel" , "Hybrid Regenerative" ]
    chk = "01 51\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    return fuel[ int('0x'+val[3]), 0 ]
    
def getethanolpercent(ser):     # problem - returns 01 52
    chk = " 01 52\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    percent = int('0x'+val[3] , 0 ) *100/255
    return percent

def getoiltemp(ser):           # problem - returns 01 5c
    chk = "41 5C\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    degc = int('0x'+val[2] , 0 ) - 40
    return degc

def fordgetoiltemp(ser):
    chk="221310\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    degc = (int('0x'+val[1] + val[2] , 0 )/100 ) - 40
    return degc

def getfuelrate(ser):           # problem - returns 01 5e
    chk = "01 5E\r"
    ser.write(chk)
    val = ser.readline().split(' ')
    Lperhr = int('0x'+val[2]+val[3] , 0 ) *0.05
    return Lperhr
