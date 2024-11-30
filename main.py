"""
  Picontosh: The Pi-Icon-Macintosh....

  Exploring original Macintosh icon resources and turning them into a small desktop display.

  Released under the MIT License (MIT).
  Copyright (c) 2024 Simon Boak, Unimplemented Trap
  http://unimplementedtrap.com/

"""

import time
import gc
from machine import Pin, SPI
from uctypes import bytearray_at, addressof
from st7789 import *
import sdcard
import os
import random
import ChicagoSB_12
import slowdraw
import slowtype

def icon_to_framebuffer(iconData):
  buf = framebuf.FrameBuffer(bytearray(32 * 32 * 2), 32, 32, framebuf.RGB565)
  bytesInLine = 0
  y = 0
  x = 0
  for i in range(len(iconData)):
    pixelByte = iconData[i]

    bitNumber = int(128)
    while bitNumber > 0:
      if pixelByte&bitNumber != 0:
        buf.pixel(x, y, BLACK)

      x = x + 1
      bitNumber = int(bitNumber / 2)

    bytesInLine = bytesInLine + 1
    if bytesInLine == 4:
      y = y + 1
      x = 0
      bytesInLine = 0
  return buf

def draw_boot_screen(slowtyper):
  time.sleep_ms(300)
  # Draw the boot message box
  ssd.fill_rect(50, 30, 220, 75, WHITE)
  ssd.rect(50, 30, 220, 75, BLACK)

  strBuffer, width = slowtyper.buffer_from_str('Starting up...')
  ssd.blit(strBuffer, int((320 - width) / 2), 52)

  ssd.show()

def load_icons(all_icons):
  sd = sdcard.SDCard(spi, Pin(22, Pin.OUT), 10_000_000)
  os.mount(sd, '/sd', readonly=True)

  icnsFileMagicNumber = b'\x69\x63\x6E\x73'
  ICNrsrcMagicNumber  = b'\x49\x43\x4E\x23'

  file_list = os.listdir('/sd')
  print('Loading ICN files')
  for i in range(len(file_list)):
    gc.collect()
    print('Mem free: ' + str(gc.mem_free()))
    slowdraw.draw_progress_bar(ssd, 110, 78, i, len(file_list) - 1)

    if file_list[i][:1] == '.':
      continue
    try:
      with open('/sd/' + file_list[i], 'rb') as f:
        s = f.read()
        if s.find(icnsFileMagicNumber) == 0:
          iconResourcePosition = s.find(ICNrsrcMagicNumber)
          if iconResourcePosition > 0:
            all_icons.append((file_list[i].replace('.icns', ''), s[iconResourcePosition + 8:iconResourcePosition + 8 + 128]))
    except:
      print('Error: Skipping "' + file_list[i] + '"')
      continue

  os.umount("/sd")


if __name__ == "__main__":
  SSD = ST7789

  pdc = Pin(8, Pin.OUT, value=0)
  pcs = Pin(9, Pin.OUT, value=1)
  prst = Pin(15, Pin.OUT, value=1)
  pbl = Pin(13, Pin.OUT, value=1)

  gc.collect()  # Precaution before instantiating framebuf
  # Max baudrate produced by Pico is 31_250_000. ST7789 datasheet allows <= 62.5MHz.
  # Note non-standard MISO pin. This works, verified by SD card.
  spi = SPI(1, 60_000_000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))

  # Define the display
  # For landscape mode:
  ssd = SSD(spi, height=240, width=320, disp_mode=4, dc=pdc, cs=pcs, rst=prst)
  ssd.fill(ssd.rgb(0xFF,0xFF,0xFF))
  ssd.show()

  slowtyper = slowtype.Slowtype(ChicagoSB_12, framebuf.RGB565)

  BLACK = ssd.rgb(0x00,0x00,0x00)
  WHITE = ssd.rgb(0xFF,0xFF,0xFF)


  slowdraw.clear_screen_with_grey(ssd)
  draw_boot_screen(slowtyper)

  all_icons = []
  load_icons(all_icons)

  slowdraw.clear_screen_with_grey(ssd)
  slowdraw.draw_menu_bar(ssd, slowtyper, ['File', 'Edit', 'View', 'Label', 'Special'])

  windowWidth = 148
  windowHeight = 120

  while True:
    windowX = random.randint(5, 320 - windowWidth - 5)
    windowY = random.randint(20, 240 - windowHeight)

    icon_index = random.randint(0, len(all_icons) - 1)
    random_icon_buffer = icon_to_framebuffer(all_icons[icon_index][1])
    windowTitleWidth = slowdraw.draw_window(ssd, slowtyper, windowX, windowY, windowWidth, windowHeight, all_icons[icon_index][0])

    iconX = int((windowWidth - 32) / 2) + windowX
    iconY = int((windowHeight - 32 - 18) / 2) + windowY + 9
    ssd.blit(random_icon_buffer, iconX, iconY)

    ssd.show()

    gc.collect()

    time.sleep_ms(2000)

    slowdraw.deactivate_window(ssd, windowX, windowY, windowWidth, windowTitleWidth)