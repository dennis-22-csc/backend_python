#add_8.py

class Add:
    def get_sum(self, num1, num2):
        print("I was called")
        return num1 + num2
		
    def add_dependent(self, num1, num2):
        if not isinstance(num1, int) or not isinstance(num2, int):
            raise ValueError("Num1 and Num2 needs to be integers")
        sum = self.get_sum(num1, num2)
        return sum

class Op:
    def add_op(self, add, num1, num2):
        try:
            return add.add_dependent(num1, num2)
        except ValueError:
            return 0
		
if __name__ == "__main__":
    add = Add()
    op = Op()
    result = op.add_op(add, "4", 5)
    print("Result: ", result)
	
	
