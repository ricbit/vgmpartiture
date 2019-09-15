import sys

class Vgm:
  def __init__(self, vgm):
    self.vgm = vgm
    
def parse_vgm(filename):
  vgm = open(filename, "rb").read()
  if vgm[:4] != b'Vgm ':
    return None
  return Vgm(vgm)

vgm = parse_vgm(sys.argv[1])
print(vgm)

