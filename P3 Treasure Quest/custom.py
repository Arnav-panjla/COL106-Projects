from treasure import *
class ModifiedTreasure :
    def __init__(self,treasure):
        '''
        creates treasure class with remining size
        '''
        self.treasure_class = treasure
        self.remaining_size = treasure.size
        self.size = treasure.size
        self.id = treasure.id
        self.arrival_time = treasure.arrival_time
        self.completion_time = treasure.completion_time

        