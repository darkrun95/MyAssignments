class Node(object):
	def __init__(self, jug1, jug2):
		self.jug1 = jug1
		self.jug2 = jug2
		self.child1 = None
		self.child2 = None
		self.child3 = None
		self.child4 = None
		self.child5 = None
		self.child6 = None
		self.child7 = None
		self.child8 = None

jug1_capacity = 0
jug2_capacity = 0

goal_jug_1 = 0
goal_jug_2 = 0

open_list = []
closed_list = []

def generate_children(expand_node):
	global closed_list

	children = []
	if expand_node.jug1 < jug1_capacity:
		first_child = Node(jug1_capacity, expand_node.jug2)
		if [first_child.jug1, first_child.jug2] not in closed_list:
			children.append(first_child)
			expand_node.child1 = first_child
			closed_list.append([first_child.jug1, first_child.jug2])

	if expand_node.jug2 < jug2_capacity:
		second_child = Node(expand_node.jug1, jug2_capacity)
		if [second_child.jug1, second_child.jug2] not in closed_list and second_child not in children:
			children.append(second_child)
			expand_node.child2 = second_child
			closed_list.append([second_child.jug1, second_child.jug2])

	if expand_node.jug1 != 0:
		third_child = Node(0, expand_node.jug2)
		if [third_child.jug1, third_child.jug2] not in closed_list and third_child not in children:
			children.append(third_child)
			expand_node.child3 = third_child
			closed_list.append([third_child.jug1, third_child.jug2])

	if expand_node.jug2 != 0:
		fourth_child = Node(expand_node.jug1, 0)
		if [fourth_child.jug1, fourth_child.jug2] not in closed_list and fourth_child not in children:
			children.append(fourth_child)
			expand_node.child4 = fourth_child
			closed_list.append([fourth_child.jug1, fourth_child.jug2])

	if (expand_node.jug1 + expand_node.jug2 >=jug1_capacity) and expand_node.jug2 > 0:
		fifth_child = Node(jug1_capacity, expand_node.jug1 + expand_node.jug2 - jug1_capacity)
		if [fifth_child.jug1, fifth_child.jug2] not in closed_list and fifth_child not in children:
			children.append(fifth_child)
			expand_node.child5 = fifth_child
			closed_list.append([fifth_child.jug1, fifth_child.jug2])
			
	if (expand_node.jug1 + expand_node.jug2 >=jug2_capacity) and expand_node.jug1 > 0:
		sixth_child = Node(expand_node.jug1 + expand_node.jug2 - jug2_capacity, jug2_capacity)
		if [sixth_child.jug1, sixth_child.jug2] not in closed_list and sixth_child not in children:
			children.append(sixth_child)
			expand_node.child6 = sixth_child
			closed_list.append([sixth_child.jug1, sixth_child.jug2])

	if (expand_node.jug1 + expand_node.jug2 <=jug1_capacity) and expand_node.jug2 > 0:
		seventh_child = Node(expand_node.jug1 + expand_node.jug2, 0)
		if [seventh_child.jug1, seventh_child.jug2] not in closed_list and seventh_child not in children:
			children.append(seventh_child)
			expand_node.child7 = seventh_child
			closed_list.append([seventh_child.jug1, seventh_child.jug2])

	if (expand_node.jug1 + expand_node.jug2 <=jug2_capacity) and expand_node.jug1 > 0:
		eighth_child = Node(expand_node.jug1 + expand_node.jug2, 0)
		if [eighth_child.jug1, eighth_child.jug2] not in closed_list and eighth_child not in children:
			children.append(eighth_child)
			expand_node.child8 = eighth_child	
			closed_list.append([eighth_child.jug1, eighth_child.jug2])

	return children

def dfs_search(start):
	global goal_jug_1
	global goal_jug_2

	path = []
	node_list = []
	flag = False

	node_list.append(start)

	while node_list != []:
		node = node_list.pop()
		path.append([node.jug1, node.jug2])

		if node.jug1 == goal_jug_1 and node.jug2 == goal_jug_2:
			flag = True
			break
		if node.child1 != None:
			node_list.append(node.child1)
		if node.child2 != None:
			node_list.append(node.child2)
		if node.child3 != None:
			node_list.append(node.child3)
		if node.child4 != None:
			node_list.append(node.child4)
		if node.child5 != None:
			node_list.append(node.child5)
		if node.child6 != None:
			node_list.append(node.child6)
		if node.child7 != None:
			node_list.append(node.child7)
		if node.child8 != None:
			node_list.append(node.child8)

	if flag == True:
		print("DFS path - 1 to the goal state is :- ")
		for element in path:
			print(element)
	else:
		print("State cannot be achieved")

	print()

	node_list = []
	path = []
	flag = False

	node_list.append(start)

	while node_list != []:
		node = node_list.pop()
		path.append([node.jug1, node.jug2])

		if node.jug1 == goal_jug_1 and node.jug2 == goal_jug_2:
			flag = True
			break
		if node.child8 != None:
			node_list.append(node.child8)
		if node.child7 != None:
			node_list.append(node.child7)
		if node.child6 != None:
			node_list.append(node.child6)
		if node.child5 != None:
			node_list.append(node.child5)
		if node.child4 != None:
			node_list.append(node.child4)
		if node.child3 != None:
			node_list.append(node.child3)
		if node.child2 != None:
			node_list.append(node.child2)
		if node.child1 != None:
			node_list.append(node.child1)

	if flag == True:
		print("DFS path - 2 to the goal state is :- ")
		for element in path:
			print(element)
	else:
		print("State cannot be achieved")

	return

def bfs_search(start):
	global goal_jug_1
	global goal_jug_2

	path = []
	node_list = []
	flag = False

	node_list.append(start)

	while node_list != []:
		node = node_list.pop(0)
		path.append([node.jug1, node.jug2])

		if node.jug1 == goal_jug_1 and node.jug2 == goal_jug_2:
			flag = True
			break
		if node.child1 != None:
			node_list.append(node.child1)
		if node.child2 != None:
			node_list.append(node.child2)
		if node.child3 != None:
			node_list.append(node.child3)
		if node.child4 != None:
			node_list.append(node.child4)
		if node.child5 != None:
			node_list.append(node.child5)
		if node.child6 != None:
			node_list.append(node.child6)
		if node.child7 != None:
			node_list.append(node.child7)
		if node.child8 != None:
			node_list.append(node.child8)

	if flag == True:
		print("BFS path to the goal state is :- ")
		for element in path:
			print(element)
	else:
		print("State cannot be achieved")

def main():
	global goal_jug_1
	global goal_jug_2

	global jug1_capacity
	global jug2_capacity

	global open_list
	global closed_list
	global total_states

	jug1_capacity = int(input("Enter capacity of jug 1 :- "))
	jug2_capacity = int(input("Enter capacity of jug 2 :- "))	

	print()
	goal_jug_1 = int(input("Enter the goal state of jug 1 :- "))
	goal_jug_2 = int(input("Enter the goal state of jug 2 :- "))

	first_node = Node(0, 0)
	closed_list.append([first_node.jug1, first_node.jug2])
	open_list.append(first_node)

	while open_list.__len__() != 0:
		node = open_list.pop(0)
		children = generate_children(node)
		open_list.extend(children)

	dfs_search(first_node)
	print()
	bfs_search(first_node)

if __name__ == '__main__':
	main()