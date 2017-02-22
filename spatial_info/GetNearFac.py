import sys
import re
import os
from glob import glob
from subprocess import call
import time
import json
import shutil


if not os.path.exists("./NearFacID"):
    os.makedirs("./NearFacID") 

if os.path.exists("./NearFacID"):
    shutil.rmtree('./NearFacID')  
    os.makedirs("./NearFacID")

    
fileList=[]
IDSrcDir=['/home/ikdd/Ben/myOwn/PM2.5_csv/airbox/','/home/ikdd/Ben/myOwn/PM2.5_csv/lass/']
nearFacDstDir='/home/ikdd/Ben/myOwn/spatial_info/NearFacID'

def binarySearch(alist, item,DirIndex): 
     if len(alist) == 0: 
         return False 
     else: 
        midpoint = len(alist)//2 
        if alist[midpoint]==item:
        #move the file to output file if located
           call(["cp",IDSrcDir[DirIndex]+item+'.csv',nearFacDstDir])        
           return True 
        else: 
           if item<alist[midpoint]: 
             return binarySearch(alist[:midpoint],item,DirIndex) 
           else: 
             return binarySearch(alist[midpoint+1:],item,DirIndex) 
 
def getFilesInDir(DirIndex):
        files = glob(os.path.join(IDSrcDir[DirIndex], '*.csv'))
        for a_file in sorted(files):
                tempfile = " ".join(re.findall(IDSrcDir[DirIndex]+'(.*?).csv', str(a_file)))
                fileList.append(tempfile)



def main():

    SrcJsonFile=sys.argv[1]
    TargetFac=sys.argv[2]


    with open(SrcJsonFile) as json_data:
            nearFacContentd = json.load(json_data)

    #get rid of ".json" in the SrcJsonFile name        
    SrcJsonFile= " ".join(re.findall('(.*?).json', SrcJsonFile))
               


    #check airbox,lass folder
    for DirIndex in range(2):
        getFilesInDir(DirIndex)
        
       

        for nearFacID in nearFacContentd[SrcJsonFile][TargetFac]:
           print nearFacID
           print('Found',binarySearch(fileList, str(nearFacID),DirIndex)) 
        
        #print(binarySearch(fileList, 13)) 
        
if __name__ == '__main__':
        main()

