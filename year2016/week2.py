import collections
import re
import itertools
import pathlib
import heapq
import math


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

    # Asigned unique powers of 2 to each type.
    # Allos for several memory saving tricks later on
    generator = 1
    microchip = 2
    thulium = 4
    plutonium = 8
    strontium = 16
    promethium = 32
    ruthenium = 64
    elerium = 128
    dilithium = 256

    def input_part_a():
        initial_floor_1 = set(
            ((thulium | generator), (thulium | microchip),
             (plutonium | generator), (strontium | generator)))

        initial_floor_2 = set(
            ((plutonium | microchip), (strontium | microchip)))
        initial_floor_3 = set(
            ((promethium | generator), (promethium | microchip),
             (ruthenium | generator), (ruthenium | microchip)))

        initial_floor_4 = set()
        initial_state = (initial_floor_1, initial_floor_2, initial_floor_3,
                         initial_floor_4)
        return initial_state

    def input_part_b():
        state = input_part_a()
        state[0].add((elerium | generator))
        state[0].add((elerium | microchip))
        state[0].add((dilithium | generator))
        state[0].add((dilithium | microchip))
        return state

    def is_safe_floor(floor):
        chips = 0
        generators = 0
        for part in floor:
            if (part & microchip) > 0:
                chips = chips | part
            else:
                generators = generators | part

        if generators == 0:
            return True

        chips = chips >> 2
        generators = generators >> 2
        unprotected = chips & ~generators
        return unprotected <= 0

    def is_safe(world):
        for floor in world:
            if not is_safe_floor(floor):
                return False
        return True

    def is_solved(world):
        for lower_floor in world[:3]:
            if len(lower_floor) > 0:
                return False
        top_floor = world[3]
        return len(top_floor) > 0

    def next_steps(elevator, world):
        """ Only generates next valid steps """
        def copy_world():
            # Explict 4 levels, because it made a large difference to performance.
            return (set(world[0]), set(world[1]), set(world[2]), set(world[3]))

        def change(next_floor):
            start = world[elevator]

            ## single element moves
            for el in start:
                a_result = copy_world()
                current_floor = a_result[elevator]
                target_floor = a_result[next_floor]

                current_floor.remove(el)
                target_floor.add(el)
                if is_safe_floor(current_floor) and is_safe_floor(
                        target_floor):
                    yield (next_floor, a_result)

            ## double element moves
            for el1, el2 in itertools.combinations(start, 2):
                a_result = copy_world()
                current_floor = a_result[elevator]
                target_floor = a_result[next_floor]

                current_floor.remove(el1)
                current_floor.remove(el2)
                if not is_safe_floor(current_floor):
                    continue

                target_floor.add(el1)
                target_floor.add(el2)
                if is_safe_floor(target_floor):
                    yield (next_floor, a_result)

        if elevator != 0:
            yield from change(elevator - 1)
        if elevator != 3:
            yield from change(elevator + 1)

    def freeze_world(elevator, floors):
        """ Freeze the world to make it easier find back. """
        res = []

        def freeze_floor(floor):
            yield from sorted(floor)
            # As stop marker.
            yield 0

        for a_floor in floors:
            res.extend(freeze_floor(a_floor))

        return (elevator, *res)

    def search_pathlength(initial_state):
        """ A-star search approach.
          Guaranteed to find a correct match thanks
          to an admissable heuristic
      """
        def min_remaining_steps(floors):
            min_cost = 0
            for lvl, a_floor in enumerate(floors[:3], start=1):
                min_cost += math.ceil(len(a_floor) / 2) * (4 - lvl)
            return min_cost

        search = [(min_remaining_steps(initial_state), 0, (0, initial_state))]
        seen = set(freeze_world(1, initial_state))
        while search:
            estimated, steps, (elevator, state) = heapq.heappop(search)

            next_steps_cnt = steps + 1
            for next_el, next_state in next_steps(elevator, state):
                if is_solved(next_state):
                    return next_steps_cnt
                if (frozen := freeze_world(next_el, next_state)) not in seen:
                    seen.add(frozen)
                    heapq.heappush(search, (
                        min_remaining_steps(next_state) + next_steps_cnt,
                        next_steps_cnt,
                        (next_el, next_state),
                    ))

    return search_pathlength(input_part_a()), search_pathlength(input_part_b())


def solve_day_12():
    """ Running the program """
    with open(get_filepath("day_12.txt"), "r") as f:
        instructions = [line.strip() for line in f]

    registers = {"a": 0, "b": 0, "c": 0, "d": 0}

    def apply(inst, registers):
        """ Runs the instructions using the register.
            Returns the offset of next next instruction
        """
        cpy_inst = "cpy (\d+|[abcd]) ([abcd])"
        inc_inst = "inc ([abcd])"
        dec_inst = "dec ([abcd])"
        jnz_inst = "jnz (\d+|[abcd]) (-*\d+)"
        program_inc = 1

        if cpy_val := re.match(cpy_inst, inst):
            src, dest = cpy_val.groups()
            if src in registers:
                registers[dest] = registers[src]
            else:
                registers[dest] = int(src)

        elif inc_val := re.match(inc_inst, inst):
            src, = inc_val.groups()
            registers[src] += 1
        elif dec_val := re.match(dec_inst, inst):
            src, = dec_val.groups()
            registers[src] -= 1
        elif jnz_val := re.match(jnz_inst, inst):
            src, dest = jnz_val.groups()
            if src in registers and registers[src] != 0:
                program_inc = int(dest)
            elif src in registers:
                pass
            elif int(src) != 0:
                program_inc = int(dest)

        else:
            print(f"unknown: {inst}")
        return program_inc

    def run_program(registers):
      program_counter = 0
      while program_counter < len(instructions):
        current = instructions[program_counter]
        offset = apply(current, registers)

        program_counter += offset
      return registers
    
    result_a = run_program(registers.copy())


      
    return result_a["a"], 0


def solve():
    import cProfile
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
    print(f"Day11a: Santa needs extra {day11_b} steps")

    day12_a, day12_b = solve_day_12()
    print(f"Day12a: Register a has {day12_a}")
