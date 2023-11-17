#add_4.py

class Add:
    num1 = 4
    num2 = 5

    def get_sum(self, num1, num2):
        print("I was called")
        return num1 + num2
		
    def add_dependent(self):
        sum = self.get_sum(self.num1, self.num2)
        return sum


if __name__ == "__main__":
    add = Add()
    result = add.add_dependent()
    print("add_dependent: ", result)
	
	
