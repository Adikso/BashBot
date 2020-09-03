def replace_shortcuts(command):
    d = {
        '[UP]': u'\u001b[A',
        '[DOWN]': u'\u001b[B',
        '[LEFT]': u'\u001b[D',
        '[RIGHT]': u'\u001b[C',
        '[ESC]': u'\u001b',
        '[TAB]': u'\u0009',
        '[T]': u'\u0009',
        '[F1]': u'\u001bOP',
        '[F2]': u'\u001bOQ',
        '[F3]': u'\u001bOR',
        '[F4]': u'\u001bOS',
        '[F5]': u'\u001b[15~',
        '[F6]': '',
        '[F7]': u'\u001b[18',
        '[F8]': u'\u001b[19~',
        '[F9]': u'\u001b[20~',
        '[F10]': u'\u001b[21~',
        '[F11]': u'\u001b[23~\u001b',
        '[F12]': u'\u001b[24~\u0008',
        '[<]': u'\u001b\u0005\u0015',  # ^E^U Clears input line
        '<ESC>': u'\u001b',
        '\\a': '\a',
        '\\b': '\b',
        '\\f': '\f',
        '\\n': '\n',
        '\\r': '\r',
        '\\t': '\t',
        '\\v': '\v'
    }

    ctrl_chars = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_"

    for char in ctrl_chars:
        command = command.replace("^" + char, str(chr(ctrl_chars.index(char))))

    for initial, to in d.items():
        command = command.replace(initial, to)

    return command
