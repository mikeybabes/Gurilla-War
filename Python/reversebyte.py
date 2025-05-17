import sys
import os

def reverse_byte(b):
    return int('{:08b}'.format(b)[::-1], 2)

def main():
    if len(sys.argv) != 2:
        print("Usage: python reversebyte.py input.bin")
        return

    input_filename = sys.argv[1]
    output_filename = "reverse_" + os.path.basename(input_filename)

    with open(input_filename, 'rb') as f:
        data = f.read()

    reversed_data = bytearray(reverse_byte(b) for b in data)

    with open(output_filename, 'wb') as f:
        f.write(reversed_data)

    print(f"Reversed file saved as: {output_filename}")

if __name__ == "__main__":
    main()
