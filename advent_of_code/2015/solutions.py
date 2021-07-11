import collections
import hashlib


def solve_day_1_part_ab():
    position = 0
    current_char = 0
    first_basement = 1e9
    with open("day_1.txt", "r") as f:
        for l in f:
            for ch in l:
                current_char += 1
                if ch == '(':
                    position += 1
                elif ch == ')':
                    position -= 1
                if position == -1:
                    first_basement = min(first_basement, current_char)
    return (position, first_basement)


def solve_day_2_part_ab():
    def parse_box(line):
        l, w, h = line.strip().split("x")
        return int(l), int(w), int(h)

    def wrapping_paper(l, w, h):
        sides = [l * w, w * h, h * l]
        return min(sides) + 2 * sum(sides)

    def ribbon(l, w, h):
        sides = sorted([l, w, h])
        around = 2 * sides[0] + 2 * sides[1]
        tie = sides[0] * sides[1] * sides[2]
        return around + tie

    total_area = 0
    total_ribbon = 0
    with open("day_2.txt", "r") as f:
        for line in f:
            l, w, h = parse_box(line)
            total_area += wrapping_paper(l, w, h)
            total_ribbon += ribbon(l, w, h)
    return total_area, total_ribbon


def solve_day_3_part_ab():
    def new_position(orig, direction):
        x, y = orig
        if direction == '^':
            y += 1
        elif direction == 'v':
            y -= 1
        elif direction == '>':
            x += 1
        elif direction == '<':
            x -= 1
        else:
            print(f'Unknown character {direction}')
        return x, y

    position = (0, 0)
    been_there = collections.defaultdict(int)
    been_there[position] += 1

    with open("day_3.txt", "r") as f:
        for line in f:
            for ch in line:
                position = new_position(position, ch)
                been_there[position] += 1

    santa_position = (0, 0)
    robo_position = (0, 0)
    next_been = collections.defaultdict(int)
    with open("day_3.txt", "r") as f:
        santa_move = True
        for line in f:
            for ch in line:
                if santa_move:
                    santa_position = new_position(santa_position, ch)
                    next_been[santa_position] += 1
                else:
                    robo_position = new_position(robo_position, ch)
                    next_been[robo_position] += 1
                santa_move = not santa_move
    return (len(been_there), len(next_been))


def solve_day_4_part_ab():
    def generate_hashes(key):
        ctr = 1
        while True:
            to_hash = key + str(ctr)
            hash_obj = hashlib.md5(to_hash.encode("utf8"))
            yield hash_obj.hexdigest()
            ctr += 1

    key = "bgvyzdsv"
    five_compare = "0" * 5
    six_compare = "0" * 6
    for five_zeros, hh in enumerate(generate_hashes(key), 1):
        if hh.startswith(five_compare):
            break
    for six_zeros, hh in enumerate(generate_hashes(key), 1):
        if hh.startswith(six_compare):
            break
    return (five_zeros, six_zeros)


def solve_day_5_part_ab():
    def is_nice(line):
        num_vowels = len(list(filter(lambda c: c in "aeiou", line)))
        duplicated = any((a == b for a, b in zip(line, line[1:])))
        forbidden = any((x in line for x in ["ab", "cd", "pq", "xy"]))
        return num_vowels >= 3 and duplicated > 0 and not forbidden

    def is_nice_v2(line):
        reseen = False
        for idx, (a, b) in enumerate(zip(line, line[1:])):
            if (a + b) in line[idx + 2:]:
                reseen = True
                break

        duplicated = any((a == b for a, b in zip(line, line[2:])))
        return reseen and duplicated > 0

    nice_strings = 0
    nice_strings_v2 = 0
    with open("day_5.txt", "r") as f:
        for line in f:
            nice_strings += is_nice(line)
            nice_strings_v2 += is_nice_v2(line)
    return (nice_strings, nice_strings_v2)


def solve_day_6_part_ab():
    import re

    def parse_line(line):
        result = re.match(
            "(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)",
            line.strip())
        return result.group(1), (int(result.group(2)),
                                 int(result.group(3))), (int(result.group(4)),
                                                         int(result.group(5)))

    grid = [[False for _ in range(1000)] for _ in range(1000)]
    grid_v2 = [[0 for _ in range(1000)] for _ in range(1000)]

    turn_off = lambda prev_val: False
    turn_on = lambda prev_val: True
    toggle = lambda prev_val: not prev_val
    actions = {"turn on": turn_on, "turn off": turn_off, "toggle": toggle}
    actions_v2 = {
        "turn on": lambda prev: prev + 1,
        "turn off": lambda prev: max(0, prev - 1),
        "toggle": lambda prev: prev + 2
    }

    def update(grid, x, y, action):
        old_val = grid[x][y]
        grid[x][y] = action(old_val)

    with open("day_6.txt", "r") as f:
        for line in f:
            current_action, start, end = parse_line(line)
            start_x, start_y = start
            end_x, end_y = end
            action_v1 = actions[current_action]
            action_v2 = actions_v2[current_action]
            for y in range(start_y, end_y + 1):
                for x in range(start_x, end_x + 1):
                    update(grid, x, y, action_v1)
                    update(grid_v2, x, y, action_v2)

    total_lit = sum((sum(row) for row in grid))
    total_brightness = sum((sum(row) for row in grid_v2))
    return total_lit, total_brightness


def solve():
    day1_a, day1_b = solve_day_1_part_ab()
    print(f"Day1a: Santa is at floor {day1_a}")
    print(f"Day1b: Santa enters the basement at {day1_b}")

    day2_a, day2_b = solve_day_2_part_ab()
    print(f"Day2a: Elves require {day2_a} square feet of wrapping paper")
    print(f"Day2b: In addition the elves require {day2_b} feet of ribbon")

    day3_a, day3_b = solve_day_3_part_ab()
    print(f"Day3a: Santa has visited {day3_a} houses")
    print(f"Day3b: Santa and robo santa have seen now {day3_b} houses")

    day4_a, day4_b = solve_day_4_part_ab()
    print(f"Day4a: First hash with 5 zeros is at count {day4_a}")
    print(f"Day4a: First hash with 6 zeros is at count {day4_b}")

    day5_a, day5_b = solve_day_5_part_ab()
    print(f"Day5a: Counted {day5_a} nice strings")
    print(f"Day5a: Counted {day5_b} nice strings in version 2")

    day6_a, day6_b = solve_day_6_part_ab()
    print(f"Day6a: {day6_a} light are lit")
    print(f"Day6b: {day6_b} is the total brightness")


if __name__ == "__main__":
    solve()
