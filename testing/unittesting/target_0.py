#target_0.py

class Target:
    def apply(self, value, flag):
        if flag == 1:
            return f"Applied. Value is {value}"
        else:
            return None

def method(target, value, flag):
    return target.apply(value, flag)


if __name__ == "__main__":
    target = Target()
    print(method(target, "Dennis", 1))
