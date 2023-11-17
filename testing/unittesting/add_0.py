#add_0.py

"""This module defines add functions that are to be used to learn unittesting and mocking."""

def add_independent(num1, num2):
	sum = num1 + num2
	return sum

def get_sum(num1, num2):
		print("I was called")
		return num1 + num2
		
def add_dependent(num1, num2):
	sum = get_sum(num1, num2) 
	return sum


if __name__ == "__main__":
	num1 = 8
	num2 = 2
	result = add_independent(num1, num2)
	print("add_independent: ", result)
	result = add_dependent(num1, num2)
	print("add_dependent: ", result)
	
	