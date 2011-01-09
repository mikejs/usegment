#!/usr/bin/env python
import re


__dont_break = {'CR': ['LF'],
                'LF': [],
                'Control': [],
                'L': ['L', 'V', 'LV', 'LVT', 'Extend', 'SpacingMark'],
                'LV': ['V', 'T', 'Extend', 'SpacingMark'],
                'V': ['V', 'T', 'Extend', 'SpacingMark'],
                'LVT': ['T', 'Extend', 'SpacingMark'],
                'T': ['T', 'Extend', 'SpacingMark'],
                'Prepend': ['Extend', 'Prepend', 'SpacingMark', 'L', 'V', 'T',
                            'LV', 'LVT', 'Other']}


def __parse_break_property_file(filename='GraphemeBreakProperty.txt'):
    break_category = {}
    
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith("#") or not line.strip():
                continue

            (cp_range, category, rest) = re.split(r'#|;', line, maxsplit=3)

            if '..' in cp_range:
                (start, end) = [int(x, 16) for x in cp_range.split('..')]
            else:
                start = int(cp_range, 16)
                end = start

            for codepoint in xrange(start, end + 1):
                break_category[codepoint] = category.strip()


        return break_category


__break_property = __parse_break_property_file()


def break_property(c):
    return __break_property.get(ord(c), 'Other')


def graphemes(s):
    current_grapheme = u''
    prev_prop = None

    for c in s:
        prop = break_property(c)

        if prev_prop and prop in __dont_break.get(prev_prop,
                                                  ['Extend', 'SpacingMark']):
            current_grapheme += c
        else:
            if current_grapheme:
                yield current_grapheme
            current_grapheme = c

        prev_prop = prop

    # Make sure we yield the final grapheme
    if current_grapheme:
        yield current_grapheme
