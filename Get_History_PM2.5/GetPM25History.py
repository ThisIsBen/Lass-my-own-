import sys
import re
import os
import json
import time

from influxdb import InfluxDBClient
connectDB='PM25'
client = InfluxDBClient('localhost', 8086, 'root', 'root', connectDB) 
client.create_database(connectDB) 





#open a file for each airbox and write each data of the airbox to that file
storeLoc='/var/www/html/LASS/data/csv'
if not os.path.exists(storeLoc):
    os.makedirs(storeLoc)



    



#get a list of PM2.5 if PM2.5 
def getIDList(arg_measurement,IDList):
    if arg_measurement=='airbox' or arg_measurement=='lass':
        PM25Query = client.query(' select "PM2.5" from ' + arg_measurement + ' where time > now() - 1h  group by "Device_id" order by time DESC limit 1;')    

        #extract ID from query replies
        IDSet = " "
        
        IDSet = " ".join(re.findall("\{u'Device_id': u'(.*?)'\}", str(PM25Query)))


        temp=IDSet.split(' ')
        for i in range(len(temp)):
            IDList.append(temp[i])


        





    else:
        print('Invalid Measurement.')
       

#to count how many airbox device don't have the requested data





#get PM2.5 latest data
def getPM25List(arg_measurement,IDList,PM25List):

    MeanDict={}
    for i in range(len(IDList)):

       MeanQuery = client.query(' select Mean("PM2.5") from ' + arg_measurement + ' WHERE "Device_id"='+'\''+IDList[i]+'\''+' and time > now()- 1w group by time(1d)')    
       
       PM25Set = " ".join(re.findall("u'mean':(.*?),", str(MeanQuery)))
       timeSet = " ".join(re.findall("u'time': u'(.*?)'", str(MeanQuery)))


       timetemp=timeSet.split(' ')

       PM25Set=PM25Set.strip()
       PM25temp=PM25Set.split('  ')

      
       MeanDict['day1']=timetemp[0]
       MeanDict['day1_mean']=PM25temp[0]
       MeanDict['day2']=timetemp[1]
       MeanDict['day2_mean']=PM25temp[1]
       MeanDict['day3']=timetemp[2]
       MeanDict['day3_mean']=PM25temp[2]
       MeanDict['day4']=timetemp[3]
       MeanDict['day4_mean']=PM25temp[3]
       MeanDict['day5']=timetemp[4]
       MeanDict['day5_mean']=PM25temp[4]
       MeanDict['day6']=timetemp[5]
       MeanDict['day6_mean']=PM25temp[5]
       MeanDict['day7']=timetemp[6]
       MeanDict['day7_mean']=PM25temp[6]
       MeanDict['today']=timetemp[7]
       MeanDict['today_mean']=PM25temp[7]

       #get total mean
       PM25MeanSum=0
       numOfNonNone=0
       for k in range(len(PM25temp)):
       	 
       	 if PM25temp[k] != 'None':
       	 	numOfNonNone+=1
       	 	PM25MeanSum+=float(PM25temp[k])
       MeanDict['total_mean']=round(PM25MeanSum/numOfNonNone)

      
       #append dict to an accumulation list
       PM25List.append(dict(MeanDict))

       #print (PM25List)



       
       #clear the dict
       #MeanDict.clear()
       #print (PM25List)


       
    #





#write the latest PM2.5 ,ID and time to csv file
def write2file(arg_measurement,IDList,PM25List):
    
    
    # print(allposition)

    if(len(IDList)!=0):

        fp = open(storeLoc+"/"+arg_measurement+"History.csv", "w+")

        fp.write( 'ID,day1,day1_mean,......day7,day7_mean,total_mean\n')
  
        for IDindex in range(len(IDList)):

            

            # fp.write( str(IDList[IDindex])+","+str(PM25List[IDindex])+","+timeList[IDindex]+"\n");
  

            fp.write( str(IDList[IDindex])+","+str(PM25List[IDindex]['day1'])+","+str(PM25List[IDindex]['day1_mean'])+","+str(PM25List[IDindex]['day2'])+","+str(PM25List[IDindex]['day2_mean'])+","+str(PM25List[IDindex]['day3'])+","+str(PM25List[IDindex]['day3_mean'])+","+str(PM25List[IDindex]['day4'])+","+str(PM25List[IDindex]['day4_mean'])+","+str(PM25List[IDindex]['day5'])+","+str(PM25List[IDindex]['day5_mean'])+","+str(PM25List[IDindex]['day6'])+","+str(PM25List[IDindex]['day6_mean'])+","+str(PM25List[IDindex]['day7'])+","+str(PM25List[IDindex]['day7_mean'])+","+str(PM25List[IDindex]['today'])+","+str(PM25List[IDindex]['today_mean'])+","+str(PM25List[IDindex]['total_mean'])+"\n");

        fp.close()







def main():

        #read in target measurement
        arg_measurementList = ['airbox','lass']
         #get a list of distinct ID
        IDList=[]
        
        PM25List=[]

        #get latest PM2.5 data and store it in CSV files from DB every 5 mins
        while(True):
            
            # re generate all position for lass, airbox
            #os.system('python region_graph.py')
            
            
            for mIndex in range(len(arg_measurementList)):
                #get all IDs in this measurement
                getIDList(arg_measurementList[mIndex],IDList)
                #Get PM2.5 list
                getPM25List(arg_measurementList[mIndex],IDList,PM25List)
                #Get time list
                #getTimeList(PM25Query,timeList)
              
                #write latest PM2.5 data to csv file
                write2file(arg_measurementList[mIndex],IDList,PM25List)
                #print PM25List[0]
                #print PM25List[0]['day1_mean']


                print('Measurement: ',arg_measurementList[mIndex])
                print('Total responsive AirBox num(which has data in the past one hour): ',len(IDList))

                #clear Lists before containing data from other measurement
                del IDList[:]
                
                del PM25List[:]
            #get latest PM2.5 data from DB every 24 hrs
            time.sleep(86400)
                
        
        
        
if __name__ == '__main__':
            main()

