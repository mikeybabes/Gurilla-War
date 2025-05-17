REM Gurilla War was a little different from Ikai Warriors and other from same hardware share almost all the layout of image.


REM Make the graphics for BG
copy /b 18.8x+19.8z+gw20.8aa+21.8ac bg-origin.bin

python .\python\reversebyte.py bg-origin.bin
python .\python\rotate90.py reverse_bg-origin.bin rotated_bg.original.bin 16 16
python .\python\reversebyte.py rotated_bg.original.bin
python .\python\swapnybbles.py reverse_rotated_bg.original.bin

REM All 2x2 Tiles
python .\python\savebit.py 2.6g tiles2x2.bin 2080 5000
REM All 8x8 map chunks
python .\python\savebit.py 2.6g all-game-map.bin 9080 f10

REM Get first tile blocks to see if are correct
python .\python\savebit.py 2.6g tileblocks.bin 7080 800

REM Get all tile blocks to see if are correct
python .\python\savebit.py 2.6g Tile_maps-7080.bin 7080 2000

REM Get game mega tile map. very small because the tiles are giant size
python .\python\savebit.py 2.6g complete_maps.bin 9080 100

REM make game palettes
python .\python\make_palette4.py 3.9w 2.9v 1.9u palettes
python .\python\generate_single_palette_grid.py palettes_1.bin palette_1.png
python .\python\generate_single_palette_grid.py palettes_2.bin palette_2.png
python .\python\generate_single_palette_grid.py palettes_3.bin palette_3.png
python .\python\generate_single_palette_grid.py palettes_4.bin palette_4.png

REM Test all tiles output to png
python .\python\tile2x2_plot_test.py swapped_reverse_rotated_bg.original.bin palettes_4.bin tiles2x2.bin all2x2-tiles.png
python .\python\map2x2_plot_number.py swapped_reverse_rotated_bg.original.bin palettes_4.bin tiles2x2.bin tileblocks.bin map2x2_plot.png --debug-blocks
REM Full Map plot for Entire Game
python .\python\mastermap_plot2.py swapped_reverse_rotated_bg.original.bin Palettes_4.bin tiles2x2.bin Tile_maps-7080.bin complete_maps.bin allgame-map.png