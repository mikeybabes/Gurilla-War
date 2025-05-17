import sys
from PIL import Image, ImageDraw, ImageFont

TILE_WIDTH = 16
TILE_HEIGHT = 16
BLOCK_SIZE = 32  # 2x2 tile block = 32x32 pixels
BYTES_PER_TILE = 128
TILES_PER_ROW = 8  # map tiles per row

def load_palette(palette_file):
    palette = []
    with open(palette_file, 'rb') as f:
        data = f.read()
        for i in range(0, len(data), 3):
            palette.append((data[i], data[i+1], data[i+2]))
    return palette

def load_tiles(tiles_file):
    with open(tiles_file, 'rb') as f:
        return f.read()

def load_tile2x2(file_path):
    entries = []
    with open(file_path, 'rb') as f:
        data = f.read()
    for i in range(0, len(data), 5):
        if i + 5 > len(data):
            break
        b0, b1, b2, b3, hi = data[i:i+5]
        bl = b0 | (hi << 8)
        br = b1 | (hi << 8)
        tl = b2 | (hi << 8)
        tr = b3 | (hi << 8)
        entries.append((tl, tr, bl, br, hi))
    return entries

def load_map(file_path):
    with open(file_path, 'rb') as f:
        return list(f.read())

def plot_tile(pixels, tile_data, palette, palette_index, x_pos, y_pos):
    for y in range(TILE_HEIGHT):
        for x in range(0, TILE_WIDTH, 2):
            byte_index = (y * TILE_WIDTH + x) // 2
            byte = tile_data[byte_index]
            pixel1 = (byte & 0xF0) >> 4
            pixel2 = byte & 0x0F
            color1 = palette[(palette_index * 16) + pixel1]
            color2 = palette[(palette_index * 16) + pixel2]
            pixels[x_pos + x, y_pos + y] = color1
            pixels[x_pos + x + 1, y_pos + y] = color2

def draw_block_number(draw, label, x_base, y_base, font):
    lines = label.split('\n')
    line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
    y = y_base + 128 - (len(lines) * line_height) // 2
    for line in lines:
        text_width = font.getbbox(line)[2]
        cx = x_base + 128 - text_width // 2
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            draw.text((cx+dx, y+dy), line, font=font, fill="black")
        draw.text((cx, y), line, font=font, fill="white")
        y += line_height

def main():
    args = sys.argv[1:]
    debug_blocks = False
    if "--debug-blocks" in args:
        debug_blocks = True
        args.remove("--debug-blocks")

    if len(args) != 5:
        print("Usage: python map2x2_plot.py tilegraphic.bin palette.bin tile2x2.bin map.bin output.png [--debug-blocks]")
        return

    tiles_file, palette_file, tile2x2_file, map_file, output_file = args

    tiles_data = load_tiles(tiles_file)
    palette = load_palette(palette_file)
    tile_blocks = load_tile2x2(tile2x2_file)
    map_data = load_map(map_file)

    total_rows = len(map_data) // TILES_PER_ROW
    img_width = TILES_PER_ROW * BLOCK_SIZE
    img_height = total_rows * BLOCK_SIZE

    img = Image.new('RGB', (img_width, img_height))
    pixels = img.load()
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for i, map_index in enumerate(map_data):
        if map_index >= len(tile_blocks):
            print(f"Map index {map_index} out of range at position {i}")
            continue

        col = i % TILES_PER_ROW
        row = i // TILES_PER_ROW
        x_base = col * BLOCK_SIZE
        y_base = (total_rows - 1 - row) * BLOCK_SIZE  # bottom-to-top

        tl_word, tr_word, bl_word, br_word, hi = tile_blocks[map_index]
        palette_index = (hi >> 4) & 0x0F

        for word, dx, dy in [
            (tl_word, 0, 0),
            (tr_word, 16, 0),
            (bl_word, 0, 16),
            (br_word, 16, 16),
        ]:
            tile_index = word & 0x07FF
            tile_offset = tile_index * BYTES_PER_TILE
            if tile_offset + BYTES_PER_TILE > len(tiles_data):
                print(f"Tile index {tile_index} out of range at map tile {i}")
                continue
            tile_data = tiles_data[tile_offset:tile_offset + BYTES_PER_TILE]
            plot_tile(pixels, tile_data, palette, palette_index, x_base + dx, y_base + dy)

        if debug_blocks and i % 64 == 0:
            block_index = (i // 64) - 1
            chunk_offset = i - 64
            if i == 0:
                block_index = 0
                chunk_offset = 0
            label = f"Block {block_index}\n@ ${chunk_offset:04X}"
            draw_block_number(draw, label, x_base, y_base, font)

    img.save(output_file)
    print(f"✅ Map image saved to {output_file}")

if __name__ == "__main__":
    main()
