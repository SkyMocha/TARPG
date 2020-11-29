import libtcodpy as tcod

class Tile():
    def __init__(self, t=' ', c=tcod.white):
        self.char = t
        if (c != tcod.white):
            c = tcod.color.Color(c[0], c[1], c[2])
        self.color = c

class NullTile(Tile):
    def __init__(self):
        super().__init__('#', tcod.black)

class BorderTile(Tile):
    def __init__(self):
        super().__init__('#', tcod.grey)

class MapTile(Tile):
    def __init__(self, val, variant):
        tmp = self.GetTile(val, variant)
        self.char = tmp[0]
        self.color = tmp[1]

    def GetTile (self, value, variant):

        tile = ' '
        color = tcod.black

        if (value == 0):
            return (' ', tcod.Color (0, 0, 0))
        # WATER
        elif (value < 0.3):
            # COLORS
            if (value < 0.15):
                color = (20, 20, 80)
            elif (value < 0.2):
                color = (20, 20, 100)
            elif (value < 0.235):
                color = (20, 20, 170)
            elif (value < 0.2625):
                color = (20, 20, 220)
            elif (value < 0.3):
                color = (20, 20, 255)
            # VARIANTS
            if (variant < 72):
                tile = '~'
            elif (variant < 90):
                tile = '-'
            elif (variant < 97):
                tile = '^'
            elif (variant < 101):
                tile = '='
            else:
                tile = '~'
        # BEACH
        elif (value < 0.325):
            # COLORS
            if (value < 0.3125):
                color = (178, 162, 100)
            elif (value < 0.3175):
                color = (184, 170, 112)
            elif (value < 0.325):
                color = (194, 178, 128)
            # VARIANTS
            if (variant < 80):
                tile = '#'
            elif (variant < 100):
                tile = '^'
            else:
                tile = '#'
        # GRASS
        elif (value < 0.75):
            color = (20, int(255 * value * (10/7)), 20)
            tile = '#'
            if (variant < 70):
                tile = '#'
            elif (variant < 95):
                color = (16, 59, 29)
                tile = '%'
            elif (variant < 101):
                color = (30, 80, 50)
                tile = '!'
        #VALLEY
        # elif (value < 0.7375):
        #     color = (20, 50, 20)
        #     tile = '#'
        # MOUNTAIN
        elif (value < 1):
            if (value < 0.75 and variant < 50):
                tile = '.'
            if (value < 0.7525):
                color = (133, 138, 133)
            elif (value < 0.775):
                color = (166, 172, 166)
            elif (value < 1):
                color = (220, 250, 215)
            tile = '^'
        # if (biome_tile == 0):
        #     return (tile, color)
        return (tile, color)