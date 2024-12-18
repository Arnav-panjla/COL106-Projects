class Stack:
    def __init__(self) -> None:
        self.data = []
        
    def len(self) -> int:
        return len(self.data)
        
    def push(self, element) -> None:
        self.data.append(element)
    
    def isEmpty(self) -> bool:
        return self.len() == 0
        
    def pop(self):
        if self.isEmpty():
            return None
        else:
            return self.data.pop()
    def lastElement(self):
        return self.data[-1]
