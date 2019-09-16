import sys

class Dummy:
  pass

class Vgm:
  GD3_TAGS = [
    'Track name (english)',
    'Track name (japanese)',
    'Game name (english)',
    'Game name (japanese)',
    'System name (english)',
    'System name (japanese)',
    'Author name (english)',
    'Author name (japanese)',
    'Date',
    'File creator',
    'Notes']

  def __init__(self, vgm):
    self.vgm = vgm
    self.gd3 = self.parse_gd3()
    self.nes_clock = self.uint32(0x84)
    self.data_offset = self.pointer(0x34)

  def parse_gd3(self):
    gd3_pointer = self.pointer(0x14)
    if gd3_pointer == 0 or self.data(gd3_pointer, 4) != b'Gd3 ':
      self.gd3 = None
      return
    size = self.uint32(gd3_pointer + 8)
    raw_gd3 = self.data(gd3_pointer + 12, size)
    decoded_gd3 = raw_gd3.decode('utf-16').split('\0')
    return dict(zip(Vgm.GD3_TAGS, decoded_gd3))

  def uint32(self, offset):
    return int.from_bytes(self.data(offset, 4), byteorder='little')

  def uint16(self, offset):
    return int.from_bytes(self.data(offset, 2), byteorder='little')

  def pointer(self, offset):
    return self.uint32(offset) + offset

  def data(self, offset, size):
    return self.vgm[offset : offset + size]

  def parse_nes(self, nes):
    current = self.data_offset
    while (code := self.vgm[current]) != 0x66:
      if (code & 0xF0) == 0x70:
        print("wait %d" % (code - 0x70 + 1))
        current += 1
      elif code == 0x61:
        print("wait %d" % self.uint16(current + 1))
        current += 3
      elif code == 0x62:
        print("wait %d" % 735)
        current += 1
      elif code == 0xB4:
        print("nes reg %02X val %02X" % (
            self.vgm[current + 1], self.vgm[current + 2]))
        current += 3
      else:
        print("unknown code %02X" % code)
        return
    
def parse_vgm(filename):
  vgm = open(filename, "rb").read()
  if vgm[:4] != b'Vgm ':
    return None
  return Vgm(vgm)

class NesApu:
  def __init__(self):
    pass

vgm = parse_vgm(sys.argv[1])
for tag, value in vgm.gd3.items():
    print(tag, ':', value)
nes = NesApu()
vgm.parse_nes(nes)
