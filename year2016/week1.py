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

  complex_keypad= {
      (2,0): 1,
      (1,1): 2,
      (2,1): 3,
      (3,1): 4,
      (0,2): 5,
      (1,2): 6,
      (2,2): 7,
      (3,2): 8,
      (4,2): 9,
      (1,3): 'A',
      (2,3): 'B',
      (3,3): 'C',
      (2,4): 'D',
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

  def solve_code(*instructions, keypad, start= (1,1)):
    x,y = start
    code = ""
    for line in instructions:
      x,y = solve_line(x,y, line, keypad=keypad)
      code += str(keypad[(x,y)])
    return code
    
  return solve_code(*instructions, keypad=keypad_part1), solve_code(*instructions, keypad=complex_keypad, start=(0,2))
  
def solve_day_3_part_ab():
    def split_triangle(line):
        string_edges = filter(lambda x: x, line.split(" "))
        return [int(d) for d in string_edges]

    with open(get_filepath("day_3.txt"), "r") as f:
      triangles= [split_triangle(line) for line in f]

    def is_triangle(edges):
      for a,b,c in itertools.permutations(edges):
        if a + b <= c:
          return False
      return True

    def rotate_triangle_list(lob_sided_triangles):
      collected = []
      t1 = []
      t2 = []
      t3 = []
      for a,b,c in lob_sided_triangles:
        t1.append(a)
        t2.append(b)
        t3.append(c)
        if len(t1) == 3:
          collected.extend([t1, t2, t3])
          t1 = []
          t2 = []
          t3 = []
      return collected

    return sum(map(is_triangle, triangles)), sum(map(is_triangle, rotate_triangle_list(triangles)))

def solve_day_4_part_ab():
  with open(get_filepath("day_4.txt"), "r") as f:
    instructions = [line.strip() for line in f]
  
  def split(line):
    parts = line.split("-")
    sector_id, hash_code = parts[-1].split("[")
    hash_code = hash_code[:-1]
    sector_id = int(sector_id)
    letters = " ".join(parts[:-1])

    return letters, sector_id, hash_code

  def calc_hash(letters):
    count = collections.Counter(letters)
    del count[" "]
    most_often = sorted(count.items(), key=lambda r: (-r[1], r[0]))

    result =""
    for letter, _ in most_often[:5]:
      result += letter
    return result
  
  def count_valid(rooms):
    total = 0
    for name, sector_id, hash_code in rooms:
      if hash_code == calc_hash(name):
        total += sector_id
    return total

  def rotate_letter(letter, count):
      LETTERS = "abcdefghijklmnopqrstuvwxyz"
      count = count % len(LETTERS)
      
      next_pos = ord(letter) - ord('a') + count
      while next_pos >= len(LETTERS):
        next_pos -= len(LETTERS)
      return LETTERS[next_pos]

  
  def decode_name(room):
    name, sector_id, hash_code = room
    decoded_name = ""
    if calc_hash(name) == hash_code:
      for letter in name:
        if 'a' <= letter <= 'z':
          letter = rotate_letter(letter, sector_id)
        decoded_name += letter
    return decoded_name

  def search_north_pole_sector(rooms):
    for a_room in rooms:
      original_name = decode_name(a_room)
      if "north" in original_name and "pole" in original_name:
        return a_room[1] 
    return 0

  rooms = [split(line) for line in instructions]
  return count_valid(rooms), search_north_pole_sector(rooms)

def solve_day_5():
    import hashlib
    salt = b"reyedfim"

    def first_key_code():
      key_code = ""
      base = hashlib.md5(salt, usedforsecurity=False)
      for idx in itertools.count():
        extra = base.copy()
        extra.update(str(idx).encode())
        hex_vals = extra.hexdigest()
        if hex_vals.startswith("00000"):
          key_code += hex_vals[5]
        if len(key_code) == 8:
          return key_code

    def second_key_code():
      NOT_DISCOVERED = 'z'
      key_code = list(NOT_DISCOVERED * 8)
      base = hashlib.md5(salt, usedforsecurity=False)
      for idx in itertools.count():
        extra = base.copy()
        extra.update(str(idx).encode())
        hex_vals = extra.hexdigest()
        if hex_vals.startswith("00000"):
          key_letter = hex_vals[6]
          key_position = int(hex_vals[5], base=16)

          if key_position < len(key_code) and key_code[key_position] == NOT_DISCOVERED:
            key_code[key_position] = key_letter

          if NOT_DISCOVERED not in key_code:
            return "".join(key_code)





    return first_key_code(), second_key_code()
        

def solve():
    day1_a, day1_b = solve_day_1_part_ab()
    print(f"Day1a: Santa is at {day1_a} blocks away")
    print(f"Day1a: Following the instructions, Santa is at {day1_b} blocks away")

    day2_a, day2_b = solve_day_2_part_ab()
    print(f"Day2a: The code for the simple keypad is {day2_a}")
    print(f"Day2a: The code for the complex keypad is {day2_b}")

    day3_a, day3_b = solve_day_3_part_ab()
    print(f"Day3a: The list has {day3_a} triangles when read horizontal")
    print(f"Day3b: The list has {day3_b} triangles when read vertically")

    day4_a, day4_b = solve_day_4_part_ab()
    print(f"Day4a: The sectors sum up to {day4_a}")
    print(f"Day4b: The sector id of the North pole is {day4_b}")

    day5_a, day5_b = solve_day_5()
    print(f"Day5a: The keycode for the first door is {day5_a}")
    print(f"Day5b: The keycode for the second door is {day5_b}")

if __name__ == "__main__":
    solve()
