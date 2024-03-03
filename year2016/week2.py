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
  
  return 0,0
def solve():
    day8_a, day8_b = solve_day_8_part_ab()
    print(f"Day8a: There would {day8_a} pixels lit")

if __name__ == "__main__":
    solve()
