import sys
from PIL import Image, ImageDraw, ImageFont

TILE_WIDTH = 16
TILE_HEIGHT = 16
BLOCK_SIZE = 32
SUPERTILE_SIZE = 8
BYTES_PER_TILE = 128
BYTES_PER_TILE2X2_ENTRY = 5

def load_palette(palette_file):
    palette = []
    with open(palette_file, 'rb') as f:
        data = f.read()
        for i in range(0, len(data), 3):
            palette.append((data[i], data[i+1], data[i+2]))
    return palette

def load_tiles(filename):
    with open(filename, 'rb') as f:
        return f.read()

def load_tile2x2(filename):
    entries = []
    with open(filename, 'rb') as f:
        data = f.read()
    for i in range(0, len(data), BYTES_PER_TILE2X2_ENTRY):
        if i + 5 > len(data):
            break
        b0, b1, b2, b3, hi = data[i:i+5]
        bl = b0 | (hi << 8)
        br = b1 | (hi << 8)
        tl = b2 | (hi << 8)
        tr = b3 | (hi << 8)
        entries.append((tl, tr, bl, br, hi))
    return entries

def load_map(filename):
    with open(filename, 'rb') as f:
        return list(f.read())

def load_master_map(filename):
    entries = []
    with open(filename, 'rb') as f:
        data = f.read()
    for i in range(0, len(data), 4):
        left_hi = data[i]
        left_chunk = data[i+1]
        right_hi = data[i+2]
        right_chunk = data[i+3]
        entries.append((left_hi, left_chunk))   # LEFT
        entries.append((right_hi, right_chunk)) # RIGHT
    return entries

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

def plot_supertile(pixels, tiles_data, tile_blocks, palette, map_data,
                   tile2x2_base_offset, map_chunk_offset, x_base, y_base):
    for tile_row in range(SUPERTILE_SIZE):
        for tile_col in range(SUPERTILE_SIZE):
            map_index = map_data[map_chunk_offset + tile_row * SUPERTILE_SIZE + tile_col]
            base_index = tile2x2_base_offset // 5  # ✅ Fix: convert byte offset to entry index
            absolute_index = base_index + map_index

            if absolute_index >= len(tile_blocks):
                print(f"❌ tile2x2 index ${absolute_index:04X} out of range")
                continue

            tl_word, tr_word, bl_word, br_word, hi = tile_blocks[absolute_index]
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
                    print(f"❌ Tile index ${tile_index:04X} out of range")
                    continue
                tile_data = tiles_data[tile_offset:tile_offset + BYTES_PER_TILE]
                final_x = x_base + tile_col * BLOCK_SIZE + dx
                final_y = y_base + (SUPERTILE_SIZE - 1 - tile_row) * BLOCK_SIZE + dy
                plot_tile(pixels, tile_data, palette, palette_index, final_x, final_y)

def draw_label(draw, x, y, label, font):
    lines = label.split('\n')
    line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
    y -= (len(lines) * line_height) // 2
    for line in lines:
        text_width = font.getbbox(line)[2]
        cx = x - text_width // 2
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            draw.text((cx+dx, y+dy), line, fill="black", font=font)
        draw.text((cx, y), line, fill="white", font=font)
        y += line_height

def main():
    if len(sys.argv) != 7:
        print("Usage: python mastermap_plot2.py tilegraphic.bin palette.bin tile2x2.bin map.bin master-map.bin output.png")
        return

    tiles_file     = sys.argv[1]
    palette_file   = sys.argv[2]
    tile2x2_file   = sys.argv[3]
    map_file       = sys.argv[4]
    mastermap_file = sys.argv[5]
    output_file    = sys.argv[6]

    tiles_data = load_tiles(tiles_file)
    palette = load_palette(palette_file)
    tile_blocks = load_tile2x2(tile2x2_file)
    map_data = load_map(map_file)
    master_entries = load_master_map(mastermap_file)

    num_supertiles = len(master_entries)
    num_rows = num_supertiles // 2
    img_width = 512
    img_height = num_rows * 256

    img = Image.new("RGB", (img_width, img_height))
    pixels = img.load()
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for row in range(num_rows):
        for side in range(2):
            entry_index = row * 2 + side
            hi_byte, chunk_index = master_entries[entry_index]
            tile2x2_base_offset = hi_byte << 8
            map_chunk_offset = chunk_index * 64
            x_base = side * 256
            y_base = (num_rows - 1 - row) * 256
            side_label = "LEFT" if side == 0 else "RIGHT"

            # ✅ Expanded debug
            print(
                f"Row {row:02} - {side_label} entry {entry_index:03}: "
                f"tile2x2 offset=${tile2x2_base_offset:04X}, "
                f"map chunk={chunk_index:02X} "
                f"(offset={map_chunk_offset} / ${map_chunk_offset:04X})"
            )

            label = f"${tile2x2_base_offset:04X}\n#{chunk_index:02X}"
            draw_label(draw, x_base + 128, y_base + 128, label, font)

            plot_supertile(pixels, tiles_data, tile_blocks, palette,
                           map_data, tile2x2_base_offset, map_chunk_offset,
                           x_base, y_base)

    img.save(output_file)
    print(f"✅ Map image saved to {output_file}")

if __name__ == "__main__":
    main()
