"""
Parallel implementation of booth's multiplier using mpi4py 
"""

from mpi4py import MPI
import numpy as np

rank = MPI.COMM_WORLD.Get_rank()

def booth_multiply(data):
	data_size = len(data[0])
	if data_size == 2:
		a1b2 = format(int(data[0][0]) * int(data[1][1]), "02b")
		a1b1 = format(int(data[0][0]) * int(data[1][0]), "02b")
		a2b2 = format(int(data[0][1]) * int(data[1][1]), "02b")
		a2b1 = format(int(data[0][1]) * int(data[1][0]), "02b")

		carry = 0
		b2a2b1 = int(a1b2[1]) + int(a2b1[1]) + int(a2b2[0])
		if b2a2b1 == 2:
			b2a2b1 = 0
			carry = 1
		elif b2a2b1 == 3:
			b2a2b1 = 1
			carry = 1

		a1b1a2 = int(a1b2[0]) + int(a2b1[0]) + int(a1b1[1])
		if a1b1a2 == 2:
			a1b1a2 = 0
			carry = 1
		elif a1b1a2 == 3:
			a1b1a2 = 1
			carry = 1

		a1 = int(a1b1[0]) + carry
		if a1 == 2:
			a1 = 0

		binary_string = str(a1) + str(a1b1a2) + str(b2a2b1) + a2b2[1]
		return binary_string
	else:	
		data = np.array(data).reshape(4, int((len(data[0])+len(data[1]))/4))
		binary_string_a1b2 = booth_multiply([data[0], data[3]])
		binary_string_a1b1 = booth_multiply([data[0], data[2]])
		binary_string_a2b2 = booth_multiply([data[1], data[3]])	
		binary_string_a2b1 = booth_multiply([data[1], data[2]])

		data_size = len(binary_string_a1b2)
		prefix_postfix_length = data_size / 2
		final_string = binary_string_a2b2[prefix_postfix_length:]

		carry = 0
		for length in range(data_size-1, -1, -1):
			middle_value = binary_string_a1b1[prefix_postfix_length:] + binary_string_a2b2[:prefix_postfix_length]
			value = int(binary_string_a1b2[length]) + int(binary_string_a2b1[length]) + carry + int(middle_value[length])
			if value == 1 or value == 0:
				carry = 0
			if value == 2:
				value = 0
				carry = 1
			elif value == 3:
				value = 1
				carry = 1
			final_string = str(value) + final_string

		if carry == 1:
			for length in range(len(binary_string_a1b1[:prefix_postfix_length])-1, -1, -1):
				value = int(binary_string_a1b2[length]) + carry
				if value == 2:
					carry = 1
					value = 0
				else:
					carry = 0
				final_string = str(value) + final_string
		else:
			final_string = binary_string_a1b1[:prefix_postfix_length] + final_string
		return final_string

if rank == 0:
	numbers = [2, 8]
	binary_numbers = []
	for num in numbers:
		num = format(num, "016b")
		binary_numbers.extend(np.array(list(num)).reshape(2, 8))

	MPI.COMM_WORLD.send([binary_numbers[0], binary_numbers[3]], dest=1, tag=1)
	MPI.COMM_WORLD.send([binary_numbers[0], binary_numbers[2]], dest=2, tag=2)
	MPI.COMM_WORLD.send([binary_numbers[1], binary_numbers[3]], dest=3, tag=3)
	MPI.COMM_WORLD.send([binary_numbers[1], binary_numbers[2]], dest=4, tag=4)

	binary_values = MPI.COMM_WORLD.gather(None, root=0)
	binary_values.pop(0)

	binary_string_a1b2 = binary_values[0]
	binary_string_a1b1 = binary_values[1]
	binary_string_a2b2 = binary_values[2]
	binary_string_a2b1 = binary_values[3]

	data_size = len(binary_string_a1b2)
	prefix_postfix_length = data_size / 2
	final_string = binary_string_a2b2[prefix_postfix_length:]

	carry = 0
	for length in range(data_size-1, -1, -1):
		middle_value = binary_string_a1b1[prefix_postfix_length:] + binary_string_a2b2[:prefix_postfix_length]
		value = int(binary_string_a1b2[length]) + int(binary_string_a2b1[length]) + carry + int(middle_value[length])
		if value == 1 or value == 0:
			carry = 0
		if value == 2:
			value = 0
			carry = 1
		elif value == 3:
			value = 1
			carry = 1
		final_string = str(value) + final_string

	if carry == 1:
		for length in range(len(binary_string_a1b1[:prefix_postfix_length])-1, -1, -1):
			value = int(binary_string_a1b2[length]) + carry
			if value == 2:
				carry = 1
				value = 0
			else:
				carry = 0
			final_string = str(value) + final_string
	else:
		final_string = binary_string_a1b1[:prefix_postfix_length] + final_string
	print final_string

else:
	data = MPI.COMM_WORLD.recv(source=0, tag=rank)
	binary_string = booth_multiply(data)
	MPI.COMM_WORLD.gather(binary_string, root=0)

"""
OUTPUT :- 
mpiuser@mpiuser:~/Desktop/MyAssignments$ mpiexec -n 5 python booths_multiplier.py 
00000000000000000000000000010000
mpiuser@mpiuser:~/Desktop/MyAssignments$
"""