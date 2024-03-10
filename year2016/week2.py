import collections
import hashlib
import re
import copy
import itertools
import pathlib
import enum


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
        return iter((cache[rr],))
      elif '(' in rr:
        if len(cache) > 1024:
          cache.clear()
        max_size = 1024 * 1024
        elements = [ch for idx, ch in zip(range(max_size), uncompress(rr, recurse_expand))]

        if len(elements) == max_size:
          return uncompress(rr, recurse_expand)
        else:
          elements = ''.join(elements)
          cache[rr] = elements
          return iter((elements,))
      else:
        return iter((rr,))

    def part_one(text):
      full_text = list(uncompress(text, no_expand))
      return len(full_text)

    def part_two(text):
      expanded= 0
      for fragment in uncompress(text, recurse_expand):
        expanded += len(fragment)
      return expanded

    return part_one(text), part_two(text)

def solve():
    day8_a, day8_b = solve_day_8()
    print(f"Day8a: There would {day8_a} pixels lit")
    print(f"Day8b: There lcd looks like \n {day8_b}")

    day9_a, day9_b = solve_day_9()
    print(f"Day9a: Decompressed the file has {day9_a} characters")
    print(f"Day9a: Recursively decompressing give {day9_b} characters")

