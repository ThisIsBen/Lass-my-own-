'''
* The program will query data in the DB, output a graph with nodes and links.
* Output JSON file?

* Nodes has different types(lass/airbox/factory)
'''
class Node(object):
    def __init__(self, id, type, lat, lon):
        super(Node, self).__init__()
        self.id = id
        self.type = type
        self.lat = lat
        self.lon = lon
    def hello(self):
        print("I'm "+ self.id+" Lat="+str(self.lat)+" and Lon="+str(self.lon))

# fuction to collect all Gps data in DB
import re
def collectAllGps(Gpslist, kind, IDList):
    # kind is lass/airbox
    # connect to DB(PM25)
    from influxdb import InfluxDBClient
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'PM25') 
    #client.create_database('AirBox_test')
    # query
    GPSQuery = client.query('select "Gps_lon" ,"Gps_lat" from ' + kind + ' group by "Device_id" limit 1;')
    print(GPSQuery)
    GPSQuery = str(GPSQuery)
    print(type(GPSQuery))

    
    IDs = list(re.findall("Device_id': u'(.*?)'", GPSQuery))

    LonList = re.findall("Gps_lon': (-*[0-9]*\.*[0-9]*)", GPSQuery)

    LatList = re.findall("Gps_lat': (-*[0-9]*\.*[0-9]*)", GPSQuery)

    for i in range(len(IDs)):
        IDList.append(IDs[i])
        Gpslist.append((float(LonList[i]), float(LatList[i])))


def main():
    Allnodes = []                      # a list store all nodes
    # 1. read factory files and construre a graph
    type = "factory"
    f = open("data.csv", 'r')
    lines = f.readlines()
    print(len(lines))
    # Get all factories
    # use "factoryXXX" as id
    for i in range(1, len(lines)):
        segment = lines[i].split(",")
        id = "factory" + segment[0]
        lat = float(segment[1])
        lon = float(segment[2])
        #print([id, type, lat, lon])
        
        node = Node(id, type, lat, lon)
        #node.hello()
        Allnodes.append(node)
        # testing
        #p1 = (120.734, 24.12)
        #p2 = (121.535, 25.023)
        #print(compute_dis(p1[0],p1[1],p2[0],p2[1]))
    

    # 2. query to get gps, id list(lass)
    type = "lass"
    LassGpsList = []
    LassIDList = []
    collectAllGps(LassGpsList, type, LassIDList)

    # build graph
    for i in range(len(LassIDList)):
        node = Node(LassIDList[i], type, LassGpsList[i][1], LassGpsList[i][0])
        Allnodes.append(node)

    # 3. query to get gps, id list(airbox)
    type = "airbox"
    AirboxGpsList = []
    AirboxIDList = []
    collectAllGps(AirboxGpsList, type, AirboxIDList)
    
    # build graph
    for i in range(len(AirboxIDList)):
        node = Node(AirboxIDList[i], type, AirboxGpsList[i][1], AirboxGpsList[i][0])
        Allnodes.append(node)
    
    for n in Allnodes:
        n.hello()
    print(len(Allnodes))

    # write Allnodes data to json file- id:{type:xxx, lon:xx, lat:xx}
    fn = "gpsfile"
    node2file(fn, Allnodes)


# fuction: compute distance given lon, lat
from math import radians, cos, sin, asin, sqrt
def compute_dis(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371    # earth radius
    return c * r * 1000         # The units is "meter"


import json
# json file- id:{type:xxx, lon:xx, lat:xx}
def node2file(fn, Allnodes):
    print("writing...")
    dict = {}
    sites = []
    
    for n in Allnodes:
        data = {"id":n.id, "lat":n.lat, "lon":n.lon, "type":n.type}
        sites.append(data)
    dict["sites"] = sites


    print(dict)
    print(len(dict))
    with open(fn, 'w') as fp:
        json.dump(dict, fp)
if __name__ == '__main__':
    main()
