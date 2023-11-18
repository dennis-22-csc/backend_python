#add_7.py

class Add:
    def get_sum(self, num1, num2):
        print("I was called")
        return num1 + num2
		
    def add_dependent(self, num1, num2):
        sum = self.get_sum(num1, num2)
        return sum

class Op:
	def add_op(self, add, num1, num2):
		return add.add_dependent(num1, num2)
		
if __name__ == "__main__":
    add = Add()
    op = Op()
    result = op.add_op(add, 4, 5)
    print("Result: ", result)
	
	
