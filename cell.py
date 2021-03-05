class Cell:
    def __init__(self):
        self.bomb = False
        self.clicked = False
        self.empty = True
        self.flag = False
        self.nearby_bombs_count = 0

    def set_bomb(self):
        self.bomb = True
        self.empty = False
        self.nearby_bombs_count = 0

    def set_clicked(self):
        self.clicked = True

    def set_empty(self):
        self.empty = True

    def __repr__(self):
        if self.bomb:
            return 'B'
        elif self.empty:
            return '_'
        else:
            return str(self.nearby_bombs_count)
