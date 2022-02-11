class KeyboardMap:
    def __init__(self, mapped_keyboard):
        self.map = dict( [(tup[1], tup[0]) for row in mapped_keyboard for tup in row] )
        self.keyboard = [ [tup[1] for tup in row ] for row in mapped_keyboard ]