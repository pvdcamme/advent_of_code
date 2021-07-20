import collections
import hashlib
import re
import copy
import itertools
import pathlib
import json


def get_filepath(file_name):
    """ Returns the full path of the file_name"""
    return pathlib.Path(__file__).parent.joinpath(file_name).resolve()


def solve_day_8_part_ab():
    def escape_str(line):
        return (line.replace("\\", "\\\\").replace('"', '\\"'))

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
            longest = max(longest, current_cost)
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

    return calc_shortest_path(cities,
                              distances), calc_longest_path(cities, distances)


def solve_day_10_part_ab():
    def look_and_say_step(start):
      result = []
      prev = next(start)
      cnt = 1
      for v in start:
        if v == prev:
          cnt += 1
        else:
          yield cnt
          yield prev
          prev = v
          cnt = 1
      yield cnt
      yield prev

    puzzle_input = [int(d) for d in "1113122113"]
    
    v1_step_count = 40
    v2_step_count = 50
    updated_v1 = iter(puzzle_input)
    for _ in range(v1_step_count):
      updated_v1 = look_and_say_step(updated_v1)

    updated_v1 = list(updated_v1)
    updated_v2 = iter(updated_v1)
    for _ in range(v2_step_count- v1_step_count):
      updated_v2 = look_and_say_step(updated_v2)
 
    return len(list(updated_v1)), len(list(updated_v2))

def solve_day_11_part_ab():
  alphabet = "abcdefghijklmnopqrstuvwxyz"
  def next_pass(val):
    new_val = list(val)
    for idx,char in reversed(list(enumerate(val))):
      pos = alphabet.find(char) + 1
      if pos < len(alphabet):
        new_val[idx] = alphabet[pos]
        break
      else:
        new_val[idx] = alphabet[0]
    else:
      return list(alphabet[0] * (len(val) + 1))
    return new_val
  
  def good_pass(val):
    bad_letters = any((bad in val for bad in "iol"))
    succession = any((a+b+c in alphabet for a,b,c in zip(val, val[1:], val[2:]))) 
    repetition_count= 0
    repeated_just_before = False
    for a,b in zip(val, val[1:]):
      if not repeated_just_before and a == b:
        repeated_just_before = True
        repetition_count+= 1
      else:
        repeated_just_before = False
    return succession and repetition_count >= 2 and not bad_letters
    
  def search_next_pass(password):
    password = next_pass(password)
    while not good_pass(password):
      password= next_pass(password)
    return password      

  password_v1= search_next_pass(list("cqjxjnds"))
  password_v2= search_next_pass(password_v1)
  return "".join(password_v1), "".join(password_v2)


def solve_day_12_part_ab():
  def recursively_add(data):
    try:
      return int(data)
    try:
      return sum((recursively_add(d) for d in data.values()))
  with open(get_filepath("day_12.txt"), "r") as f:
    data = json.load(f)
  
  return 0,0
  
def solve():
    day8_a, day8_b = solve_day_8_part_ab()
    print(f"Day8a: The file has {day8_a} additional formatting characters")
    print(f"Day8b: The file has {day8_b} too few formatting characters")

    day9_a, day9_b = solve_day_9_part_ab()
    print(f"Day9a: The shortest route is {day9_a} units")
    print(f"Day9b: The longest route is {day9_b} units")

    day10_a, day10_b = solve_day_10_part_ab()
    print(f"Day10a: The length grows to {day10_a} after applying 40 times")
    print(f"Day10b: The length grows to {day10_b} after applying 50 times")

    day11_a, day11_b = solve_day_11_part_ab()
    print(f"Day11a: Santa's next password is {day11_a}")
    print(f"Day11b: And after that Santa's next password one is {day11_b}")


    day12_a, day12_b = solve_day_12_part_ab()
    print(f"Day12a: Accounting all numbers, added together the give {day12_a}")

if __name__ == "__main__":
    solve()
