from region_graph import Node, compute_dis
import sys
import json

# load file and split into 2 partition-(near factory or far from factory)
with open('gpsfile') as data_file:    
    data = json.load(data_file)

list = data["sites"]
print(len(list))

# print(data["sites"])
# print(len(data["sites"]))

# parameters
near = []
far = []
distance = float(sys.argv[1]) 		# meter

output = {"near"+str(distance):{}}

count = 0
# check each node
for k in list:
	if k["type"] == "factory":
	
		# # check each airbox/lass
		# for measure in list:
		# 	if measure["type"] == "airbox" or measure["type"] == "lass":
		# 		count += 1
		# 		if measure["id"] not in near:
		# 			# compute distance
		# 			if compute_dis(k["lon"], k["lat"], measure["lon"], measure["lat"])<distance:
		# 				near.append(measure["id"])

		
		output["near"+str(distance)][k['id']] = []
		for measure in list:
			if measure["type"] == "airbox" or measure["type"] == "lass":
				count += 1
				# compute distance
				if compute_dis(k["lon"], k["lat"], measure["lon"], measure["lat"])<distance:
					output["near"+str(distance)][k['id']].append(measure["id"])
# print(count)
# print(near)

print(output)
with open("near"+str(distance)+".json", 'w') as fp:
    json.dump(output, fp)