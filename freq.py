"""

"""
from collections import defaultdict
import string
import sys

ord_uca = ord('A')
LETTERS_UC = set(string.ascii_uppercase)


def index_of_coincidence(tally):
    total = 0
    numerator = 0
    for chr in LETTERS_UC:
        count = tally[chr]
        if count > 1:
            numerator += count * (count - 1)
        total += count
    ic = numerator / (total * (total - 1))
    print(f'IC = {ic:6.3}')

def main():
    cipherfile = open(sys.argv[1])
    cipher = cipherfile.read()
    print(cipher)
    tally = defaultdict(int)
    # print(tally)
    for ch in cipher:
        if ch.isalpha():
            tally[ch.upper()] += 1
    print(sorted(tally.items(), key=lambda item: item[1], reverse=True))

    # print only uppercase letters
    # outs = []
    # for ch in cipher:
    #     if not ch.isalpha() or ch == ch.upper():
    #         outs.append(ch)
    # print(''.join(outs))

    index_of_coincidence(tally)

if __name__ == '__main__':
    main()
