import pathlib
import functools
import re
import heapq
import itertools
import collections


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
    minimal_count = list(filter(lambda cc: len(cc) == least_containers, combos))

    return len(combos), len(minimal_count)


def solve_day_18_part_ab():
    def neighbours(x, y, max_c=100):
        lower_x = max(0, x - 1)
        upper_x = min(x + 2, max_c)

        lower_y = max(0, y - 1)
        upper_y = min(y + 2, max_c)

        all_neighbours = (
            (nx, ny) for nx in range(lower_x, upper_x) for ny in range(lower_y, upper_y)
        )
        return [(nx, ny) for nx, ny in all_neighbours if nx != x or ny != y]

    def count_lights(grid):
        total = 0
        for row in grid:
            total += sum(row)
        return total

    def update_grid(old_grid):
        new_grid = []
        for x, old_row in enumerate(old_grid):
            new_row = []
            for y, val in enumerate(old_row):
                nvals = sum(map(lambda cor: old_grid[cor[0]][cor[1]], neighbours(x, y)))
                next_val = nvals == 3 or (val and nvals == 2)
                new_row.append(next_val)
            new_grid.append(new_row)
        return new_grid

    def light_up_the_corner(grid_v2):
        grid_v2[0][0] = True
        grid_v2[99][0] = True
        grid_v2[0][99] = True
        grid_v2[99][99] = True
        return grid_v2

    grid = []
    with open(get_filepath("day_18.txt"), "r") as f:
        for line in f:
            grid.append(["#" == c for c in line.strip()])

    grid_v1 = grid
    for _ in range(100):
        grid_v1 = update_grid(grid_v1)

    grid_v2 = light_up_the_corner(grid)
    for _ in range(100):
        grid_v2 = update_grid(grid_v2)
        grid_v2 = light_up_the_corner(grid_v2)

    return count_lights(grid_v1), count_lights(grid_v2)


def solve_day_19_part_ab():
    def read_replacement(line):
        matched = re.match("(\w+) => (\w+)", line)
        if matched:
            return matched.group(1), matched.group(2)

    def step_replacements(line, replacements):
        for start, end in replacements:
            idx = line.find(start)
            while idx > -1:
                new_line = line[:idx] + end + line[idx + len(start) :]
                yield new_line
                idx = line.find(start, idx + 1)

    def best_first_search(start, end, replacements):
        results = [(len(start), 1, start)]
        seen = set()
        while True:
            best_score, steps, best_val = heapq.heappop(results)
            for a in step_replacements(best_val, replacements):
                if a == end:
                    return steps
                if a not in seen:
                    heapq.heappush(results, (len(a), steps + 1, a))

    replacements = []
    target = ""
    with open(get_filepath("day_19.txt"), "r") as f:
        for line in f:
            line = line.strip()
            conversion = read_replacement(line)
            if conversion:
                start, end = conversion
                replacements.append((start, end))
            elif line:
                target = line

    all_replacements = set(step_replacements(target, replacements))
    reverse_replace = [(end, start) for start, end in replacements]
    return len(all_replacements), best_first_search(target, "e", reverse_replace)


def solve_day_20_part_ab():
    def adding():
        houses = collections.defaultdict(list)
        for idx in itertools.count(1):
            current = houses[idx]
            current.append(idx)
            summed = 0
            for c in current:
                houses[idx + c].append(c)
                summed += c
            del houses[idx]
            yield summed * 10

    def limited_adding():
        houses = collections.defaultdict(list)
        for idx in itertools.count(1):
            current = houses[idx]
            current.append((idx, 50))
            summed = 0
            for elf_idx, count in current:
                summed += elf_idx
                if count > 1:
                    houses[idx + elf_idx].append((elf_idx, count - 1))
            del houses[idx]
            yield summed * 11

    many_presents = 34000000
    for idx_v1, presents in enumerate(adding(), start=1):
        if presents >= many_presents:
            break
    for idx_v2, presents in enumerate(limited_adding(), start=1):
        if presents >= many_presents:
            break

    return idx_v1, idx_v2


def solve_day_21_part_ab():
    weapons = [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)]
    armors = [(0, 0, 0), (13, 0, 1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5)]
    rings = [(25, 1, 0), (50, 2, 0), (100, 3, 0), (20, 0, 1), (40, 0, 2), (80, 0, 3)]

    def combine(*items):
        total_attack, total_defense = (0, 0)
        total_price = 0
        for price, attack, defense in items:
            total_price += price
            total_attack += attack
            total_defense += defense
        return (total_price, total_attack, total_defense)

    def outfits():
        for weapon in weapons:
            for armor in armors:
                yield combine(weapon, armor)
                for r in rings:
                    yield combine(weapon, armor, r)
                for r1, r2 in itertools.product(rings, rings):
                    if r1 == r2:
                        continue
                    yield combine(weapon, armor, r1, r2)

    def play(attack, defense):
        player_health = 100
        boss_health = 100
        boss_attack = 8
        boss_def = 2
        while True:
            boss_health -= max(1, attack - boss_def)
            if boss_health <= 0:
                return True
            player_health -= max(1, boss_attack - defense)
            if player_health <= 0:
                return False

    def cheapest_win():
        wins = (price for price, att, defen in outfits() if play(att, defen))
        return min(wins)

    def most_expensive_loss():
        loses = (price for price, att, defen in outfits() if not play(att, defen))
        return max(loses)

    return cheapest_win(), most_expensive_loss()


