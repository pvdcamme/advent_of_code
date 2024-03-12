import collections
import re
import itertools
import pathlib
import heapq
import copy


def get_filepath(file_name):
    """ Returns the full path of the file_name"""
    return pathlib.Path(__file__).parent.joinpath(file_name).resolve()


def solve_day_8():
    """ Decoding the broken LCD """
    with open(get_filepath("day_8.txt"), "r") as f:
        instructions = [line.strip() for line in f]

    wide = 50
    tall = 6
    lcd = [False] * (wide * tall)

    def as_text(lcd):
        """ Helps with debugging and the 2nd part"""
        txt = ""
        for y in range(tall):
            row_str = ""
            for x in range(wide):
                if get_pixel(lcd, x, y):
                    row_str += "#"
                else:
                    row_str += "."
            txt += row_str + "\n"
        return txt

    def get_pixel(lcd, x, y):
        return lcd[x + y * wide]

    def put_pixel(lcd, x, y, val):
        lcd[x + y * wide] = val
        return val

    def rect(a, b):
        for x in range(a):
            for y in range(b):
                put_pixel(lcd, x, y, True)

    def rotate_by_column(x, amt):
        orig_lcd = list(lcd)
        for y in range(tall):
            src_val = get_pixel(orig_lcd, x, (y - amt) % tall)
            put_pixel(lcd, x, y, src_val)

    def rotate_by_row(y, amt):
        orig_lcd = list(lcd)
        for x in range(wide):
            src_val = get_pixel(orig_lcd, (x - amt) % wide, y)
            put_pixel(lcd, x, y, src_val)

    def eval_instruction(line):
        rect_instr = "rect (\d+)x(\d+)"
        col_rotate = "rotate column x=(\d+) by (\d+)"
        row_rotate = "rotate row y=(\d+) by (\d+)"

        if rect_val := re.match(rect_instr, line):
            a, b = rect_val.groups()
            rect(int(a), int(b))
        elif row_val := re.match(row_rotate, line):
            y, amt = row_val.groups()
            rotate_by_row(int(y), int(amt))
        elif col_val := re.match(col_rotate, line):
            x, amt = col_val.groups()
            rotate_by_column(int(x), int(amt))

    for ins in instructions:
        eval_instruction(ins)

    return sum(lcd), as_text(lcd)


def solve_day_9():
    """ decompressing the text """
    with open(get_filepath("day_9.txt"), "r") as f:
        text = next(f).strip()

    def uncompress(initial_txt, inner):
        """ Taking the state machine approach. 
          The inner argumetn is called each time one
          of the inner values are expanded.

          This allows to solve the 2nd part of the riddle
          fairly cleanly.

          returns fragments of the uncompressed string.
          Joined together these are these are the full 
          decompressed text.
          Working with these fragments as a tradeoff 
          between keeping memory overhead reasonably low
          and increasing efficiency by batching.
      """
        EMPTY_OUT = iter([])
        data = ""

        def handle_char(ch, data):
            if '(' == ch:
                return EMPTY_OUT, handle_range, ""
            else:
                return ch, handle_char, data

        def handle_range(ch, data):
            if 'x' == ch:
                data = (int(data), '')
                return EMPTY_OUT, handle_repeat, data
            else:
                data += ch
                return EMPTY_OUT, handle_range, data

        def handle_repeat(ch, data):
            range_cnt, str_repeat = data
            if ')' == ch:
                data = (int(range_cnt), int(str_repeat), '')
                return EMPTY_OUT, handle_collect, data
            else:
                data = (range_cnt, str_repeat + ch)
                return EMPTY_OUT, handle_repeat, data

        def handle_collect(ch, data):
            range_cnt, repeat, collected = data
            collected += ch
            if range_cnt == 1:
                final = (inner(collected) for _ in range(repeat))

                return itertools.chain(*final), handle_char, ''
            else:
                data = (range_cnt - 1, repeat, collected)
                return EMPTY_OUT, handle_collect, data

        current_state = handle_char
        for ch in initial_txt:
            out, current_state, data = current_state(ch, data)
            yield from out

    def no_expand(vals):
        return iter(vals)

    cache = {}

    def recurse_expand(rr):
        """ Recursively go deeper if the input has more

          Using a cache to efficiently deal with all
          the repeated values.

          Major constraint is trying avoid letting the 
          memory grow too much out of bounds.
      """
        if rr in cache:
            return iter((cache[rr], ))
        elif '(' in rr:
            if len(cache) > 1024:
                cache.clear()
            max_size = 16 * 1024
            elements = [
                ch for idx, ch in zip(range(max_size),
                                      uncompress(rr, recurse_expand))
            ]

            if len(elements) == max_size:
                return uncompress(rr, recurse_expand)
            else:
                elements = ''.join(elements)
                cache[rr] = elements
                return iter((elements, ))
        else:
            return iter((rr, ))

    def part_one(text):
        full_text = list(uncompress(text, no_expand))
        return len(full_text)

    def part_two(text):
        expanded = 0
        for fragment in uncompress(text, recurse_expand):
            expanded += len(fragment)
        return expanded

    return part_one(text), part_two(text)


