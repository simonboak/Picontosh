def draw_progress_bar(ssd, x, y, value, max):
  BLACK = ssd.rgb(0x00,0x00,0x00)
  WHITE = ssd.rgb(0xFF,0xFF,0xFF)

  if (value < max):
    percentage = value / max * 100
  else:
    percentage = 100

  ssd.fill_rect(x, y, 100, 6, WHITE)
  ssd.rect(x, y, 100, 6, BLACK)
  ssd.rect(x, y, int(percentage), 6, BLACK, BLACK)
  ssd.show()

def clear_screen_with_grey(ssd):
  BLACK = ssd.rgb(0x00,0x00,0x00)
  WHITE = ssd.rgb(0xFF,0xFF,0xFF)

  # First clear to white
  ssd.fill(ssd.rgb(0xFF,0xFF,0xFF))

  # Color alternate pixels in black
  x = 0
  y = 0
  alt = 1
  while y < 240:
    ssd.pixel(x, y, BLACK)
    x = x + 2
    if x > 319:
      alt = alt * -1
      if alt > 0:
        x = 0
      else:
        x = 1
      y = y + 1

  ssd.show()

def draw_menu_bar(ssd, slowtyper, items):
  BLACK = ssd.rgb(0x00,0x00,0x00)
  WHITE = ssd.rgb(0xFF,0xFF,0xFF)

  ssd.fill_rect(0, 0, 320, 19, WHITE)
  ssd.hline(0, 19, 320, BLACK)

  # Rounded corners
  cornerShape = [5, 3, 2, 1, 1]
  for i, length in enumerate(cornerShape):
    # Top/bottom left
    ssd.hline(0, i, length, BLACK)
    ssd.hline(0, 239 - i, length, BLACK)
    # Top/bottom right
    ssd.hline(320 - length, i, length, BLACK)
    ssd.hline(320 - length, 239 - i, length, BLACK)
  
  # Mystery logo
  stevesBits = [
    (5, 0, 2),
    (4, 1, 2),
    (4, 2, 1),
    (1, 3, 3),
    (5, 3, 3),
    (0, 4, 9),
    (0, 5, 7),
    (0, 6, 7),
    (0, 7, 9),
    (0, 8, 9),
    (1, 9, 7),
    (2, 10, 2),
    (5, 10, 2)
  ]
  for line in stevesBits:
    ssd.hline(line[0] + 19, line[1] + 3, line[2], BLACK)

  # Text items
  menuText = '   '.join(items)
  menuTextBuffer, menuTextWidth = slowtyper.buffer_from_str(menuText)
  ssd.blit(menuTextBuffer, 42, 3)


def draw_window(ssd, slowtyper, x, y, width, height, title):
  BLACK = ssd.rgb(0x00,0x00,0x00)
  WHITE = ssd.rgb(0xFF,0xFF,0xFF)

  # Window outline
  ssd.fill_rect(x, y, width, height, WHITE)
  ssd.rect(x, y, width, height, BLACK)

  # Window shadow
  ssd.hline(x+1, y+height, width, BLACK)
  ssd.vline(x+width, y+1, height, BLACK)

  # Title bar
  ssd.hline(x, y+18, width, BLACK)
  lineOffset = 4
  while lineOffset < 16:
    ssd.hline(x+2, y+lineOffset, width-4, BLACK)
    lineOffset += 2

  # Draw the title text
  titleBuffer, titleBufferWidth = slowtyper.buffer_from_str(title)
  if titleBufferWidth > (width - 60):
    # Trim longer titles
    titleDoesntFit = True
    shorterTitle = title
    while titleDoesntFit:
      shorterTitle = shorterTitle[:-1]
      #print('Too long: ', titleBufferWidth)
      #print(shorterTitle)
      titleBuffer, titleBufferWidth = slowtyper.buffer_from_str(shorterTitle + '...')
      #print('Shorter: ', titleBufferWidth)
      if titleBufferWidth < (width - 60):
        titleDoesntFit = False


  titleX = int((width - titleBufferWidth) / 2)
  ssd.fill_rect(x + titleX - 6, y + 4, titleBufferWidth + 12, 13, WHITE)
  ssd.blit(titleBuffer, x + titleX, y + 4)

  # Close box
  ssd.fill_rect(x+6, y+4, 13, 11, WHITE)
  ssd.rect(x+7, y+4, 11, 11, BLACK)

  return titleBufferWidth

  # Scrollbars
  #ssd.hline(x, y+height-14, width, BLACK)
  #ssd.vline(x+width-14, y+15, height-15, BLACK)


def deactivate_window(ssd, x, y, width, windowTitleWidth):
  WHITE = ssd.rgb(0xFF,0xFF,0xFF)
  # Clear the title bar area for a window at this position but leav the title text
  widthToDelete = int((width - windowTitleWidth) / 2) - 2
  ssd.fill_rect(x+2, y+2, widthToDelete, 13, WHITE)
  ssd.fill_rect(x+3+windowTitleWidth+widthToDelete, y+2, widthToDelete, 13, WHITE)


