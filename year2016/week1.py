import collections
import hashlib
import re
import copy
import itertools
import pathlib


def get_filepath(file_name):
    """ Returns the full path of the file_name"""
    return pathlib.Path(__file__).parent.joinpath(file_name).resolve()


def solve_day_1_part_ab():
   with open(get_filepath("day_1.txt"), "r") as f:
    line = f.read()


   def split(directive):
    return directive[:1], int(directive[1:])

   ORIENTATIONS= [
          lambda x,y,s: (x, y+s)  ,
          lambda x,y,s: (x+s, y)  ,
          lambda x,y,s: (x, y -s) ,
          lambda x,y,s: (x-s, y)  ,
   ]
    
   def go_left(orientation):
      new_orient = orientation -1
      if new_orient < 0:
        new_orient += len(ORIENTATIONS)
      return new_orient
   def go_right(orientation):
     return (orientation + 1) % len(ORIENTATIONS)

   def distance(x,y):
    return abs(x) + abs(y)

   def travel(instructions):
     x = 0
     y = 0
     orientation= 0
     for direction, steps in instructions:
        if 'L' == direction:
          orientation = go_left(orientation)
        else:
          orientation = go_right(orientation)

        x, y = ORIENTATIONS[orientation](x,y, steps)
     return x, y
   

   sample = list(map(split, line.split(", ")))
   return distance(*travel(sample)), 0


def solve():
    day1_a, day1_b = solve_day_1_part_ab()
    print(f"Day1a: Santa is at {day1_a} blocks away")
    print(f"Day1a: Following the instructions, Santa is at {day1_b} blocks away")

if __name__ == "__main__":
    solve()
