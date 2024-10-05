from heap import *
from straw_hat import *
from treasure import *


if __name__=="__main__":
    sh = StrawHatTreasury(1)
    sh.add_treasure(Treasure(1, 4, 4))
    sh.add_treasure(Treasure(2, 10, 7))
    sh.add_treasure(Treasure(3, 4, 10))
    sh.add_treasure(Treasure(4, 1, 20))
    
    completionList = sh.get_completion_time()
    # print([(i.id,i.size,i.arrival_time,i.completion_time) for i in completionList])
    for treasure in completionList:
        print(f"Treasure ID: {treasure.id}, Size: {treasure.size}, Arrival: {treasure.arrival_time}, Completion: {treasure.completion_time}")
    
    