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

   def travel_without_repeat(instructions):
     x = 0
     y = 0
     orientation= 0
     been_there = set()
     been_there.add((x,y))
     for direction, steps in instructions:
        if 'L' == direction:
          orientation = go_left(orientation)
        else:
          orientation = go_right(orientation)

        for _ in range(steps):
          x, y = ORIENTATIONS[orientation](x,y, 1)
          if (x,y) in been_there:
            return (x,y)

          been_there.add((x,y))
     return x, y

   sample = list(map(split, line.split(", ")))
   return distance(*travel(sample)), distance(*travel_without_repeat(sample))

def solve_day_2_part_ab():
  with open(get_filepath("day_2.txt"), "r") as f:
    instructions = [line.strip() for line in f]

  keypad_part1 = {
      (0,0): 1,
      (1,0): 2,
      (2,0): 3,
      (0,1): 4,
      (1,1): 5,
      (2,1): 6,
      (0,2): 7,
      (1,2): 8,
      (2,2): 9,
  }
  directions = {
    "U": lambda x,y: (x, y-1),
    "R": lambda x,y: (x+1, y),
    "L": lambda x,y: (x-1, y),
    "D": lambda x,y: (x, y+1),
  }

  def solve_line(x, y, instructions, keypad):
    for i in instructions:
      next_x, next_y = directions.get(i)(x,y)
      if (next_x, next_y) in keypad:
        x = next_x
        y = next_y
    return x,y

  def solve_code(*instructions, keypad):
    x = 1
    y = 1
    code = ""
    for line in instructions:
      x,y = solve_line(x,y, line, keypad=keypad)
      code += str(keypad[(x,y)])
    return code
    
  return solve_code(*instructions, keypad=keypad_part1), 0
  

def solve():
    day1_a, day1_b = solve_day_1_part_ab()
    print(f"Day1a: Santa is at {day1_a} blocks away")
    print(f"Day1a: Following the instructions, Santa is at {day1_b} blocks away")

    day2_a, day1_b = solve_day_2_part_ab()
    print(f"Day2a: The code for the keypad is {day2_a}")

if __name__ == "__main__":
    solve()
