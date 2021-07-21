import pathlib
import re

def get_filepath(file_name):
    """Returns the full path of the file_name"""
    return pathlib.Path(__file__).parent.joinpath(file_name).resolve()

def solve_day_15_part_ab():
  def parse_line(line):
    matched = re.match("(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)", line)
    assert matched, line

  with open(get_filepath("day_15.txt"),"r") as f:
    for line in f:
      parse_line(line)

  return 0,0

def solve():
  day15_a, day15_b = solve_day_15_part_ab()
  print(f"Day15b: Highest scoring cookie reach {day15_a} points")

if __name__ == "__main__":
    solve()
