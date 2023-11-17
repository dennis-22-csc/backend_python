#add_2.py

num1 = 4
num2 = 5

def get_sum(num1, num2):
    print("I was called")
    return num1 + num2
		
def add_dependent():
    sum = get_sum(num1, num2)
    return sum


if __name__ == "__main__":
	result = add_dependent()
	print("add_dependent: ", result)
	
	
