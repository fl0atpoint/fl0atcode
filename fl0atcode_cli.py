def encode(text: str, dots: bool = False) -> str:
    out = []

    for ch in text.lower():
        if ch == ' ':
            out.append(' ')
        elif ch in ENCODE_MAP:
            out.append(ENCODE_MAP[ch])
            if dots:
                out.append('.')
        else:
            out.append(ch)

    if dots:
        return ''.join(out).replace('. ', ' ')
    return ''.join(out)


def decode(text: str) -> str:
    i = 0
    out = []

    while i < len(text):
        if text[i] == ' ':
            out.append(' ')
            i += 1
            continue

        # optional separators
        if text[i] == '.':
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
            out.append(text[i])
            i += 1

    return ''.join(out)


def auto_detect(text: str) -> str:
    """
    Guess whether the input is fl0atcode or plain English.
    """

    encoded_chars = set("~^!*+@#$%&-=|/.")

    english = sum(c.isalpha() for c in text)
    encoded = sum(c in encoded_chars for c in text)

    return "decode" if encoded > english else "encode"


def main():
    parser = argparse.ArgumentParser(
        description="fl0atcode cli\n\nturns readable text into unreadable text... and back again.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "mode",
        nargs="?",
        choices=["encode", "decode"],
        help="force encode or decode (optional)",
    )

    parser.add_argument(
        "text",
        nargs="*",
        help="text to process (reads stdin if omitted)",
    )

    parser.add_argument(
        "-d",
        "--dots",
        action="store_true",
        help="insert optional '.' separators while encoding",
    )

    args = parser.parse_args()

    if args.text:
        text = " ".join(args.text)
    else:
        text = sys.stdin.read().rstrip("\n")

    mode = args.mode or auto_detect(text)

    if mode == "encode":
        print(encode(text, dots=args.dots))
    else:
        print(decode(text))


if __name__ == "__main__":
    main()
