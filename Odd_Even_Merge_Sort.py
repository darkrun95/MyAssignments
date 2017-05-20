"""
Author : Arun Pottekat
Domain : High Performance Computing
Problem : Odd Even Merge Sort
"""

from mpi4py import MPI
import random
import numpy as np

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

if rank == 0:
	numbers = random.sample(xrange(0,8), 8)
	numbers = np.array(numbers).reshape(size-1, (8/(size-1)))
	
	for x in xrange(1, size):
		MPI.COMM_WORLD.send(numbers[x-1], dest=x, tag=x)

	numbers = MPI.COMM_WORLD.recv(source=1, tag=1)
	for x in xrange(2, size):
		data = MPI.COMM_WORLD.recv(source=x, tag=x)
		numbers = np.concatenate((numbers, data))

		even_numbers = numbers[::2]
		odd_numbers = numbers[1::2]

		even_numbers = np.sort(even_numbers)
		MPI.COMM_WORLD.send(odd_numbers, dest=x, tag=x)
		odd_numbers = MPI.COMM_WORLD.recv(source=x, tag=x)

		numbers = []
		for y in zip(even_numbers, odd_numbers):
			numbers.append(y[0])
			numbers.append(y[1])

		numbers = np.array(numbers)
		for z in xrange(1, len(numbers)-2, 2):
			if numbers[z] > numbers[z+1]:
				numbers[z], numbers[z+1] = numbers[z+1], numbers[z]

	print "Sorted Numbers : ", numbers
	MPI.COMM_WORLD.Abort()

elif rank == 1:
	numbers = MPI.COMM_WORLD.recv(source=0, tag=1)
	
	# Write sorting module
	numbers = np.sort(numbers)
	MPI.COMM_WORLD.send(numbers, dest=0, tag=1)
else:
	numbers = MPI.COMM_WORLD.recv(source=0, tag=rank)

	numbers = np.sort(numbers)
	MPI.COMM_WORLD.send(numbers, dest=0, tag=rank)
	numbers = MPI.COMM_WORLD.recv(source=0, tag=rank)

	numbers = np.sort(numbers)
	MPI.COMM_WORLD.send(numbers, dest=0, tag=rank)