"""
File Name: credicardchecker.py
Author: Akli Amrous
Description: This file defines a function that implements
Luhn's Algorithm (https://en.wikipedia.org/wiki/Luhn_algorithm)
to check the validity of a credit card number

"""

def isValidCreditCard(ccn):
	if(ccn.isdigit() != True):
		return False
	
	check = 0
	checkl = []
	for i in range(len(ccn) - 1, -1, -1):
		checkl.append(int(ccn[i]))
	
	
	for i in range(1, len(checkl), 2):
		if(checkl[i] * 2 > 9):
			adj = checkl[i] * 2 - 9
			checkl[i] = adj 
			
                
		else:
			checkl[i] = checkl[i] * 2
			
	check = (sum(checkl)) % 10 
	
	if(check == 0):
		return True
	else:
		return False
		





