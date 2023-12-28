class Object:
    loc = None

    def __init__(self, loc, kws):
        self.loc = loc
        self.kws = kws

    def get_location(self):
        return self.loc

    def get_kws(self):
        return self.kws

    def print_info(self):
        print("The location is: ")
        print(self.loc)
        print("The keywords are: ")
        print(self.kws)
