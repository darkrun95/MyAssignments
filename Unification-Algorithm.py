"""
Author : Arun Pottekat
Domain : Artificial Intelligence
Problem : Unification Algorithm
"""

constants_list = ["1", "2", "3", "4"]

num_predicates = int(input("Enter the number of predicates :- "))
predicates = []
for i in range(0, num_predicates):
	predicates.append(list(input("Enter predicate " +  str(i+1) + " :- ")))

def unify(l1, l2):
	if l1 == l2:
		return "NIL"
	elif l1 not in constants_list:
		if l1 in l2:
			return "FAIL"
		else:
			return "("+l2+"/"+l1+")"
	elif l2 not in constants_list:
		if l2 in l1:
			return "FAIL"
		else:
			return "("+l1+"/"+l2+")"
	else:
		return "FAIL"			

flag = 0
for i in range(0, predicates.__len__() - 1):
	for j in range(i+1, predicates.__len__()):
		if predicates[i][0] != predicates[j][0]:
			flag = 1
			break

	if flag == 1:
		print("FAIL")
		exit()


parameter_count = predicates[0].count(",") + 1
for i in range(1, predicates.__len__()):
	parameter_count_temp = predicates[i].count(",") + 1
	if parameter_count_temp == parameter_count:
		parameter_count = parameter_count_temp
	else:
		print("FAIL")
		exit()

for i in range(0, predicates.__len__() - 1):
	SUBST = []
	parameter_1 = []
	parameter_2 = []
	for j in range(predicates[i].index("(") + 1, predicates[i].index(")"), 2):
		parameter_1.append(predicates[i][j])
	for j in range(predicates[i+1].index("(") + 1, predicates[i+1].index(")"), 2):
		parameter_2.append(predicates[i+1][j])

	for i in range(0, parameter_1.__len__()):
		result = unify(parameter_1[i], parameter_2[i])
		if result == "FAIL":
			print("FAIL")
			exit()
		if result != "NIL":
			list_result = list(result)
			first = list_result[1]
			second = list_result[3]
			if first in parameter_1:
				index = parameter_1.index(first)
				parameter_1.pop(index)
				parameter_1.insert(index, second)

			if first in parameter_2:
				index = parameter_2.index(first)
				parameter_2.pop(index)
				parameter_2.insert(index, second)
			SUBST.append(result)

	print(SUBST)