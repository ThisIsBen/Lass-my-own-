#!/usr/bin/python3

import urllib.request
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
import time
from datetime import datetime



#connect with DB (PM25)
database='LASS_RAIN_PROB'
client = InfluxDBClient('localhost', 8086, 'root', 'root', database)
client.create_database(database)


class Rain:
    def __init__(self, time, county, temp, prob):
        self.time = time     # TIME string
        self.county = county # CITY string
        self.temp = temp     # Temperature string
        self.prob = prob     # rain prob string
        pass
    def __str__(self):
        return '{{"time": "{}", "county": "{}", "temp": "{}", "prob": "{}"}}'.format(self.time, self.county, self.temp, self.prob)
    def toJSON(self):
        return self
    def toCSV(self):
        return '{},{},{},{}'.format(self.time, self.county, self.temp, self.prob)

def getRains(link):
    with urllib.request.urlopen(link) as f:
        forecast = f.read().decode('UTF-8')
    rains = []
    soup = BeautifulSoup(forecast, 'html.parser')
    timeStr = soup.findAll('div', {'class': 'modifyedDate'})[0].string
    trs = soup.findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        if not tds:
            continue
        rain = Rain(timeStr, tds[0].a.string, tds[1].a.string, tds[2].a.string)
        rains.append(rain)
    return rains

def main():

    #parse the following 3 webpage every 24 hours
    while True:

        links = ['http://www.cwb.gov.tw/V7/forecast/f_index.htm', 'http://www.cwb.gov.tw/V7/forecast/f_index2.htm', 'http://www.cwb.gov.tw/V7/forecast/f_index3.htm']
        for link in links:
            rains = getRains(link)
            # TODO
            # fill -1 to attrubute if no values
            
            for countyIndex in range(len(rains)):
                print (rains[countyIndex].county)
                print ('Rain Probability:')
                print (rains[countyIndex].prob)   
                print (rains[countyIndex].time)
                if rains[countyIndex].time is None:
                    rains[countyIndex].time = '-1'

                if rains[countyIndex].county is None:
                    rains[countyIndex].county = '-1'

                if rains[countyIndex].temp is None:
                    rains[countyIndex].temp = '-1'

                if rains[countyIndex].prob is None:
                    rains[countyIndex].prob = '-1'

            
            
                json_body = [{
                    "measurement":'rain_prob',
                    #"time": self.jsonData.get('version'),
                    
                    "tags": {
                        "County": rains[countyIndex].county
                    },
                    "fields": {
                        "Timespan":rains[countyIndex].time,
                        "Temperature": rains[countyIndex].temp,
                        "Prob": rains[countyIndex].prob
                       
                    }

                }]
                client.write_points(json_body)
        
        #parse the following 3 webpage every 24 hours   
        time.sleep(86400) 

if __name__ == '__main__':
    main()
    pass

