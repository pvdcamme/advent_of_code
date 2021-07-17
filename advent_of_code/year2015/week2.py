import collections
import hashlib
import re
import copy
import itertools
import pathlib

def get_filepath(name):
  return pathlib.Path(__file__).parent.joinpath(name).resolve()

def solve_day_8_part_ab():
    def escape_str(line):
      return (line.replace("\\", "\\\\")
                  .replace('"', '\\"'))
    total_original = 0
    total_memory = 0
    total_more_escaped = 0
    with open(get_filepath("day_8.txt"), "r") as f:
        for line in f:
          line = line.strip()
          total_original += len(line)
          total_memory += len(eval(line))
          total_more_escaped += len(escape_str(line)) + 2

    return total_original - total_memory, total_more_escaped - total_original


def solve_day_9_part_ab():
  def parse(line):
    matched = re.match("(\w+) to (\w+) = (\d+)", line)
    return matched.group(1), matched.group(2), int(matched.group(3))

  def path_cost(path, distances):
    total_cost = 0
    for current_city, next_city in zip(path, path[1:]):
      total_cost += distances[(current_city, next_city)]
    return total_cost      
      
  def calc_shortest_path(cities, distances):
    cheapest = sum(distances.values())
    for path in itertools.permutations(cities):
      current_cost = path_cost(path, distances)
      cheapest = min(cheapest, current_cost)
    return cheapest 
  
  def calc_longest_path(cities, distances):
    longest = 0
    for path in itertools.permutations(cities):
      current_cost = path_cost(path, distances)
      longest= max(longest, current_cost)
    return longest 


  distances = {}    
  cities = set()
  with open(get_filepath("day_9.txt"), "r") as f:
    for line in f:
      src, dst, cost = parse(line)
      distances[(src, dst)] = cost
      distances[(dst, src)] = cost
      cities.add(src)
      cities.add(dst)
        
  return calc_shortest_path(cities, distances), calc_longest_path(cities, distances)

def solve():
    day8_a, day8_b = solve_day_8_part_ab()
    print(f"Day8a: The file has {day8_a} additional formatting characters")
    print(f"Day8b: The file has {day8_b} too few formatting characters")

    day9_a, day9_b = solve_day_9_part_ab()
    print(f"Day9a: The shortest route is {day9_a} units")
    print(f"Day9b: The longest route is {day9_b} units")


if __name__ == "__main__":
    solve()
