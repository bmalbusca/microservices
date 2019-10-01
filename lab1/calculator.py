
def  insert_top(value, data_list = []):
    data_list.append(value)


class  rpnCalculator:
    def __init__(self):
        self.memory = []

    def pushValue(self,value=0):
        print("Will push the value %f" %value)
        insert_top(value, self.memory)
    
    def popValue(self):
        return  self.memory.pop()
    def add():
            pass


