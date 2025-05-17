import sys
from PIL import Image, ImageDraw

TILE_WIDTH = 16
TILE_HEIGHT = 16
BLOCK_SIZE = 32
BYTES_PER_TILE = 128
TILE2X2_ENTRY_SIZE = 5
TILES_PER_ROW = 16

def load_palette(palette_file):
    with open(palette_file, 'rb') as f:
        data = f.read()
    palette = [(data[i], data[i+1], data[i+2]) for i in range(0, len(data), 3)]
    return palette

def load_tiles(tile_file):
    with open(tile_file, 'rb') as f:
        return f.read()

def load_tile2x2(tile2x2_file):
    with open(tile2x2_file, 'rb') as f:
        data = f.read()
    blocks = []
    for i in range(0, len(data), TILE2X2_ENTRY_SIZE):
        if i + 5 > len(data):
            break
        b0, b1, b2, b3, hi = data[i:i+5]
        bl = b0 | (hi << 8)
        br = b1 | (hi << 8)
        tl = b2 | (hi << 8)
        tr = b3 | (hi << 8)
        blocks.append((tl, tr, bl, br, hi))
    return blocks

def plot_tile(pixels, tile_data, palette, palette_index, x_pos, y_pos):
    for y in range(TILE_HEIGHT):
        for x in range(0, TILE_WIDTH, 2):
            byte = tile_data[(y * TILE_WIDTH + x) // 2]
            px1 = (byte & 0xF0) >> 4
            px2 = byte & 0x0F
            color1 = palette[palette_index * 16 + px1]
            color2 = palette[palette_index * 16 + px2]
            pixels[x_pos + x, y_pos + y] = color1
            pixels[x_pos + x + 1, y_pos + y] = color2

def main():
    if len(sys.argv) != 5:
        print("Usage: python tile_plot_test.py tilegraphic.bin palette.bin tiles2x2.bin output.png")
        return

    tile_file, palette_file, tile2x2_file, output_file = sys.argv[1:]
    tiles = load_tiles(tile_file)
    palette = load_palette(palette_file)
    blocks = load_tile2x2(tile2x2_file)

    total = len(blocks)
    rows = (total + TILES_PER_ROW - 1) // TILES_PER_ROW
    img = Image.new("RGB", (TILES_PER_ROW * BLOCK_SIZE, rows * BLOCK_SIZE))
    pixels = img.load()

    for idx, (tl, tr, bl, br, hi) in enumerate(blocks):
        px = (idx % TILES_PER_ROW) * BLOCK_SIZE
        py = (idx // TILES_PER_ROW) * BLOCK_SIZE
        palette_index = (hi >> 4) & 0x0F

        for word, dx, dy in [
            (tl, 0, 0),
            (tr, 16, 0),
            (bl, 0, 16),
            (br, 16, 16),
        ]:
            tile_index = word & 0x07FF
            offset = tile_index * BYTES_PER_TILE
            tile_data = tiles[offset:offset + BYTES_PER_TILE]
            plot_tile(pixels, tile_data, palette, palette_index, px + dx, py + dy)

    img.save(output_file)
    print(f"✅ Saved tile test image to {output_file}")

if __name__ == "__main__":
    main()
