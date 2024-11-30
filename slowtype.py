import framebuf

class Slowtype():
  def __init__(self, font, format):
    self.font = font
    self.format = format
    self.foreground = 0xFFFF
  
  def get_str_width(self, str):
    width = 0
    for c in str:
      if c == ' ':
        width += 4
      else:
        charData, h, w = self.font.get_ch(c)
        if charData != None:
          width += w
    return width
  
  def buffer_from_str(self, str):
    width = self.get_str_width(str)
    cursor = 0
    h = self.font.height()
    #print(width, h, self.format)
    buffer = framebuf.FrameBuffer(bytearray(2 * width * h), width, h, self.format)
    
    for c in str:
      if c == ' ':
        cursor += 4
      else:
        letter, letterWidth = self.char_to_buffer(c)
        if letter != None:
          buffer.blit(letter, cursor, 0)
          cursor += letterWidth

    return buffer, width

  def char_to_buffer(self, char):
    charData, h, w = self.font.get_ch(char)
    if charData == None:
      return None, 0
    letter = framebuf.FrameBuffer(bytearray(2 * w * h), w, h, self.format)
    charData = bytearray(charData)

    #print(char, w, h)

    bitsPerLine = 8
    if w > 8:
      bitsPerLine = 16

    x = 0
    y = 0
    for byte in charData:
      for bit in range(7, -1, -1):
        if byte & (1 << bit):
          letter.pixel(x,y,self.foreground)
          #print('#', end='')
        #else:
          #print(' ', end='')
        x += 1
        if x >= bitsPerLine:
          #print('')
          x = 0
          y += 1
    return letter, w