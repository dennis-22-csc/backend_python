#add_6.py

class Add:
    
    def get_sum(self, num1, num2):
        print("I was called")
        return num1 + num2
		
    def add_dependent(self, nums):
        sum = self.get_sum(nums[0], nums[1])
        return sum


if __name__ == "__main__":
    add = Add()
    result = add.add_dependent([4, 5])
    print("add_dependent: ", result)
	
	
