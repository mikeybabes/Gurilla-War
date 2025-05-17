import sys
import os

def split_file(input_file, output_file, chunk_size, offset=0, quantity=None):
    try:
        with open(input_file, 'rb') as f:
            f.seek(offset)
            chunk_number = 1
            while quantity is None or chunk_number <= quantity:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                chunk_filename = f"{os.path.splitext(output_file)[0]}_{chunk_number}{os.path.splitext(output_file)[1]}"
                with open(chunk_filename, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                chunk_number += 1
        print(f"File split into {chunk_number - 1} chunks.")
    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 6:
        print("Usage: python splitchunks.py input.bin output.pal chunk_size [offset] [quantity]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        chunk_size = int(sys.argv[3])
    except ValueError:
        print("Chunk size must be an integer.")
        sys.exit(1)

    offset = 0
    if len(sys.argv) > 4:
        try:
            offset = int(sys.argv[4], 16)
        except ValueError:
            print("Offset must be a hexadecimal integer.")
            sys.exit(1)

    quantity = None
    if len(sys.argv) > 5:
        try:
            quantity = int(sys.argv[5])
        except ValueError:
            print("Quantity must be an integer.")
            sys.exit(1)
    
    split_file(input_file, output_file, chunk_size, offset, quantity)
