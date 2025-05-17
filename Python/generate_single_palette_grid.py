from PIL import Image, ImageDraw, ImageFont
import os
import sys

def generate_single_grid(input_file, output_file):
    # Read binary palette data
    with open(input_file, "rb") as f:
        data = f.read()

    colors_per_palette = 16
    bytes_per_color = 3
    bytes_per_palette = colors_per_palette * bytes_per_color

    total_palettes = len(data) // bytes_per_palette
    if total_palettes < colors_per_palette:
        print(f"Warning: Expected at least {colors_per_palette} palettes, found {total_palettes}.")
    # Only take first 16 palettes
    palettes = []
    for p in range(colors_per_palette):
        start = p * bytes_per_palette
        palette = []
        for i in range(colors_per_palette):
            offset = start + i * bytes_per_color
            r, g, b = data[offset], data[offset+1], data[offset+2]
            palette.append((r, g, b))
        palettes.append(palette)

    # Image setup: 16x16 grid in a 1920x1920 PNG
    img_size = 1920
    square = img_size // colors_per_palette  # 120 pixels

    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)

    # Font setup (small font for hex numbers)
    try:
        font = ImageFont.truetype("arial.ttf", 36)  # You may need to adjust the font size
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font if Arial is not available

    # Draw the 16x16 grid
    for row in range(colors_per_palette):
        for col in range(colors_per_palette):
            color = palettes[row][col]
            x = col * square
            y = row * square
            draw.rectangle([x, y, x + square, y + square], fill=color)

        # Draw the palette set number (in hex) at the start of each row
        hex_value = f"{row:X}"  # Hexadecimal representation of the set number
        #text_x = 5 + row * square  # Fixed x position at the start of the row (just inside the box)
        text_x = 42  # Fixed x position at the start of each block (just inside the box)
        text_y = 42 + row * square  # Fixed y position just inside the box
        draw.text((text_x, text_y), hex_value, fill="white", font=font)

    # Save the single PNG
    img.save(output_file)
    print(f"Generated grid saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_single_palette_grid.py <input_file> <output_file>")
        sys.exit(1)
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    generate_single_grid(in_file, out_file)
