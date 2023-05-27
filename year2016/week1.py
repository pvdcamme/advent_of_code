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

   def rotate(start_x, start_y, direction):
      if direction == "L":
        return start_y, -start_x
      else:
        return -start_y, start_x
      
   def walk(x, y, steps):
      return x, y + steps


   def distance(x,y):
    return abs(x) + abs(y)
   def travel(instructions):
     x = 0
     y = 0
     for direction, steps in instructions:
        x, y = rotate(x,y, direction)
        x,y = walk(x,y, steps)
     return x, y
   
   sample = list(map(split, line.split(", ")))
   return distance(*travel(sample)), 0


def solve():
    day1_a, day1_b = solve_day_1_part_ab()
    print(f"Day1a: Santa is at {day1_a} blocks away")
    print(f"Day1a: Following the instructions, Santa is at {day1_b} blocks away")

if __name__ == "__main__":
    solve()
