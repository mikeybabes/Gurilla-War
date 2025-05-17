import sys

def extract_bitplanes(tile_bytes, size):
    bitplanes = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(4)]
    for y in range(size):
        for x in range(0, size, 2):
            i = (y * size + x) // 2
            byte = tile_bytes[i]
            p0 = (byte >> 4) & 0xF
            p1 = byte & 0xF
            for b in range(4):
                bitplanes[b][y][x] = (p0 >> b) & 1
                bitplanes[b][y][x+1] = (p1 >> b) & 1
    return bitplanes

def rotate_anticlockwise(plane):
    size = len(plane)
    return [[plane[x][size - 1 - y] for x in range(size)] for y in range(size)]

def merge_bitplanes(bitplanes, size):
    out = bytearray((size * size) // 2)
    for y in range(size):
        for x in range(0, size, 2):
            p0 = sum((bitplanes[b][y][x] << b) for b in range(4))
            p1 = sum((bitplanes[b][y][x+1] << b) for b in range(4))
            out[(y * size + x) // 2] = (p0 << 4) | p1
    return out

def rotate_tile(tile_bytes, size):
    planes = extract_bitplanes(tile_bytes, size)
    rotated_planes = [rotate_anticlockwise(plane) for plane in planes]
    return merge_bitplanes(rotated_planes, size)

def main():
    if len(sys.argv) != 5:
        print("Usage: python rotate90.py input.bin output.bin 8 8|16 16")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    size = int(sys.argv[3])
    if size != int(sys.argv[4]) or size not in (8, 16):
        print("Only square tiles of size 8 or 16 supported.")
        return

    bytes_per_tile = (size * size) // 2

    with open(input_file, "rb") as f:
        data = f.read()

    output = bytearray()
    for i in range(0, len(data), bytes_per_tile):
        tile = data[i:i+bytes_per_tile]
        if len(tile) < bytes_per_tile:
            break
        rotated = rotate_tile(tile, size)
        output.extend(rotated)

    with open(output_file, "wb") as f:
        f.write(output)

if __name__ == "__main__":
    main()
