"""
  This module contains the solutions of 2015.
  https://adventofcode.com/2015
  
  Solved for fun, code quality could without doubt be a lot
  better.

  Each challange stands more or less on its own. To introduce
  some structure in the code, the solutions are split into 
  separate weeks. This has a decent balance with not too many
  nor too long files.
  (with the main intention to have project stay a fun excercise.)

"""
from .week1 import solve as solve_week_1
from .week2 import solve as solve_week_2


def solve():
    solve_week_1()
    solve_week_2()
