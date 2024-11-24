import math
import heapq
from pygame.math import Vector2

class block:
    def __init__(self):
        self.parent_i=10
        self.parent_j=5
        self.f=float("inf")
        self.g=float("inf")
        self.h=0
        
        
def is_safe(row,col,grid):
    return (row>=0) and (row<40) and (col>=0) and (col<40) and grid[row][col]==1

def fruit_eaten(row,col,fruit_pos):
    return row,col==fruit_pos

print(fruit_eaten(0,0,Vector2(1,1)))