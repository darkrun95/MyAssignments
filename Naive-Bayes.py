"""
Author : Arun Pottekat
Domain : Data Mining 
Problem : Naive Bayes
"""

# sample.txt
# Consultancy,30,Ph.D,9
# Service,21,MTech,1
# Research,26,MTech,2
# Service,28,BTech,10
# Consultancy,40,MTech,14
# Research,35,Ph.D,10
# Research,27,BTech,6
# Service,32,MTech,9
# Consultancy,45,BTech,17
# Research,36,Ph.D,7

test_age = int(input("Enter age :- "))
test_qualification = input("Enter qualification :- ")
test_experience = int(input("Enter experience :- "))

fh = open("sample.txt", "r")
entry = []
total_entries = 0
for line in fh:
	line=line.split("\n")
	line[0] = line[0].split(",")
	entry.append(line[0])
	total_entries = total_entries + 1

# Training phase
classes = []
class_probability = []

age_probability = [[], [], []]

qualification_class = []
qualification_probability = []
qualification_entries = 0

experience_probability = [[], [], [], []]

for element in entry:
	if element[0] not in classes:
		classes.append(element[0])
		class_probability.append(1)
	else:
		index = classes.index(element[0])
		class_probability[index] = class_probability[index] + 1

	if element[2] not in qualification_class:
		qualification_class.append(element[2])

for x in qualification_class:
	qualification_probability.append([])

qualification_entries = qualification_class.__len__()

for x in classes:
	age_probability[0].append(0)
	age_probability[1].append(0)
	age_probability[2].append(0)

	experience_probability[0].append(0)
	experience_probability[1].append(0)
	experience_probability[2].append(0)
	experience_probability[3].append(0)

	for y in range(0, qualification_entries):
		qualification_probability[y].append(0)

for element in entry:
	index = classes.index(element[0])
	if int(element[1]) > 20 and int(element[1]) <= 30:
		age_probability[0][index] = age_probability[0][index] + 1

	elif int(element[1]) > 30 and int(element[1]) <= 40:
		age_probability[1][index] = age_probability[1][index] + 1
		
	elif int(element[1]) > 40 and int(element[1]) <= 50:
		age_probability[2][index] = age_probability[2][index] + 1

	for var in range(0, qualification_entries):
		if element[2] == qualification_class[var]:
			qualification_probability[var][index] = qualification_probability[var][index] + 1

	if int(element[3]) > 0 and int(element[3]) <= 5:
		experience_probability[0][index] = experience_probability[0][index] + 1

	elif int(element[3]) > 5 and int(element[3]) <= 10:
		experience_probability[1][index] = experience_probability[1][index] + 1
		
	elif int(element[3]) > 10 and int(element[3]) <= 15:
		experience_probability[2][index] = experience_probability[2][index] + 1

	elif int(element[3]) > 15 and int(element[3]) <= 20:
		experience_probability[3][index] = experience_probability[3][index] + 1		


# Testing phase
predictions = []

age_val = []
age_sum = 0
if test_age > 20 and test_age <= 30:
	for x in age_probability[0]:
		age_sum = age_sum + x

	for x in range(0, classes.__len__()):
		age_val.append(float(age_probability[0][x]/age_sum))

elif test_age > 30 and test_age <= 40:
	for x in age_probability[1]:
		age_sum = age_sum + x

	for x in range(0, classes.__len__()):
		age_val.append(float(age_probability[1][x]/age_sum))

elif test_age > 40 and test_age <= 50:
	for x in age_probability[2]:
		age_sum = age_sum + x

	for x in range(0, classes.__len__()):
		age_val.append(float(age_probability[2][x]/age_sum))

qualification_val = []
qualification_sum = 0
for var in range(0, qualification_entries):
	if test_qualification == qualification_class[var]:
		for x in qualification_probability[var]:
			qualification_sum = qualification_sum + x

		for x in range(0, classes.__len__()):
			qualification_val.append(float(qualification_probability[var][x]/qualification_sum))

experience_val = []
experience_sum = 0
if test_experience > 0 and test_experience <= 5:
	for x in experience_probability[0]:
		experience_sum = experience_sum + x

	for x in range(0, classes.__len__()):
		experience_val.append(float(experience_probability[0][x]/experience_sum))

elif test_experience > 5 and test_experience <= 10:
	for x in experience_probability[1]:
		experience_sum = experience_sum + x

	for x in range(0, classes.__len__()):
		experience_val.append(float(experience_probability[1][x]/experience_sum))

elif test_experience > 10 and test_experience <= 15:
	for x in experience_probability[2]:
		experience_sum = experience_sum + x

	for x in range(0, classes.__len__()):
		experience_val.append(float(experience_probability[2][x]/experience_sum))

elif test_experience > 15 and test_experience <= 20:
	for x in experience_probability[2]:
		experience_sum = experience_sum + x

	for x in range(0, classes.__len__()):
		experience_val.append(float(experience_probability[3][x]/experience_sum))

for index in range(0, classes.__len__()):
	predict_val = age_val[index] * experience_val[index] * qualification_val[index] * float(class_probability[index]/total_entries)
	predictions.append(predict_val)

print(predictions)
max_index = predictions.index(max(predictions))
print(classes[max_index])