def solve_day_10():
    """ Robots distributing chips """
    with open(get_filepath("day_10.txt"), "r") as f:
        instructions = [line.strip() for line in f]

    class Bot:
        """ Values and instructions for the Bot.
          Oddly enough we don't need to name.
      """
        def __init__(self):
            self.values = []
            self.outputs = []

        def append(self, val):
            # Match the list.append signature.
            # Makes is polymorphic to add a val to
            # a Bot or an output
            self.values.append(val)

        def instruction(self, lowout, highout):
            self.outputs = [lowout, highout]

        def __call__(self, name, others, outputs):
            should_act = len(self.values) == 2
            if should_act:
                # an easy switch between output locations
                places = {"output": outputs, "bot": others}

                lower, higher = self.outputs
                lower_type, lower_idx = lower
                higher_type, higher_idx = higher

                places[lower_type][lower_idx].append(min(self.values))
                places[higher_type][higher_idx].append(max(self.values))
                self.values.clear()
            return should_act

        def __str__(self):
            return f"Bot has {self.values} and {self.outputs}"

    def decode_instruction(line, bots):
        goes_to = "value (\d+) goes to bot (\d+)"
        hand_over = "bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)"

        if res := re.match(goes_to, line):
            val, bot_idx = res.groups()
            bots[bot_idx].append(int(val))
        elif res := re.match(hand_over, line):
            bot_idx, low_type, low_idx, high_type, high_idx = res.groups()
            bots[bot_idx].instruction((low_type, low_idx),
                                      (high_type, high_idx))
            pass
        else:
            print(f"Not decoded: {line}")

    bots = collections.defaultdict(Bot)
    outputs = collections.defaultdict(list)
    for l in instructions:
        decode_instruction(l, bots)

    acted = True
    responsible = None
    while acted:
        acted = False
        for name, b in bots.items():
            if set([61, 17]) == set(b.values) and not responsible:
                responsible = name
            acted = b(name, bots, outputs) or acted

    def multiply(*vals):
        # For second part
        result = 1
        for a_val in vals:
            result = result * a_val
        return result

    return responsible, multiply(*(outputs["0"] + outputs["1"] + outputs["2"]))


def solve_day_11():
    """ Safely bringing the microchips up """

    initial_floor_1 = set(
        (("thulium", "generator"), ("thulium", "microchip"),
         ("plutonium", "generator"), ("strontium", "generator")))
    initial_floor_2 = set(
        (("plutonium", "microchip"), ("strontium", "microchip")))
    initial_floor_3 = set(
        (("promethium", "generator"), ("promethium", "microchip"),
         ("ruthenium", "generator"), ("ruthenium", "microchip")))

    #initial_floor_1 = set((("hydrogen", "microchip"), ("lithium", "microchip")))
    #initial_floor_2 = set((("hydrogen", "generator"),))
    #initial_floor_3 = set((("lithium", "generator"),))

    initial_floor_4 = set()
    initial_state = (initial_floor_1, initial_floor_2, initial_floor_3,
                     initial_floor_4)

    def is_safe(world):
        for floor in world:
            chips = {rtg for rtg, part in floor if part == "microchip"}
            generators = {rtg for rtg, part in floor if part == "generator"}

            unprotected = chips.difference(generators)
            if len(unprotected) > 0 and len(generators) > 0:
                return False
        return True

    def is_solved(world):
        for lower_floor in world[:3]: 
            if lower_floor:
              return False
        top_floor = world[3]
        return len(top_floor) > 0

    def next_steps(elevator, world):
        def change(next_floor):
            start = world[elevator]

            ## single element moves
            for el in start:
                a_result = copy.deepcopy(world)
                a_result[elevator].remove(el)
                a_result[next_floor].add(el)
                yield (next_floor, a_result)

            ## double element moves
            for el1, el2 in itertools.combinations(start, 2):
                a_result = copy.deepcopy(world)
                a_result[elevator].remove(el1)
                a_result[elevator].remove(el2)
                a_result[next_floor].add(el1)
                a_result[next_floor].add(el2)
                yield (next_floor, a_result)

        total_result = []
        if elevator != 0:
            total_result.extend(change(elevator - 1))
        if elevator != 3:
            total_result.extend(change(elevator + 1))
        return total_result

    assert is_safe(initial_state)
    assert not is_solved(initial_state)

    def freeze_world(elevator, floors):
        def freeze_floor(floor):
          res = []
          for a,b in sorted(floor):
            res.append(a)
            res.append(b)

          return tuple(res)
        floors = tuple(freeze_floor(a_floor) for a_floor in floors)
        return (elevator, floors)

    def show_state(el, ww):
      for idx,  ll in enumerate(ww, start=0):
        if idx == el:
          print(f"{idx + 1} : E , {ll}")
        else:
          print(f"{idx + 1} : . , {ll}")
        

    def search_pathlength(initial_state):
      search = [(0, (0, initial_state))]
      seen = set(freeze_world(1, initial_state))
      while search:
        steps, (elevator, state), *rest = heapq.heappop(search)
        if len(search) % 1024 == 0:
          print(f"Searching in {len(search)} for {steps} -- from {len(seen)} seen")
        for next_el, next_state in next_steps(elevator, state):
          if is_solved(next_state):
            return steps + 1
          frozen = freeze_world(next_el, next_state)
          if frozen not in seen and is_safe(next_state):
            seen.add(frozen)
            heapq.heappush(search,(steps + 1, (next_el, next_state), (elevator, state), *rest))

    return search_pathlength(initial_state), 0


def solve():
    day8_a, day8_b = solve_day_8()
    print(f"Day8a: There would {day8_a} pixels lit")
    print(f"Day8b: There lcd looks like \n {day8_b}")

    day9_a, day9_b = solve_day_9()
    print(f"Day9a: Decompressed the file has {day9_a} characters")
    print(f"Day9a: Recursively decompressing give {day9_b} characters")

    day10_a, day10_b = solve_day_10()
    print(f"Day10a: Bot {day10_a} handles Microchips 17 and 61")
    print(f"Day10b: Multiplied values together are {day10_b}")

    day11_a, day11_b = solve_day_11()
    print(f"Day11a: Santa needs {day11_a} steps with the elevator")
