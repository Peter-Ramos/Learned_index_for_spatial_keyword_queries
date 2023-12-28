from Mbr import Mbr
from Object import Object
from Query import Skr_query


class Cell:
    def __init__(self, coords, obj):
        self.objects = []
        self.kws = []
        self.mbr = Mbr(coords[0][0], coords[0][1], coords[1][0], coords[1][1])
        for i in obj:
            self.set_object(i)

    def get_area(self):
        return self.mbr.get_area()

    def get_objects(self):
        return self.objects

    def get_kws(self):
        return self.kws

    def set_object(self, obj):
        self.objects.append(obj)
        keywords = obj.get_kws()
        for j in keywords:
            if j not in self.kws:
                self.kws.append(j)

    def get_num_of_objects(self):
        return len(self.objects)

    def print_info(self):
        print("It has the area of: ")
        print(self.mbr.get_area())
        print("Num of objects is: ")
        print(len(self.objects))
