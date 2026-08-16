import argparse
import sys

from colorama import Fore, Style

english_frequences = [ 0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228,
    0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406,
    0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056,
    0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074, ]


if __name__ == "__main__":
    orda = ord("A")
    ef = [(chr(n + orda), f) for n, f in enumerate(english_frequences)]
    ef.sort(key=lambda x: x[1], reverse=True)
    # print('\n'.join('{} {:8.5f}'.format(*k) for k in ef))
    print('\n'.join(f'{c} {f:8.5f}' for c, f in ef))
    # for char, freq in ef:
    #     print(f"{char} {freq:8.5f}")
