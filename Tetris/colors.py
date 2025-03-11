
class Colors:
    def __init__(self):
        self.dark_grey = (26, 31, 40)
        self.green = (47, 230, 23)
        self.red = (232, 18, 18)
        self.orange = (226, 116, 17)
        self.yellow = (237, 234, 4)
        self.purple = (166, 0, 247)
        self.cyan = (21, 204, 209)
        self.blue = (13, 64, 216)
        self.white = (255, 255, 255)
        self.dark_blue = (44, 44, 127)
        self.light_blue = (59, 85, 162)
    
    def get_cell_colors(self):
        return [self.dark_grey, self.green, self.red, self.orange, self.yellow, self.purple, self.cyan, self.blue]
        