import collections
import hashlib
import re
import copy
import itertools
import pathlib


def get_filepath(file_name):
    """ Returns the full path of the file_name"""
    return pathlib.Path(__file__).parent.joinpath(file_name).resolve()


def solve_day_8_part_ab():
  with open(get_filepath("day_8.txt"), "r") as f:
    instructions = [line.strip() for line in f]
  
  wide = 50
  tall = 6
  lcd = [False] * (wide * tall)

  def get_pixel(x,y):
    return lcd[x + y * wide]

  def put_pixel(x,y,val):
    lcd[x + y * wide] = val
    return val

  def rect(a,b):
    for x in range(a):
      for y in range(b):
        put_pixel(x,y, True)

    
  def eval_instruction(line):
    rect_instr = "rect (\d+)x(\d+)"
    
    if rect_val := re.match(rect_instr, line):
      a,b = rect_val.groups()
      rect(int(a),int(b))

  for ins in instructions:
    eval_instruction(ins)

  return sum(lcd),0
def solve():
    day8_a, day8_b = solve_day_8_part_ab()
    print(f"Day8a: There would {day8_a} pixels lit")

if __name__ == "__main__":
    solve()
