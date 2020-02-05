import datetime
import time
import re
import mysql.connector
from pysnmp.entity.rfc3413.oneliner import cmdgen

#List of IP addresses to monitor
ip= 'address1'
ip2='address2'
ip3='address3'
ip4='address4'
ip5='address5'
ip6='address6'
ip7='address7'

UPSip='upsadd1' 
UPSip2='upsadd2' 
UPSip3='upsadd3' 

 
community=''             #community strings
ecommunity=''
value=(1,3,6,1,4,1,9,9,13,1,3,1,3)   #OIDs
evalue=(1,3,6,1,4,1,534,1,6,5,0)

while True: #loop
    times = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    #mysql connection
    mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='',
                auth_plugin='mysql_native_password'
                )
    #mydb = mysql.connector.connect(
    #            host='',
    #            user='grafanaReader',
    #            password='',
    #            database='',
    #            auth_plugin='mysql_native_password'
    #            )
    mycursor = mydb.cursor()
            
    #function for sql statements
    def connection(daValue,loca):
        sql = 'INSERT INTO thelist(RoomTemp, Timestamp, Location) VALUES (%s , %s, %s);'
        val = [daValue, times, loca]
        mycursor.execute(sql,val,loca)
        mydb.commit()
        #print(mycursor.rowcount, "was inserted.")
    
    
    
    #main
    def temperatureCrud(ipAddress, loc):
        generator = cmdgen.CommandGenerator()
        comm_data = cmdgen.CommunityData('server', community, 1) # 1 means version SNMP v2c
        transport = cmdgen.UdpTransportTarget((ipAddress, 161))
           
        real_fun = getattr(generator, 'nextCmd') #snmp walking
        res = (errorIndication, errorStatus, errorIndex, varBinds)\
            = real_fun(comm_data, transport, value)
                
        
        if not errorIndication is None  or errorStatus is True:
            print("Error: %s %s %s %s" % res)
        else:
            #print("%s" % varBinds)
            #befAvg = 0
            #afAvg = 0
            counter = 0
            goof = 0
            for varBind in varBinds:  # SNMP response contents
                #print(' = '.join([x.prettyPrint() for x in varBind]))
                text = str(varBind)
                allTemps = re.findall(r'\d+', text)
                results = list(map(int, allTemps))
                if 60011 in results:
                    goof += results[-1]
                    counter+=1
                    val = str(goof)
                    value2 = val[-2:]
                    temp2 = float(value2)
                    temperature2 = ((temp2 * 1.8)+32)
                    connection(temperature2, loc)
                    break
                    #print(value)
                    #print(counter)
                if 160171 in results:
                    goof += results[-1]
                    counter+=1
                    val = str(goof)
                    value2 = val[-2:]
                    temp2 = float(value2)
                    temperature2 = ((temp2 * 1.8)+32)
                    connection(temperature2, loc)
                    break
                    #print(value)
                if 93 in results:
                    goof += results[-1]
                    counter+=1
                    val = str(goof)
                    value2 = val[-2:]
                    temp2 = float(value2)
                    temperature2 = ((temp2 * 1.8)+32)
                    connection(temperature2, loc)
                    break
                    #print(value)
                    
        #print(goof)
                #print(str(results[-1]))
                #value = text[-2:]
                #temp = float(value)
                #temperature = ((temp * 1.8)+32)
    #afAvg = befAvg/counter
    #print(afAvg)
    
    a=0
    ipAddress = 'ipx'
    #looping through list of IP addresses
    while a<7:
        
        if a == 0:
            ipAddress = ip
            loc = 'LU-Core-6500-VSS'
            #print(ipAddress)
            temperatureCrud(ipAddress, loc)
            a+=1
        elif a==1:
            ipAddress = ip2
            loc = 'LU-LVR-6506'
            #print(ipAddress)
            temperatureCrud(ipAddress, loc)
            a+=1
        elif a==2:
            ipAddress = ip3
            loc = 'Life6506-CHOP'
            #print(ipAddress)
            temperatureCrud(ipAddress, loc)
            a+=1
        elif a==3:
            ipAddress = ip4
            loc = 'Life6506-SHS'
            #print(ipAddress)
            temperatureCrud(ipAddress, loc)
            a+=1
        elif a==4:
            ipAddress = ip5
            loc = 'LU-AnnexA-6506'
            #print(ipAddress)
            temperatureCrud(ipAddress, loc)
            a+=1
        elif a==5:
            ipAddress = ip6
            loc = 'LU-AnnexB-6506'
            #print(ipAddress)
            temperatureCrud(ipAddress, loc)
            a+=1
        elif a==6:
            ipAddress = ip7
            loc = 'LU-AnnexC-6506'
            #print(ipAddress)
            temperatureCrud(ipAddress, loc)
            a+=1
        
    #                       print('loopdon')
    time.sleep(30)