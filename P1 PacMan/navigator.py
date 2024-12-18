from maze import *
from exception import PathNotFoundException
from stack import Stack

class PacMan:
    def __init__(self, grid: Maze) -> None:
        self.navigator_maze = grid.grid_representation

    def isValidPos(self,pos) -> bool:
        rows = len(self.navigator_maze)
        cols = len(self.navigator_maze[0])

        if 0<=pos[0]<rows and 0<=pos[1]<cols and self.navigator_maze[pos[0]][pos[1]] == 0:
            return True
        
        return False

    def find_path(self, start, end) -> list:
        
        if self.navigator_maze[start[0]][start[1]] == 1 :
            raise PathNotFoundException
            
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Clockwise
        visitedCells = set()
        path = Stack()
        path.push(start)
        
        while not path.isEmpty():
            if path.lastElement() == end :
                return path.data
            foundWay =False 
            for way in directions:
                nextPos = (path.lastElement()[0]+way[0],path.lastElement()[1]+way[1])
                if self.isValidPos(nextPos) and nextPos not in visitedCells:
                    path.push(nextPos)
                    visitedCells.append(nextPos)
                    foundWay = True
                else:
                    continue
            if not foundWay:
                path.pop()
            
                
        raise PathNotFoundException
