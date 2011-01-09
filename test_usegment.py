# -*- coding: utf-8 -*-
import re
import codecs
import usegment


def test_break_property():
    assert usegment.break_property(u'\n') == 'LF'
    assert usegment.break_property(u'\r') == 'CR'
    assert usegment.break_property(u'\t') == 'Control'
    assert usegment.break_property(u'\a') == 'Control'
    assert usegment.break_property(u'\u1100') == 'L'
    assert usegment.break_property(u'\u1160') == 'V'
    assert usegment.break_property(u'\u11A8') == 'T'
    assert usegment.break_property(u'\uAC00') == 'LV'
    assert usegment.break_property(u'\uAC01') == 'LVT'
    assert usegment.break_property(u'\u0903') == 'SpacingMark'
    assert usegment.break_property(u'\u0E40') == 'Prepend'
    assert usegment.break_property(u'\u0308') == 'Extend'
    assert usegment.break_property(u' ') == 'Other'
    assert usegment.break_property(u'a') == 'Other'
    assert usegment.break_property(u'S') == 'Other'


def test_grapheme_break():
    with codecs.open('GraphemeBreakTest.txt', 'r', 'utf-8') as f:
        for line in f:
            if not line.startswith(u'÷'):
                continue

            line = line.split(u'#')[0]

            string = u''
            expect = []
            current_grapheme = u''

            for match in re.finditer(ur'\s?(÷|×) ([A-F\d]+)', line):
                char = unichr(int(match.group(2), 16))

                string += char

                if match.group(1) == u'÷' and current_grapheme:
                    expect.append(current_grapheme)
                    current_grapheme = char
                else:
                    current_grapheme += char

            if current_grapheme:
                expect.append(current_grapheme)

            got = list(usegment.graphemes(string))

            print 'Expected graphemes: ', expect
            print 'Got: ', got

            assert got == expect


def test_codepoints():
    assert list(usegment.codepoints(u'abc')) == [97, 98, 99]

    expect = [97, 0x10000, 98]
    got = list(usegment.codepoints(u'a\U00010000b'))
    assert got == expect

    expect = [97, 0x1D11E, 0x10000, 98]
    got = list(usegment.codepoints(u'a\U0001D11E\U00010000b'))
    assert got == expect
