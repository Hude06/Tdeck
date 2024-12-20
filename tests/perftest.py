import board
import displayio

from helper import TDeck

from adafruit_display_text import label
import terminalio

import time
import board, busio
import displayio
import vectorio
import math

# SPEED = 1_000_000 # 1.38s/f  6.9/10
# SPEED = 2_000_000 # 0.82s/f  4.2/10
# SPEED = 3_000_000 # 0.63s/f  3.2/10
# SPEED = 5_000_000 # 0.48s/f  2.5/10 = 4fps
# SPEED = 10_000_000 # 0.38s/f  1.97/10  = 5fps
# SPEED = 15_000_000 # 0.34  1.79/10
# SPEED = 20_000_000 # 0.325s/f  1.7s / 10
# SPEED = 48_000_000 # 1.523/10
# SPEED = 100_000_000 # 1.44s / 10
# SPEED = 200_000_000 # 1.44s / 10
SPEED = 64_000_000 # 1.53/10
# SPEED = 99_000_000
# setup the display
# displayio.release_displays()
# spi = busio.SPI(clock=board.LCD_CLK, MOSI=board.LCD_DIN)
# LCD_RST is 12 in the regular, but 13 for the touch version
# display_bus = displayio.FourWire(spi, command=board.LCD_DC,
#                                  chip_select=board.LCD_CS,reset=board.GP13, baudrate=SPEED)
# display = gc9a01.GC9A01(display_bus, width=240, height=240,
#                         backlight_pin=board.LCD_BL, rotation=0, auto_refresh=False)

tdeck = TDeck()
display = board.DISPLAY

main = displayio.Group()

bgpal = displayio.Palette(8)
bgpal[0] = 0xFF0000
bgpal[1] = 0x00FF00
bgpal[2] = 0x0000FF
bgpal[3] = 0xFFFFFF
bgpal[4] = 0xFF0000
bgpal[5] = 0x00FF00
bgpal[6] = 0x0000FF
bgpal[7] = 0xFFFFFF

# bgbit = displayio.Bitmap(60,60,len(bgpal))
# bgbit.fill(0)
# bg_tile_grid = displayio.TileGrid(bgbit, pixel_shader=bgpal)
# bg_tile_grid.x = 120-30
# bg_tile_grid.y = 120-30
# main.append(bg_tile_grid)

last_time = time.monotonic()

cx = int(display.width / 2)
cy = int(display.height / 2)

circles = []
# for n in range(len(bgpal)):
for n in range(1):
    ang = (n*45)*(math.pi/180)
    x = int(math.sin(ang) * 20)
    y = int(math.cos(ang) * 20)
    circle = vectorio.Circle(pixel_shader=bgpal, radius=10, x=cx+x, y=cy+y)
    circle.color_index = n
    main.append(circle)
    circles.append(circle)

count = 0

radius = 70.0
def position():
    for n in range(len(circles)):
        ang = (n*10+count*2.3)*(math.pi/180.0)
        x = int(math.sin(ang) * (radius * math.sin(ang/10)))
        y = int(math.cos(ang) * (radius* math.sin(ang/10)))
        circles[n].x = cx+x
        circles[n].y = cy+y


# display.show(main)
display.root_group = main

fps = label.Label(terminalio.FONT, text="hi there", x=10, y= 30)
main.append(fps)

prev = time.monotonic()
prev_count = 0
while True:
    count = count + 1
    position()
    # 4 sec to do 60 frames = 15/fps or 60/4
    now = time.monotonic()
    # print(now)
    if (count % 60) == 0:
        diff = now - last_time
        # print('60 diff',diff, 60/diff)
        last_time = now
    # display.refresh(target_frames_per_second=20)
    display.refresh()

    if now - prev > 1:
        print("fps", (count-prev_count)/(now-prev))
        fps.text = f"circles: {len(circles)} fps: {(count-prev_count)/(now-prev)}"
        prev = now
        prev_count = count
        new_circle = vectorio.Circle(pixel_shader=bgpal, radius=10)
        main.append(new_circle)
        circles.append(new_circle)



