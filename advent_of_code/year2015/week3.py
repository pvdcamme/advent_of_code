import pathlib
import re

def get_filepath(file_name):
    """Returns the full path of the file_name"""
    return pathlib.Path(__file__).parent.joinpath(file_name).resolve()

def solve_day_15_part_ab():
  class Ingredient(object):
    def __init__(self, capacity, durability, flavor, texture, calories):
      self.capacity = capacity
      self.durability = durability
      self.flavor = flavor
      self.texture = texture
      self.calories = calories

    def __mul__(self, other):
      return Ingredient(self.capacity* other, self.durability * other, self.flavor * other, self.texture *other, self.calories * other)

    def __add__(self, other):
      return Ingredient(self.capacity + other.capacity, self.durability + other.durability, self.flavor + other.flavor, self.texture + other.texture, self.calories + other.calories)
    
    def score(self):
      return max(0, self.capacity) * max(0, self.durability) * max(0, self.flavor) * max(0, self.texture) 
    def __repr__(self):
      return f'Ingredient: {self.__dict__}'

  def parse_line(line):
    matched = re.match("(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)", line)
    assert matched, line
    return matched.group(1), Ingredient(int(matched.group(2)), int(matched.group(3)), int(matched.group(4)), int(matched.group(5)), int(matched.group(6)))
  
  def split_into_parts(total, parts):
    if parts == 1:
      return [[total]]

    results = []
    for p in range(total + 1):
      for child in split_into_parts(total - p, parts -1):
        results.append([p] + child)
    return results
  
  ingredients = []
  with open(get_filepath("day_15.txt"),"r") as f:
    for line in f:
      _, stuff = parse_line(line)
      ingredients.append(stuff)

  best_score_v1 = 0
  best_score_v2 = 0
  for parts in split_into_parts(100, len(ingredients)):
    recipe = [ingredient * quantity for quantity, ingredient in zip(parts, ingredients) if quantity > 0]
    summed = recipe[0]
    for other in recipe[1:]:
      summed += other
    best_score_v1 = max(best_score_v1, summed.score())          
    if summed.calories == 500:
      best_score_v2 = max(best_score_v2, summed.score())

  return best_score_v1, best_score_v2


def solve():
  day15_a, day15_b = solve_day_15_part_ab()
  print(f"Day15a: Highest scoring cookie reaches {day15_a} points")
  print(f"Day15b: With exactly 500 calories, the highest scoring cookie has {day15_b} points")

if __name__ == "__main__":
    solve()
