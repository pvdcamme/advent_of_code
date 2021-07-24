import pathlib
import functools
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

    def equal_cmp(key, sub_value, super_value):
        return sub_value == super_value

    def fuzzy_compare(key, sub_value, super_value):
        sub_too_low = {"trees", "cats"}
        sub_too_high = {"pomeranians", "goldfish"}
        if key in sub_too_low:
            return sub_value > super_value
        elif key in sub_too_high:
            return sub_value < super_value
        else:
            return sub_value == super_value

    def is_sub_dict(sub_dict, super_dict, value_compare=equal_cmp):
        for k, v in sub_dict.items():
            if k not in super_dict or not value_compare(k, v, super_dict[k]):
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

    gifting_sue_v1 = -1
    gifting_sue_v2 = -1
    with open(get_filepath("day_16.txt"), "r") as f:
        for line in f:
            sue_number, identifiers = parse_line(line)
            if is_sub_dict(identifiers, to_match):
                assert gifting_sue_v1 == -1
                gifting_sue_v1 = sue_number
            if is_sub_dict(identifiers, to_match, fuzzy_compare):
                assert gifting_sue_v2 == -1
                gifting_sue_v2 = sue_number

    return gifting_sue_v1, gifting_sue_v2


def solve_day_17_part_ab():
    def calc_combos(total, containers):
        if len(containers) == 1:
            [size] = containers
            if size == total:
              yield [size] 
        else:
    
            first_size = containers[0]
            other_sizes = containers[1:]
            if total == first_size:
              yield [first_size]
            if total > first_size:
              for other in calc_combos(total - first_size, other_sizes):
                yield [first_size] + other 
            for other in calc_combos(total, other_sizes):
              yield other

    with open(get_filepath("day_17.txt"), "r") as f:
        container_sizes = tuple(sorted([int(c) for c in f]))

    total_eggnog = 150
    combos = list(calc_combos(total_eggnog, container_sizes))
    least_containers = min(map(len, combos))
    minimal_count= list(filter(lambda cc: len(cc) == least_containers, combos))

    return len(combos), len(minimal_count)


def solve():
    day15_a, day15_b = solve_day_15_part_ab()
    print(f"Day15a: Highest scoring cookie reaches {day15_a} points")
    print(f"Day15b: With exactly 500 calories, the best cookie scores {day15_b}")

    day16_a, day16_b = solve_day_16_part_ab()
    print(f"Day16a: Sue {day16_a} was the one, she sent the gift.")
    print(f"Day16b: But the real Sue is {day16_b}")

    day17_a, day17_b = solve_day_17_part_ab()
    print(f"Day17a: There {day17_a} combinations to store the eggnog")
    print(f"Day17a: With as few as feasible, there are {day17_b} combinations")


if __name__ == "__main__":
    solve()
