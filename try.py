import argparse
import curses
from string import ascii_uppercase
import sys

HEADER_LEN = 3

def getparser() -> argparse.ArgumentParser:
    """
    Called either by getargs() in this file or by Sphinx.
    :return: an argparse.ArgumentParser object
    """
    parser = argparse.ArgumentParser(description='''
    ''')
    parser.add_argument('-i', '--infile')
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


def main(scr):
    maxrows, maxcols = scr.getmaxyx()
    lastrow = maxrows - 1
    lastcol = maxcols - 1
    scr.addstr(lastrow, 0, f'Hello World, {lastrow=}, {lastcol=}')
    cipher = read_cipher()
    row_one =  '  ' + '  '.join([char for char in ascii_uppercase[:26]])
    scr.addstr(0, 0, row_one)
    for row, line in enumerate(cipher):
        pt_last_row = row * 3 + HEADER_LEN  # last row of plaintext
        scr.addstr(pt_last_row, 0, line)
    # scr.refresh()
    curses.echo()
    scroll_home = pt_last_row + 2
    while True:
        scr.move(lastrow, 0)
        scr.clrtoeol()
        ch = scr.getch()
        scr.addstr(lastrow - 1, 0, f'{ch=}')
        if ch == ord('X'):
            break

    curses.napms(500)

if __name__ == '__main__':
    assert sys.version_info >= (3, 14)
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    _args = getargs(sys.argv)
    xl = [' ' for n in range(26)]  # translate table (c -> p)
    rxl = [' ' for n in range(26)]  # reverse translate table (p -> c)


    curses.wrapper(main)
