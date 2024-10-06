'''
    This file contains the class definition for the StrawHat class.
'''
from crewmate import *
from heap import *
from treasure import *
from custom import *

def comp2(a,b):
    if (a.arrival_time + a.remaining_size) == (b.arrival_time + b.remaining_size):
        return a.id < b.id
    return (a.arrival_time + a.remaining_size) < (b.arrival_time + b.remaining_size)


def comp1(a,b):
    return a.load<b.load
    
class StrawHatTreasury:
    '''
    Class to implement the StrawHat Crew Treasury
    '''
    
    def __init__(self, m):

        '''
        Arguments:
            m : int : Number of Crew Mates (positive integer)
        Returns:
            None
        Description:
            Initializes the StrawHat
        Time Complexity:
            O(m)
        '''

        # form crew ka heap
        if m > 0 :
            self.crew = Heap(comp1,[]) # initialise heap
        self.max_working_crew = m
        
    
    def add_treasure(self, treasure):

        '''
        Arguments:
            treasure : Treasure : The treasure to be added to the treasury
        Returns:
            None
        Description:
            Adds the treasure to the treasury
        Time Complexity:
            O(log(m) + log(n)) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''

        if len(self.crew.heap) < self.max_working_crew:# when n<m 
            crewmate = CrewMate()
            crewmate.load = treasure.size + treasure.arrival_time
            crewmate.treasures.append(treasure)
            self.crew.insert(crewmate)

        
        else :# when n>m 
            mincrew = self.crew.extract() # extract the crew with least load
            if mincrew.load > treasure.arrival_time: # when treasure arives before the prev is processed
                mincrew.load += treasure.size
                mincrew.treasures.append(treasure)
                self.crew.insert(mincrew)
            else: # when treasure arrive after the prev is processed 
                mincrew.load = treasure.arrival_time + treasure.size
                self.crew.insert(mincrew)
                mincrew.treasures.append(treasure)
        

    def get_completion_time(self):

        '''
        Arguments:
            None
        Returns:
            List[Treasure] : List of treasures in the order of their ids after updating Treasure.completion_time
        Description:
            Returns all the treasure after processing them
        Time Complexity:
            O(n(log(m) + log(n))) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''
        # list to store the completed treasure , will sort ot later
        completionList = []

        # taking one crewMember at a time
        for crew_member in self.crew.heap: 
            tempHeap = Heap(comp2, [])
            et = 0  # Execution time starts from 0
            prev_treasure = None

            for treasure in crew_member.treasures:
                new_treasure = ModifiedTreasure(treasure)

                # Set the first treasure as the initial one
                if not tempHeap.heap and prev_treasure is None:
                    prev_treasure = new_treasure
                    tempHeap.insert(prev_treasure)
                    et = prev_treasure.arrival_time
                    continue

                # Process treasures from the heap until arrival time of new one stops the currect execution
                while tempHeap.heap and (tempHeap.top().remaining_size + et <= new_treasure.arrival_time):
                    extracted_treasure = tempHeap.extract()
                    extracted_treasure.completion_time = et + extracted_treasure.remaining_size
                    extracted_treasure.treasure_class.completion_time = extracted_treasure.completion_time
                    et = extracted_treasure.completion_time 
                    completionList.append(extracted_treasure)

                # handeling the curent element,
                # will modify only the top, because thats what matters
                if tempHeap.top():# if not empty
                    tempHeap.top().remaining_size -= new_treasure.arrival_time - et
                
                # modify the et anf inserting newTreasure for priority ordering
                et = new_treasure.arrival_time
                tempHeap.insert(new_treasure)

            # handle remaining heap objects
            while tempHeap.heap:
                #ectract the top object 
                extracted_treasure = tempHeap.extract()
                # compTime is et + remSize
                extracted_treasure.completion_time = et + extracted_treasure.remaining_size
                extracted_treasure.treasure_class.completion_time = extracted_treasure.completion_time
                et = extracted_treasure.completion_time
                completionList.append(extracted_treasure)


        # Extract Treasure objects anf then sorting them 
        completionList = [t.treasure_class for t in completionList]  
        completionList.sort(key=lambda treasure: treasure.id) 
        return completionList
