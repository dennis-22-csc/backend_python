#add_9.py
import time

def get_sum(num1, num2):
    print("I was called")
    time.sleep(10)
    return num1 + num2
		
def add_dependent(num1, num2):
    sum = get_sum(num1, num2)
    return sum


if __name__ == "__main__":
	result = add_dependent(4, 5)
	print("Result: ", result)
	
	
