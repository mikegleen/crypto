import argparse
from colorama import Fore, Style
import curses
from inspect import currentframe as cf
from inspect import getframeinfo
from string import ascii_uppercase, ascii_lowercase
import sys

HEADER_LEN = 3
NOPT = '_'  # character representing no plaintext

def trace(level, template, *args, color=None, frame=None):

    if logfile and _args.verbose >= level:
        if frame:
            line = getframeinfo(frame).lineno
            print(f'{line=} {template.format(*args)}', file=logfile)
        elif color:
            print(f'{color}{template.format(*args)}{Style.RESET_ALL}', file=logfile)
        else:
            print(template.format(*args), file=logfile)



def getparser() -> argparse.ArgumentParser:
    """
    Called either by getargs() in this file or by Sphinx.
    :return: an argparse.ArgumentParser object
    """
    parser = argparse.ArgumentParser(description='''
    ''')
    parser.add_argument('infile')
    parser.add_argument('-l','--log')
    parser.add_argument('-t','--test', type=int)
    parser.add_argument('-v', '--verbose', type=int, default=1, help='''
        Set the verbosity. The default is 1 which prints summary information.
        ''')
    return parser


def getargs(argv):
    parser = getparser()
    args = parser.parse_args(args=argv[1:])
    return args


def read_cipher() -> list[str]:
    cipher = []
    infile = open(_args.infile)
    for line in infile:
        line = line.strip()
        if line:
            cipher.append(line)
    return cipher


def dumpxl(marker):
    print(f'dumpxl: {marker}', file=logfile)
    # print(f'{len(xl)=}, {ascii_uppercase=}, {xl=}')
    # print('    ', ('{:02d} ' * len(xl)).format(*range(26)))
    print('    ', (' {} ' * len(xl)).format(*[char for char in ascii_uppercase]),
          file=logfile)
    print(' xl=', (' {} ' * len(xl)).format(*xl.values()),
          file=logfile)
    print('rxl=', (' {} ' * len(rxl)).format(*rxl.values()),
          file=logfile)


def test_update_mapping():
    print('Testing update_mapping()')
    for mapping in (('a', 'b'), ('d', 'c'), ('a', 'c'), ('ef', 'gh'), ('a', '-')):
        print(f'\n{mapping=}')
        update_mapping(*mapping)
        dumpxl('test')


def test():
    match _args.test:
        case 1:
            test_update_mapping()
        case _:
            print('Not a valid test.')


def machine(state: int, char: str) -> int:
    global command, instr
    match state:
        case 0:

            instr += char
            state = 1
    return state


def update_mapping(ctstr: str, ptstr: str):
    """

    :param ctstr: ciphertext characters
    :param ptstr: plaintext characters
    :return: None, xl and rxl are updated
    """
    dumpxl('begin update_mapping')
    if len(ctstr) != len(ptstr):
        print(f'"{ctstr}" not same length as "{ptstr}". Command ignored.')
        return
    for ix, newct in enumerate(ctstr.upper()):
        # print(f'{newct=}')
        if newct not in au_set:
            print(f'"{newct}" is not alphabetic. Command ignored.')
            continue
        newpt = ptstr[ix].upper()
        if newpt not in au_set:
            newpt = NOPT
        # remove any old mapping
        oldpt = xl[newct]
        # print(f'{oldpt=}')
        trace(1, f'{newct=} {newpt=} {oldpt=} ', frame=cf())
        if rxl[newpt] in au_set:
            oldct = rxl[newpt]
            trace(1, f'{oldct=} ', frame=cf())
            xl[oldct] = NOPT
            rxl[oldpt] = NOPT
            # An old ct may have been pointing to the new pt. Remove that mapping.
            if newpt in au_set:
                oldrevct = rxl[newpt]
                # print(f'{oldrevct=}')
                if oldrevct in au_set:
                    xl[oldrevct] = NOPT
        # Assign the new mapping
        xl[newct] = newpt
        if newpt in au_set:
            rxl[newpt] = newct
    dumpxl('end update_mapping')


def display_cipher(scr, cipher):
    pt_last_row = 0  # stop PyCharm whining
    row_one =  '  ' + '  '.join([char for char in ascii_uppercase])
    row_two =  '  ' + '  '.join([xl[char] for char in ascii_uppercase])
    scr.addstr(0, 0, row_one)
    scr.addstr(1, 0, row_two)
    for row, line in enumerate(cipher):
        pt_last_row = row * 3 + HEADER_LEN  # last row of plaintext
        scr.addstr(pt_last_row, 0, line)
        ptlist = []
        for ch in line:
            if ch in au_set:
                ptlist.append(xl[ch])
            elif ch in ascii_lowercase:
                ptlist.append(xl[ch.upper()].lower())
            else:
                ptlist.append(ch)
        pline = ''.join(ptlist)
        scr.addstr(pt_last_row + 1, 0, pline)
        curses.napms(10)
    return pt_last_row


def main(scr):
    global instr
    maxrows, maxcols = scr.getmaxyx()
    lastrow = maxrows - 1
    lastcol = maxcols - 1
    scr.addstr(lastrow, 0, f'Hello World, {lastrow=}, {lastcol=}, {type(scr)=}')
    cipher = read_cipher()    # for row, line in enumerate(cipher):
    #     pt_last_row = row * 3 + HEADER_LEN  # last row of plaintext
    #     scr.addstr(pt_last_row, 0, line)
    #     curses.napms(10)
    pt_last_row = display_cipher(scr, cipher)
    scr.refresh()
    curses.echo()
    scroll_home = pt_last_row + 3
    #
    # Scrollable window for user input
    swin_rows = lastrow - scroll_home
    swin_lastrow = swin_rows - 1
    swin = curses.newwin(swin_rows, maxcols, scroll_home, 0)
    swin.scrollok(True)

    while True:
        swin.scroll(0)
        swin.move(swin_lastrow, 0)
        # swin.refresh()
        # swin.clrtoeol()
        instr = swin.getstr().decode()
        trace(1, f'{instr=}')
        if len(instr) == 2:
            update_mapping(*instr)
            display_cipher(scr, cipher)
        else:
            swin.addstr(swin_lastrow, 0, 'Input two characters, CT and PT.')
        scr.refresh()
        curses.napms(50)
        # swin.addstr(swin_lastrow, 2, f'{len(instr)=} {instr=}')
        # swin.scroll(1)
        # swin.addstr(swin_lastrow, 2, f'{xl=}')
        if instr.startswith('Q'):
            break



if __name__ == '__main__':
    assert sys.version_info >= (3, 14)
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    _args = getargs(sys.argv)
    logfile = open(_args.log, 'w') if _args.log else None
    au_set = set(ascii_uppercase)
    xl = {a: NOPT for a in ascii_uppercase}  # translate table (c -> p)
    rxl = {a: NOPT for a in ascii_uppercase}  # reverse translate table (p -> c)
    instr = ''
    command = ''
    if _args.test:
        test()
    else:
        curses.wrapper(main)
