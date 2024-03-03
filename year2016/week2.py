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
  return 0,0
def solve():
    day8_a, day8_b = solve_day_8_part_ab()

if __name__ == "__main__":
    solve()
