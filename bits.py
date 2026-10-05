"""Fixed-width integer exploration, using only Python's standard library."""

def decode(value, width):
    if not 2 <= width <= 16:
        raise ValueError("Width must be 2 through 16 bits.")
    if not 0 <= value < 2 ** width:
        raise ValueError("Value does not fit the unsigned width.")
    signed = value - 2 ** width if value >= 2 ** (width - 1) else value
    return {"binary": format(value, f"0{width}b"), "hex": hex(value),
            "unsigned": value, "signed": signed}


def addition(a, b, width):
    first, second = decode(a, width), decode(b, width)
    total = a + b
    wrapped = total % (2 ** width)
    signed_total = first["signed"] + second["signed"]
    minimum, maximum = -(2 ** (width - 1)), 2 ** (width - 1) - 1
    return {"result": decode(wrapped, width), "unsigned_overflow": total >= 2 ** width,
            "signed_overflow": not minimum <= signed_total <= maximum,
            "unsigned_sum": total, "signed_sum": signed_total}


def parse(text):
    text = text.strip().lower()
    # Plain numbers are decimal; 0b and 0x explicitly select other bases.
    return int(text, 2 if text.startswith("0b") else 16 if text.startswith("0x") else 10)


def encode_signed(number, width):
    decode(0, width)
    minimum, maximum = -(2 ** (width - 1)), 2 ** (width - 1) - 1
    if not minimum <= number <= maximum:
        raise ValueError(f"Signed input must be {minimum} through {maximum}.")
    return decode(number % (2 ** width), width)


def explain(a, b, width):
    result = addition(a, b, width)
    first, second = decode(a, width), decode(b, width)
    lines = [f"Width: {width}; retain only the lowest {width} bits.",
             f"A: {first['binary']} = unsigned {a}, signed {first['signed']}",
             f"B: {second['binary']} = unsigned {b}, signed {second['signed']}",
             f"Unsigned sum: {a} + {b} = {a+b}; maximum {2**width-1}.",
             f"Wrapped result: ({a+b}) modulo {2**width} = {result['result']['unsigned']}.",
             f"Result bits: {result['result']['binary']}.",
             f"Signed sum: {first['signed']} + {second['signed']} = {result['signed_sum']}.",
             f"Signed range: {-2**(width-1)} through {2**(width-1)-1}.",
             f"Unsigned overflow: {result['unsigned_overflow']}; signed overflow: {result['signed_overflow']}."]
    if result['result']['signed'] < 0:
        lines.append(f"Leading bit is 1: signed result = {result['result']['unsigned']} - {2**width} = {result['result']['signed']}.")
    return lines


def report(a, b, width, path):
    from html import escape
    lines = explain(a, b, width)
    rows = ''.join(f"<li>{escape(line)}</li>" for line in lines)
    output = addition(a, b, width)["result"]["binary"]
    weights = [2**i for i in range(width-1, -1, -1)]
    cells = ''.join(f'<td><strong>{bit}</strong><br><small>weight {weight}</small></td>' for bit, weight in zip(output, weights))
    path.write_text(f'<!doctype html><meta charset="utf-8"><title>Bits explained</title><style>body{{font:18px system-ui;max-width:1000px;margin:40px auto;padding:20px;color:#17243b;background:#f1f5fb}}td{{text-align:center;background:white;padding:12px;border:1px solid #ddd}}li{{margin:16px 0}}strong{{font-size:28px}}</style><h1>Fixed-Width Arithmetic Lab</h1><table><tr>{cells}</tr></table><p>Weights above are unsigned. In signed interpretation the leftmost weight is negative.</p><ol>{rows}</ol>', encoding="utf-8")


def main():
    print("BITS EXPLORER: decimal, 0b binary, or 0x hex; negative inputs encode signed values; q to quit")
    while True:
        width_text = input("Width (2-16): ").strip()
        if width_text.lower() == "q":
            return
        try:
            width = int(width_text)
            a = parse(input("First value or pattern: "))
            if a < 0:
                a = encode_signed(a, width)["unsigned"]
            print(decode(a, width))
            other = input("Second pattern for addition (Enter to skip): ")
            if other.strip():
                b = parse(other)
                if b < 0:
                    b = encode_signed(b, width)["unsigned"]
                result = addition(a, b, width)
                for name, value in result.items():
                    print(f"{name}: {value}")
                for line in explain(a, b, width):
                    print(line)
                from pathlib import Path
                path = Path(__file__).with_name("calculation.html")
                report(a, b, width, path)
                print("Open calculation.html for the visual explanation.")
        except ValueError as error:
            print(f"Invalid input: {error}")


if __name__ == "__main__":
    main()
