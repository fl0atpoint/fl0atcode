#!/usr/bin/env python3
# Uses the MIT license; https://github.com/fl0atpoint/fl0atcode/blob/main/LICENSE

import sys
import argparse

# fl0atcode (lite) mapping
ENCODE_MAP = {
    # vowels
    'a': '~',
    'e': '^',
    'i': '!',
    'o': '*',
    'u': '+',

    # consonants
    'b': '@',
    'c': '#',
    'd': '$',
    'f': '%',
    'g': '&',
    'h': '-',
    'j': '=',
    'k': '|',
    'l': '/',

    'm': '@@',
    'n': '##',
    'p': '$$',
    'q': '%%',
    'r': '&&',
    's': '--',
    't': '==',
    'v': '||',
    'w': '//',
    'x': '@#',
    'y': '$%',
    'z': '&*',

    # punctuation
    '.': '|||',
    ',': '///',
}

# build decode map (longest tokens first)
DECODE_MAP = {v: k for k, v in ENCODE_MAP.items()}
TOKENS = sorted(DECODE_MAP.keys(), key=len, reverse=True)


def encode(text: str) -> str:
    out = []
    for ch in text.lower():
        if ch == ' ':
            out.append(' ')
        elif ch in ENCODE_MAP:
            out.append(ENCODE_MAP[ch])
        else:
            # passthrough for unknown chars
            out.append(ch)
    return ''.join(out)


def decode(text: str) -> str:
    i = 0
    out = []
    while i < len(text):
        if text[i] == ' ':
            out.append(' ')
            i += 1
            continue

        matched = False
        for token in TOKENS:
            if text.startswith(token, i):
                out.append(DECODE_MAP[token])
                i += len(token)
                matched = True
                break

        if not matched:
            # unknown symbol, just copy it
            out.append(text[i])
            i += 1

    return ''.join(out)


def main():
    parser = argparse.ArgumentParser(
        description='fl0atcode cli - remaking the alphabet to make it look like spammed text(tm)'
    )
    parser.add_argument(
        'mode',
        choices=['encode', 'decode'],
        help='encode english to fl0atcode or decode it back'
    )
    parser.add_argument(
        'text',
        nargs='*',
        help='text to process (reads stdin if omitted)'
    )

    args = parser.parse_args()

    if args.text:
        text = ' '.join(args.text)
    else:
        text = sys.stdin.read().rstrip('\n')

    if args.mode == 'encode':
        print(encode(text))
    else:
        print(decode(text))


if __name__ == '__main__':
    main()
