class Grid:
    def __init__(self, width, height):
        self.cells_x = width
        self.cells_y = height
        
        self.cells = [[None for x in range(width)] for y in range(height)]
    
    def get_cell(self, x, y):
        try:
            return self.cells[y][x]
        except:
            return None
    
    def set_cell(self, x, y, color):
        self.cells[y][x] = color

