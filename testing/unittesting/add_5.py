#add_5.py

class Add:
    
    def get_sum(self, num1, num2):
        print("I was called")
        return num1 + num2
		
    def add_dependent(self, num1, num2):
        sum = self.get_sum(num1, num2)
        return sum


if __name__ == "__main__":
    add = Add()
    result = add.add_dependent(4, 5)
    print("add_dependent: ", result)
	
	
