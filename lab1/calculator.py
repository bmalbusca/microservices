
def  insert_top(value, data_list = []):
    data_list.append(value)


class  rpnCalculator:
    def __init__(self):
        self.memory = []

    def pushValue(self,value=0):
        insert_top(value, self.memory)
    
    def popValue(self):
        return  self.memory.pop()
    def add(self):
        val1 =0;
        val2 =0;
        if (self.memory) :
            val1 =  self.memory.pop()
            
            try:
                val2  = self.memory.pop()
            except IndexError as e:
                return val1            
            return val1+val2
        
        else:
            return None  

