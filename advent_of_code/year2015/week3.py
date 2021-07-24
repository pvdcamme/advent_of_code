import pathlib
import re


def get_filepath(file_name):
    """Returns the full path of the file_name"""
    return pathlib.Path(__file__).parent.joinpath(file_name).resolve()


def solve_day_15_part_ab():
    class Ingredient(object):
        """
        Helper class to easily:
          - Add ingredients together (= sum)
          - Take several spoonfulls (= multiple)
          - And score score the whole.
        """

        def __init__(self, capacity, durability, flavor, texture, calories):
            self.capacity = capacity
            self.durability = durability
            self.flavor = flavor
            self.texture = texture
            self.calories = calories

        def __mul__(self, other):
            return Ingredient(
                self.capacity * other,
                self.durability * other,
                self.flavor * other,
                self.texture * other,
                self.calories * other,
            )

        def __add__(self, other):
            return Ingredient(
                self.capacity + other.capacity,
                self.durability + other.durability,
                self.flavor + other.flavor,
                self.texture + other.texture,
                self.calories + other.calories,
            )

        def score(self):
            return (
                max(0, self.capacity)
                * max(0, self.durability)
                * max(0, self.flavor)
                * max(0, self.texture)
            )

        def __repr__(self):
            return f"Ingredient: {self.__dict__}"

    def parse_line(line):
        matched = re.match(
            "(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)",
            line,
        )
        assert matched, line
        return matched.group(1), Ingredient(
            int(matched.group(2)),
            int(matched.group(3)),
            int(matched.group(4)),
            int(matched.group(5)),
            int(matched.group(6)),
        )

    def split_into_parts(total, nparts):
        """
        Returns a list of nparts whose sum is total.
        """
        if nparts == 1:
            return [[total]]

        results = []
        for p in range(total + 1):
            for child in split_into_parts(total - p, nparts - 1):
                results.append([p] + child)
        return results

    ingredients = []
    with open(get_filepath("day_15.txt"), "r") as f:
        for line in f:
            _, stuff = parse_line(line)
            ingredients.append(stuff)

    best_score_v1 = 0
    best_score_v2 = 0
    for parts in split_into_parts(100, len(ingredients)):
        recipe = [
            ingredient * quantity
            for quantity, ingredient in zip(parts, ingredients)
            if quantity > 0
        ]
        summed = recipe[0]
        for other in recipe[1:]:
            summed += other
        best_score_v1 = max(best_score_v1, summed.score())
        if summed.calories == 500:
            best_score_v2 = max(best_score_v2, summed.score())

    return best_score_v1, best_score_v2


def solve_day_16_part_ab():
    def parse_line(line):
        matched = re.match("Sue (\d+): (.*)", line)
        assert matched, line
        sue_number = int(matched.group(1))
        character = {}
        for identifier in matched.group(2).split(", "):
            part, count = identifier.split(":")
            character[part] = int(count)
        return sue_number, character
    def is_sub_dict(sub_dict, super_dict):
      for k,v in sub_dict.items():
        if v != super_dict.get(k):
          return False
      return True          

    to_match = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    gifting_sue = -1
    with open(get_filepath("day_16.txt"), "r") as f:
        for line in f:
            sue_number, identifiers = parse_line(line)
            if is_sub_dict(identifiers, to_match):
                assert gifting_sue == -1
                gifting_sue = sue_number

    return gifting_sue, 0


def solve():
    day15_a, day15_b = solve_day_15_part_ab()
    print(f"Day15a: Highest scoring cookie reaches {day15_a} points")
    print(f"Day15b: With exactly 500 calories, the best cookie scores {day15_b}")

    day16_a, day16_b = solve_day_16_part_ab()
    print(f"Day16a: Sue {day16_a} was the one, she sent the gift.")


if __name__ == "__main__":
    solve()
