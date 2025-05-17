import sys

def prom_to_rgb(val):
    bit0 = (val >> 0) & 1
    bit1 = (val >> 1) & 1
    bit2 = (val >> 2) & 1
    bit3 = (val >> 3) & 1
    return 0x0e * bit0 + 0x1f * bit1 + 0x43 * bit2 + 0x8f * bit3

def main():
    if len(sys.argv) != 5:
        print("Usage: python make_palette.py r.bin g.bin b.bin output_prefix")
        sys.exit(1)

    r_file, g_file, b_file, out_prefix = sys.argv[1:]

    try:
        with open(r_file, "rb") as rf, open(g_file, "rb") as gf, open(b_file, "rb") as bf:
            r_data = rf.read()
            g_data = gf.read()
            b_data = bf.read()

        if not (len(r_data) == len(g_data) == len(b_data) == 1024):
            raise ValueError("Each PROM file must be exactly 1024 bytes.")

        # Create 4 output files of 256 colors each (64 palettes × 16 colors)
        outputs = [bytearray() for _ in range(4)]

        for i in range(1024):
            r = prom_to_rgb(r_data[i])
            g = prom_to_rgb(g_data[i])
            b = prom_to_rgb(b_data[i])

            file_index = i // 256  # 256 colors per file
            outputs[file_index].extend([r, g, b])

        for idx, buf in enumerate(outputs, 1):
            filename = f"{out_prefix}_{idx}.bin"
            with open(filename, "wb") as f:
                f.write(buf)
            print(f"Wrote: {filename} ({len(buf)} bytes)")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
