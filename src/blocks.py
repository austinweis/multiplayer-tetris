import pygame
import game

class Block():
    def __init__(self, shapes, color):
        self.landed = False
        self.shapes = shapes
        self.color = color

        self.rotation = 0

        self.last_x = None
        self.last_y = None
        self.x = int(game.GAME_WIDTH/2)
        self.y = 0
    def rotate(self, grid):
        previous = self.rotation
        self.rotation+=1
        if self.rotation == 4:
            self.rotation = 0
        for cell in self.shapes[self.rotation]:
            try:
                if grid[cell[0] + self.x, cell[1] + self.y] != game.BACKGROUND_COLOR :
                    self.rotation = previous
            except:         
                if (cell[0] + self.x) < 0 or (cell[0] + self.x) > game.GAME_WIDTH-1 or (cell[1] + self.y) > game.GAME_HEIGHT-1:
                    self.rotation = previous
        
    def borders(self, grid):
        border = [False, False, False]
        for cell in self.shapes[self.rotation]:
            if cell[1] + self.y >= 0:
                try:
                    if grid[cell[0] + self.x, cell[1] + self.y + 1] != game.BACKGROUND_COLOR:
                        border[2] = True
                except:
                    border[2] = True
                try:
                    if grid[cell[0] + self.x + 1, cell[1] + self.y] != game.BACKGROUND_COLOR:
                        border[0] = True
                except:
                    border[0] = True
                try:
                    if grid[cell[0] + self.x - 1, cell[1] + self.y] != game.BACKGROUND_COLOR:
                        border[1] = True
                except:
                    border[1] = True
                
        return border

I_SHAPE = [
# rotation 1
[(-2, -1), (-1, -1), (0, -1), (1, -1)], 
# rotation 2
[(-1, -2), (-1, -1), (-1, 0), (-1, 1)],
# rotation 3
[(-2, 0), (-1, 0), (0, 0), (1, 0)], 
# rotation 4,
[(0, -1), (0, 0), (0, 1), (0, 2)]
]

J_SHAPE = [
# rotation 1
[(-1, 0), (-1, 1), (0, 1), (1, 1)], 
# rotation 2
[(0, 0), (1, 0), (0, 1), (0, 2)], 
# rotation 3
[(-1, 1), (0, 1), (1, 1), (1, 2)], 
# rotation 4,
[(0, 0), (0, 1), (-1, 2), (0, 2)], 
]

L_SHAPE = [
# rotation 1
[(1, 0), (-1, 1), (0, 1), (1, 1)], 
# rotation 2
[(0, 0), (0, 1), (0, 2), (1, 2)], 
# rotation 3
[(-1, 1), (0, 1), (1, 1), (-1, 2)], 
# rotation 4,
[(0, 0), (0, 1), (-1, 0), (0, 2)], 
]

O_SHAPE = [
# rotation 1
[(0, 0), (1, 0), (0, 1), (1, 1)], 
# rotation 2
[(0, 0), (1, 0), (0, 1), (1, 1)], 
# rotation 3
[(0, 0), (1, 0), (0, 1), (1, 1)], 
# rotation 4,
[(0, 0), (1, 0), (0, 1), (1, 1)], 
]

S_SHAPE = [
# rotation 1
[(0, 0), (1, 0), (-1, 1), (0, 1)], 
# rotation 2
[(0, 0), (0, 1), (1, 1), (1, 2)], 
# rotation 3
[(0, 1), (1, 1), (-1, 2), (0, 2)], 
# rotation 4,
[(-1, 0), (-1, 1), (0, 1), (0, 2)], 
]

T_SHAPE = [
# rotation 1
[(0, -1), (-1, 0), (0, 0), (1, 0)], 
# rotation 2
[(0, -1), (0, 0), (1, 0), (0, 1)], 
# rotation 3
[(-1, 0), (0, 0), (1, 0), (0, 1)], 
# rotation 4
[(0, -1), (-1, 0), (0, 0), (0, 1)], 
]

Z_SHAPE = [
# rotation 1
[(-1, 0), (0, 0), (0, 1), (1, 1)], 
# rotation 2
[(1, 0), (0, 1), (1, 1), (0, 2)], 
# rotation 3
[(-1, 1), (0, 1), (0, 2), (1, 2)], 
# rotation 4,
[(0, 0), (-1, 1), (0, 1), (-1, 2)], 
]

shapes = [Block(I_SHAPE, (0, 255, 255)), Block(J_SHAPE, (0, 0, 255)), Block(L_SHAPE, (255, 128, 0)), Block(O_SHAPE, (255, 255, 0)), Block(S_SHAPE, (0, 255, 0)), Block(T_SHAPE, (255, 0, 255)), Block(Z_SHAPE, (255, 0, 0))]