""" ASIT
	Desc:	Lab 1 - Python 
	Devs: 	Bruno Figueiredo
""" 


import sys
import os 

dif_list = []
n_dif = 0;

counter = {}



def average_input():
	received_buf = input("Insert two numbers: ").split()

	while len(received_buf) < 1:
		received_buf = input("Insert two numbers: ").split()		

	a = float(received_buf[0])	
	if len(received_buf) < 2: 
		b = float(input("Insert 2nd number: "))
	else: 
		b = float(received_buf[1])

	return ((a + b) / 2.0)
	

def average_20():
	sum = 0
	n = 1
	
	while n <= 20:
		
		received = float(input("Insert a number (%i): " %n))
		
		if received >= 0:
			sum += received
			n += 1
		else: 
			pass	

	return sum/n

def count_new(line):
	global n_dif
	flag = False
	
	if (dif_list):
			for new in dif_list:
				if new == line:
					flag = True
					break
					
			
			if not flag :
				dif_list.append(line)
				n_dif += 1

	else:
		dif_list.append(line)
		n_dif += 1


def read_file(filename):
	
	list = []
	flag = False

	fp = open(str(filename), 'r')
	line = fp.readline()

	while line :

		print(line)
		list.append(int(line))

		if int(line) in counter: 
			counter[int(line)] +=1
		else:
			counter[int(line)] =1	
			
		line = fp.readline()
		count_new(line)

		

	fp.close()

	print("Different numbers: ", n_dif)
	print(list, counter)
	return True



		
def main():

	#print( "average_input() returned",average_input(),"\n")
	#print( "average_20() returned",average_20(),"\n")
	print( "read_file() returned", read_file("num_test.txt"),"\n")



if __name__ == "__main__":
    main();		
