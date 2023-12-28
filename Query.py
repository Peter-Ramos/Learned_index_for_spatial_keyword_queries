from Mbr import Mbr
from Object import Object
from Mbr import Mbr


class Skr_query:
    def __init__(self, coords, kws):
        self.mbr = Mbr(coords[0][0], coords[0][1], coords[1][0], coords[1][1])
        self.kws = kws

    def get_area(self):
        return self.mbr.get_area()

    def get_kws(self):
        return self.kws

    def print_info(self):
        print("The area is:")
        print(self.mbr.get_area())
        print("the keywords are:")
        print(self.kws)
