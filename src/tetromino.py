class Tetromino:
    current_rotation = 0
    x, y = 0, 0

    def __init__(self, shapes, color):
        self.shapes = shapes
        self.color = color
    
    def create(self, x, y):
        object = Tetromino(self.shapes, self.color)
        object.x, object.y = x, y

        return object
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def rotate(self):
        self.current_rotation = (self.current_rotation + 1) % len(self.shapes)
    
    def get_shape(self):
        return self.shapes[self.current_rotation]
    
    def left(self):
        shape = self.get_shape()

        for row in range(len(shape)):
            for col in range(len(shape[row])):
               if shape[row][col]:
                    return self.x + col
        
        return self.x
    
    def right(self):
        shape = self.get_shape()

        for row in range(len(shape)):
            for col in range(len(shape[row]) - 1, 0, -1):
               if shape[row][col]:
                    return self.x + col
        
        return self.x
    
    def bottom(self):
        shape = self.get_shape()

        for row in range(len(shape) - 1, 0, -1):
            for col in range(len(shape[row])):
               if shape[row][col]:
                    return self.y + row
        
        return self.y

# Shapes for the tetrominos
I_SHAPES = [
    [[0,0,0,0],
    [1,1,1,1],
    [0,0,0,0],
    [0,0,0,0]],

    [[0,1,0,0],
    [0,1,0,0],
    [0,1,0,0],
    [0,1,0,0]]
]

O_SHAPES = [
    [[0,0,0,0],
    [0,1,1,0],
    [0,1,1,0],
    [0,0,0,0]]
]

J_SHAPES = [
    [[0,0,0,0],
    [1,0,0,0],
    [1,1,1,1],
    [0,0,0,0]]
]