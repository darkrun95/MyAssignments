import math
fh = open("sample.txt", "r")
entry = []
total_entries = 0
for line in fh:
	entry.append(line.strip().split(" "))

cluster = []
cluster_count = 4
initial_centroid = []
new_centroid = []

# Initialize cluster centroid
counter = 0
for val in range(cluster_count):
	initial_centroid.append(entry[val+counter])
	counter = counter + int(entry.__len__()/4)

def kmeans_clustering():
	global cluster
	cluster = []
	for val in range(cluster_count):
		cluster.append([])

	for element in entry:
		euclidian_distance = []
		min_index = 0
		for index in range(0,cluster_count):
			euclidian_sum = 0
			for val in range(0,4):
				euclidian_sum = euclidian_sum + (int(float(element[val])-float(initial_centroid[index][val]))**2)
			euclidian_distance.append(math.sqrt(euclidian_sum))
		min_index = euclidian_distance.index(min(euclidian_distance))
		cluster[min_index].append(element)

def calc_new_centroid():
	global initial_centroid
	global new_centroid

	for cluster_val in cluster:
		sum_tuple = [0, 0, 0, 0]
		mean_tuple = [0, 0, 0, 0]
		for element in cluster_val:
			for val in range(0, sum_tuple.__len__()):
				sum_tuple[val] = sum_tuple[val] + float(element[val])

		for val in range(0, mean_tuple.__len__()):
			mean_tuple[val] = str(int(sum_tuple[val]/cluster_val.__len__()))

		new_centroid.append(mean_tuple)

def main():
	global initial_centroid
	global new_centroid
	global cluster

	kmeans_clustering()
	calc_new_centroid()

	while True:
		if initial_centroid == new_centroid:
			for val in range(0, cluster.__len__()):
				print("Cluster",val+1)
				for entity in cluster[val]:
					print(entity)
				print()
			break
		else:
			initial_centroid = new_centroid
			new_centroid = []
			kmeans_clustering()
			calc_new_centroid()

if __name__ == '__main__':
	main()

# sample.txt
# 74 180 22 80
# 74 215 34 115
# 72 210 30 110
# 72 210 35 110
# 73 188 35 88
# 69 176 29 76
# 69 209 30 109
# 71 200 35 100
# 76 231 30 131
# 71 180 27 80
# 73 188 23 88
# 73 180 26 80
# 74 185 23 85
# 74 160 26 60
# 69 180 27 80
# 70 185 34 85
# 72 197 30 97
# 73 189 27 89
# 75 185 22 85
# 78 219 22 119
# 79 230 25 130
# 76 205 36 105
# 74 230 31 130
# 76 195 32 95
# 72 180 31 80
# 71 192 29 92
# 75 225 29 125
# 77 203 32 103
# 74 195 35 95
# 73 182 25 82
# 74 188 26 88
# 78 200 24 100
# 73 180 26 80
# 75 200 25 100
# 73 200 27 100
# 75 245 30 145
# 75 240 31 140
# 74 215 30 115
# 69 185 32 85
# 71 175 27 75