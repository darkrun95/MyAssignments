#include <iostream>
#include <mpi.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
using namespace std;

class node {
public:
	int data;
	node* left;
	node* right;
};

class Tree {
private:
	node *head;

public:
	Tree();
	int insert_value(int );
	int search(int ,int );
};

Tree :: Tree() {
	head = new node();
}

int Tree :: insert_value(int data) {
	node* new_node = new node();
	new_node->data = data;

	if (head->left == NULL) {
		head->left = new_node;
		return 0;
	}
	else {
		node *temp = head->left;
		while(1) {
			if (data < temp->data) {
				if (temp->left == NULL) {
					temp->left = new_node;
					return 0;
				}
				else {
					temp = temp->left;
				}
			}
			else if (data >= temp->data) {
				if (temp->right == NULL) {
					temp->right = new_node;		
					return 0;
				}
				else {
					temp = temp->right;
				}
			}
		}
	}
}

int Tree :: search(int search_element, int proc_rank) {
	node *temp = head->left;
	int flag = 0;
	while(temp != NULL) {
		if (temp->data == search_element) {
			flag = 1;
			break;
		}
		else if (search_element < temp->data) {
			temp = temp->left;
		}
		else {
			temp = temp->right;
		}
	}
	if (flag != 0) {
		int send_value = proc_rank;
		MPI_Send(&send_value, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
	}
	else {
		int send_value = 0;
		MPI_Send(&send_value, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);	
	}
	return 0;
}

int main(int argc, char const *argv[]) {
	int proc_rank = 0;
	int size = 0;

	MPI_Init(0, 0);

	MPI_Comm_rank(MPI_COMM_WORLD, &proc_rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);

	if (proc_rank != 0) {
		int search_element = 0;
		int counter = 0;

		Tree tree;

		MPI_Bcast(&search_element, 1, MPI_INT, 0, MPI_COMM_WORLD);
		MPI_Bcast(&counter, 1, MPI_INT, 0, MPI_COMM_WORLD);

		int* arr = new int[counter];

		MPI_Recv(arr, counter, MPI_INT, 0, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

		for (int i = 0; i < counter; ++i) {
			tree.insert_value(arr[i]);
		}	
		tree.search(search_element, proc_rank);
	}
	else if (proc_rank == 0) {
		int element_count = 0;
		int search_element = 0;
		cout << "Enter number of elements :- ";
		cin >> element_count; 

		int counter = ceil((float)element_count/(size-1));
		int *arr = new int[element_count];

		srand(time(NULL));
		for (int i = 0; i < element_count; ++i) {
			int temp = rand() % 1000;
			arr[i] = temp;
		}

		int **subarray = new int*[size-1];
		for (int i = 0; i < size-1; ++i) {
			subarray[i] = new int[counter];
		}

		int element_counter = 0;
		int i,j;
		for (i = 0; i < size-2; ++i) {
			for (j = 0; j < counter; ++j) {
				subarray[i][j] = arr[element_counter];
				element_counter = element_counter + 1;
			}
		}
		int element = element_counter;
		for (int k = 0; k < element_count - element_counter; k++) {
			subarray[i][k] = arr[element];
			element = element + 1;
		}

		for (int i = 0; i < size-1; ++i) {
			for (int j = 0; j < counter; ++j) {
				cout << subarray[i][j] << endl;
			}
		}

		cout << "Enter the search element :- ";
		cin >> search_element;

		MPI_Bcast(&search_element, 1, MPI_INT, 0, MPI_COMM_WORLD);
		MPI_Bcast(&counter, 1, MPI_INT, 0, MPI_COMM_WORLD);

		for (int i = 0; i < size-1; ++i) {
			MPI_Send(subarray[i], counter, MPI_INT, i+1, 2, MPI_COMM_WORLD);
		}

		int* recv_val = new int[size-1];
		for (int i = 1; i < size; i++) {
			MPI_Recv(&recv_val[i-1], 1, MPI_INT, MPI_ANY_SOURCE, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);	
		}

		int flag = 0;
		for (int i = 0; i < size-1; ++i) {
			if (recv_val[i] != 0) {
				cout << "Value found by node : " << recv_val[i] << endl;	
				flag = 1;
				break;
			}
		}

		if (flag == 0) {
			cout << "Value not found" << endl;
		}
	}

	MPI_Finalize();
	return 0;
}