def solve_day_22_part_ab():
    import copy
    import random

    CAST_ANY_TIME = -1

    def boss_turn(timer, player, boss):
      MINIMUM_DAMAGE = 1 
      player_damage = max(boss_damage - player['armor'], MINIMUM_DAMAGE)
      player['hit_points'] -= player_damage
      return CAST_ANY_TIME
 
    def magic_missle(timer, player, boss):
      boss['hit_points'] -= 4
      return CAST_ANY_TIME
      
    def drain(timer, player, boss):
      boss['hit_points'] -= 2
      player['hit_points'] += 2
      return CAST_ANY_TIME
      
    def shield(timer, player, boss):
      player['armor'] += 7
      until = timer + 5
      def apply_effect(timer, player, boss):
        should_continue= timer <= until
        if not should_continue:
          player['armor'] -= 7
        return should_continue 
      player['effects'].append(apply_effect)
      return until 

    def poison(timer, player, boss):
      until = timer + 5 
      def apply_effect(timer, player, boss):
        boss['hit_points'] -= 3
        return timer <= until
      player['effects'].append(apply_effect)
      return until 

    def recharge(timer, player, boss):
      until = timer + 4
      def apply_effect(timer, player, boss):
        player['mana'] += 101
        return timer <= until
      player['effects'].append(apply_effect)
      return until 

    boss_hit_points= 51
    boss_damage= 9

    default_spells = [(CAST_ANY_TIME, 53, magic_missle), (CAST_ANY_TIME, 73, drain),
                      (CAST_ANY_TIME, 113, shield), (CAST_ANY_TIME, 173, poison),
                      (CAST_ANY_TIME, 229, recharge) ]

    player = {'hit_points': 50, 'mana':500, 'spells': default_spells, 'effects': [], 'armor': 0}
    boss = {'hit_points': boss_hit_points}
    world = {"timer": 1, "player": player, "boss": boss}


    def apply_effects(world, effects) -> list:
        new_effects = []
        for effect in effects:
          result = effect(**world)
          if result:
            new_effects.append(effect)
        return new_effects

    def default_turn_effect(timer, player, boss):
      pass

    def hard_mode(timer, player, boss):
      #if timer % 2 == 1:
      player["hit_points"] -= 1

    def search(world, difficulty=default_turn_effect):
      moves = [(0 , world)]
      while moves:
        mana_cost, best_world = heapq.heappop(moves) 
        best_world = copy.deepcopy(best_world)
  
        
        difficulty(**best_world)

        if  best_world["player"]["hit_points"] <= 0:
          continue

        if  best_world["boss"]["hit_points"] < 0:
          return mana_cost



        best_world["player"]["effects"] = apply_effects(best_world, best_world["player"]["effects"])
  
        is_boss_turn = (best_world["timer"] % 2) == 0
        best_world["timer"] += 1
  
        if is_boss_turn:
          boss_turn(**best_world)
          if best_world["player"]["hit_points"] >= 0:
            heapq.heappush(moves, (mana_cost, best_world))
        else:
          for idx, (until, spell_cost, pick) in enumerate(best_world["player"]["spells"]):
            if until <= best_world["timer"] and spell_cost < best_world["player"]["mana"]:
              new_world = copy.deepcopy(best_world)
              new_until = pick(**new_world)
              new_world["player"]["spells"][idx] = (new_until, spell_cost, pick)
              new_world["player"]['mana'] -= spell_cost
  
              new_mana_cost = mana_cost + spell_cost
              new_mana_cost += random.random() / 1e3 # Make every value unique 
              if new_world["boss"]["hit_points"] <= 0:
                return new_mana_cost
              else:
                heapq.heappush(moves, (new_mana_cost, new_world))
       
    return search(world), search(world, hard_mode)
  

def solve():
    day15_a, day15_b = solve_day_15_part_ab()
    print(f"Day15a: Highest scoring cookie reaches {day15_a} points")
    print(f"Day15b: With exactly 500 calories, the best cookie scores {day15_b}")

    day16_a, day16_b = solve_day_16_part_ab()
    print(f"Day16a: Sue {day16_a} was the one, she sent the gift.")
    print(f"Day16b: But the real Sue is {day16_b}")

    day17_a, day17_b = solve_day_17_part_ab()
    print(f"Day17a: There are {day17_a} combinations to store the eggnog")
    print(f"Day17b: With as few as feasible, there are {day17_b} combinations")

    day18_a, day18_b = solve_day_18_part_ab()
    print(f"Day18a: {day18_a} are on after 100 steps.")
    print(f"Day18b: With the corners stuck there {day18_b} lights lit")

    day19_a, day19_b = solve_day_19_part_ab()
    print(f"Day19a: {day19_a} distinct molecules from a single replacement.")
    print(f"Day19b: Frabricating the medicine will take {day19_b} steps.")

    day20_a, day20_b = solve_day_20_part_ab()
    print(f"Day20a: House {day20_a} gets a lot of presents from infinite elves")
    print(f"Day20b: House {day20_b} gets a lot of presents from finite elves")

    day21_a, day21_b = solve_day_21_part_ab()
    print(f"Day21a: Winning for only {day21_a} gold")
    print(f"Day21b: Most expensive loss costs {day21_b} gold")

if __name__ == "__main__":
    solve()
