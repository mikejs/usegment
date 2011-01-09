#!/usr/bin/env python
import re
import sys


def codepoints(s):
    if sys.maxunicode == 0xFFFF:
        # Narrow build
        prev = None

        for c in s:
            code_unit = ord(c)

            # Check if this is the second codepoint in a surrogate pair
            if prev:
                yield (((prev - 0xD800) << 10) | (code_unit - 0xDC00)) + 0x10000
                prev = None
            else:
                if code_unit >= 0xD800 and code_unit <= 0xDBFF:
                    prev = code_unit
                else:
                    yield code_unit
    else:
        # Wide build
        for c in s:
            yield ord(c)


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
    if isinstance(c, basestring):
        c = ord(c)
    return __break_property.get(c, 'Other')


def graphemes(s):
    current_grapheme = u''
    prev_prop = None

    for c in codepoints(s):
        prop = break_property(c)

        if prev_prop and prop in __dont_break.get(prev_prop,
                                                  ['Extend', 'SpacingMark']):
            current_grapheme += unichr(c)
        else:
            if current_grapheme:
                yield current_grapheme
            current_grapheme = unichr(c)

        prev_prop = prop

    # Make sure we yield the final grapheme
    if current_grapheme:
        yield current_grapheme
