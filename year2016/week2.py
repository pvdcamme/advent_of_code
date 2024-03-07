import collections
import hashlib
import re
import copy
import itertools
import pathlib


def get_filepath(file_name):
    """ Returns the full path of the file_name"""
    return pathlib.Path(__file__).parent.joinpath(file_name).resolve()


def solve_day_8_part_ab():
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


def solve():
    day8_a, day8_b = solve_day_8_part_ab()
    print(f"Day8a: There would {day8_a} pixels lit")
    print(f"Day8b: There lcd looks like \n {day8_b}")


if __name__ == "__main__":
    solve()
