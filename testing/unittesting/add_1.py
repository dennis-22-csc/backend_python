#add_1.py

def get_num1():
    return 5
def get_num2():
    return 4
def get_sum(num1, num2):
    print("I was called")
    return num1 + num2
		
def add_dependent():
    num1 = get_num1()
    num2 = get_num2()
    sum = get_sum(num1, num2)
    return sum


if __name__ == "__main__":
	result = add_dependent()
	print("add_dependent: ", result)
	
	
