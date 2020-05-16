#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def highlight(msg: str, color: str='white', bold: bool=False, underline: bool=False):
    if not sys.stdout.isatty():
        return msg
    attr = []
    if bold:
        attr.append('1')
    if underline:
        attr.append('4')
    if not bold and not underline:
        attr.append('0')
    try:
        color = {
            'black':  '90',
            'red':    '91',
            'green':  '92',
            'yellow': '93',
            'blue':   '94',
            'purple': '95',
            'cyan':   '96',
            'white':  '97',
            'DeepPink1':    [ '38', '5', '198' ],
            'DeepSkyBlue2': [ '38', '5', '38'  ],
            'IndianRed1':   [ '38', '5', '203' ],
            'IndianRed':    [ '38', '5', '167' ],
            'SeaGreen2':    [ '38', '5', '83'  ]
        }[color]
    except KeyError:
        #default to white
        color = '97'
    if isinstance(color, str):
        attr.append(color)
    else:
        attr.extend(color)
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
