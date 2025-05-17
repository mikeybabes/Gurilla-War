
update_scrool:                          ; CODE XREF: ROM:loc_120↑p
                ld      a, (byte_E48E+1)
                ld      e, a            ; maybe level number!
                ld      d, 0
                ld      hl, SCROLL_OFFSETS_START ; The Y-position scroll values for each level position initial value
                add     hl, de          ; Add offset table values
                ld      e, (hl)         ; Get low byte
                inc     hl
                ld      d, (hl)         ; Get High byte
                ex      de, hl
                ld      (WORLD_YPOSITION_BOTTOM), hl ; Save pointer
                ld      l, h
                ld      h, 0
                add     hl, hl
                add     hl, hl
                ld      de,  byte_907E+2 ; $9080 All level maps start
                add     hl, de
                ld      (MAP_MEMORY), hl ; Get our starting positions
                call    GET_POINTERS
                ld      a, (byte_E48E+1)
                rlca
                ld      e, a
                ld      d, 0
                ld      hl, screen_memory_table ; Screen memory
                add     hl, de
                ld      e, (hl)
                inc     hl
                ld      d, (hl)
                ld      (TILE_SCREEN_MEMORY), de
                inc     hl
                ld      e, (hl)
                inc     hl
                ld      d, (hl)
                ld      hl, (TILE_MAP_START)
                add     hl, de
                ld      (TILE_MAP_START), hl
                ld      hl, (TILE_MAP_START_RIGHT)
                add     hl, de
                ld      (TILE_MAP_START_RIGHT), hl
                ret
; End of function sub_AD7

; ---------------------------------------------------------------------------
SCROLL_OFFSETS_START:dw 0               ; DATA XREF: sub_AD7+6↑o
                                        ; The Y-position scroll values for each level position initial value
                dw 0E20h
                dw 1A20h
                dw 2820h
                dw 3520h
screen_memory_table:dw 0D000h           ; DATA XREF: sub_AD7+27↑o
                                        ; Screen memory
                dw 0
                dw 0D080h
                dw 8
                dw 0D080h
                dw 8
                dw 0D080h
                dw 8
                dw 0D480h
                dw 8

; =============== S U B R O U T I N E =======================================


SCROLL_SCREEN_UPDATER:                  ; CODE XREF: sub_38+64↑p
                ld      hl, (WORLD_YPOSITION)
                ld      bc, 1A0h        ; 416 difference between display and to plot
                add     hl, bc          ; Add to y offset
                ld      de, (WORLD_YPOSITION_BOTTOM)
                or      a
                sbc     hl, de          ; check if data to plot into tile memory
                ret     c
                ld      hl, 20h ; ' '   ; add 32 to screen pointer
                add     hl, de
                ld      (WORLD_YPOSITION_BOTTOM), hl
                ld      iy, (TILE_SCREEN_MEMORY) ; Tile Screen Memory Pointer
                ld      hl, (TILE_MAP_START) ; Table data numbers
                ld      ix, (TILES_BLOCK_START) ; 5 table entry data set
                call    plot_2x2_tile   ; plot first strip across
                ld      (TILE_MAP_START), hl ; save the pointer to tile map
                ld      hl, (TILE_MAP_START_RIGHT) ; Right screen tile data
                ld      ix, (TILES_BLOCK_START_RIGHT) ; 2nd screen data table memory
                call    plot_2x2_tile   ; plot another 8 2x2 tiles
                ld      (TILE_MAP_START_RIGHT), hl
                ld      a, l
                ld      hl, (TILE_SCREEN_MEMORY)
                ld      bc, 80h         ; Advance pointer two rows as 64bytes / screen
                add     hl, bc
                res     3, h
                ld      (TILE_SCREEN_MEMORY), hl ; save new value
                and     3Fh			; Every 64th plot update pointers
                ret     nz
                ld      hl, (MAP_MEMORY)

GET_POINTERS:                           ; CODE XREF: sub_AD7+1D↑p
                call    CALC_TILE_BLOCK_MEM
                ld      (TILE_MAP_START), bc ; Save pointer
                ld      (TILES_BLOCK_START), de ; save pointer
                call    CALC_TILE_BLOCK_MEM
                ld      (TILE_MAP_START_RIGHT), bc
                ld      (TILES_BLOCK_START_RIGHT), de
                ld      (MAP_MEMORY), hl ; Save map memory pointer
                ret
; End of function SCROLL_SCREEN_UPDATER


; =============== S U B R O U T I N E =======================================


CALC_TILE_BLOCK_MEM:                    ; CODE XREF: SCROLL_SCREEN_UPDATER:GET_POINTERS↑p
                                        ; SCROLL_SCREEN_UPDATER+52↑p
                ld      d, (hl)
                inc     hl              ; Get first byte and advance pointer
                ld      b, (hl)
                inc     hl              ; 2nd byte for right size offset chunk
                push    hl
                ld      c, 0
                srl     b               ; Multiply * 64 for offset
                rr      c
                srl     b
                rr      c
                ld      hl, 7080h       ; offset * 64 + base
                add     hl, bc
                push    hl
                pop     bc
                ld      e, 0            ; clear high
                ld      hl, TILES       ; Tiles start $2080
                add     hl, de          ; Add first byte + offset 2080
                ex      de, hl
                pop     hl
                ret
; End of function CALC_TILE_BLOCK_MEM

; =============== S U B R O U T I N E =======================================

; 8 2x2 tiles / screen row
; IX is current tile pointer base
; HL is map memory pointer

plot_2x2_tile:                          ; CODE XREF: SCROLL_SCREEN_UPDATER+21↑p
                                        ; SCROLL_SCREEN_UPDATER+2E↑p
                ld      b, 8

tile_loop:                              ; CODE XREF: plot_2x2_tile+41↓j
                push    bc              ; save row count
                push    ix              ; take original tiles base pointer copy to stack
                ld      e, (hl)         ; get tile number table
                ld      d, 0            ; make de 16 bit so only 0 - 255 tiles
                ex      de, hl          ; swap = save current hl
                ld      c, l
                ld      b, h            ; value into temp of bc for add in a minute
                add     hl, hl          ; tile number * 2
                add     hl, hl          ; tile number * 4
                add     hl, bc          ; and finally tile number * 5
                ex      de, hl          ; put the offset into de
                add     ix, de          ; now add offset into base
                ld      c, (ix+4)       ; c holds the msb which is same for all characters, 5th byte
                ld      a, (ix+sub_0)   ; Get lsb for screen character, bottom left one first
                ld      (iy+0), a       ; save to screen data
                ld      (iy+1), c       ; Save to screen tile data
                ld      a, (ix+1)       ; get tile offset 2nd byte
                ld      (iy+2), a       ; bottom right character
                ld      (iy+3), c       ; bottom right colour and high byte
                ld      a, (ix+2)       ; get tile offset 3rd byte
                ld      (iy+40h), a     ; tile screen top left above 1st
                ld      (iy+41h), c     ; msb + colour for above
                ld      a, (ix+3)       ; last of the 2x2 tile top right lsb
                ld      (iy+42h), a     ; lsb tile number
                ld      (iy+43h), c     ; msb and colour as per rest
                inc     hl              ; increase tile map source pointer
                ld      bc, 4           ; advance screen address to 2 characters (4 bytes)
                add     iy, bc          ; screen memory pointer advance
                pop     ix              ; return back tile base
                pop     bc              ; bc was initial count which would be a single complete row
                djnz    tile_loop       ; advance to next tile
                ret
; End of function plot_2x2_tile
