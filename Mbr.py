class Mbr:
    def __init__(self, minx, miny, maxx, maxy):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def change_with_mbr(self, mbr):
        dims = mbr.get_dimensions
        self.minx = dims[0][0]
        self.miny = dims[0][1]
        self.maxx = dims[1][0]
        self.maxy = dims[1][1]

    def get_area(self):
        return [[self.minx, self.miny], [self.maxx, self.maxy]]
