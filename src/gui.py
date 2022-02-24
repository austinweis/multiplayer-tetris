import pygame, os

pygame.font.init()
pygame.init()
font_size = 60
font = pygame.font.Font(os.path.dirname(__file__)+'/../assets/font.ttf', font_size)

buttons = []
labels  = []
inputs  = []

def draw(target_surface):
    for button in buttons:   
        text_surface = font.render(button.text, True, "white")
        pygame.draw.rect(target_surface, button.color, button.rect)
        target_surface.blit(text_surface, (button.rect.centerx - text_surface.get_width()/2, button.rect.centery - text_surface.get_height()/2))
    for label in labels:
        target_surface.blit(label.text_surface, (label.position[0] - label.text_surface.get_width()/2, label.position[1] - label.text_surface.get_height()/2))
    for input in inputs:
        target_surface.blit(input.text_surface, (input.rect.centerx - input.text_surface.get_width()/2, input.rect.centery - input.text_surface.get_height()/2))
        pygame.draw.rect(target_surface, input.color, input.rect, 2)
        pygame.draw.rect(target_surface, input.color, input.line)
def call(event):
    for button in buttons:
        if event.type == pygame.MOUSEBUTTONUP:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                return button
    for input in inputs:
        if event.type == pygame.MOUSEBUTTONUP:
            if input.rect.collidepoint(event.pos):
                input.active = True
                input.line.width = 8
            else:
                input.line.width = 0
                input.active = False
        if event.type == pygame.KEYDOWN:
            if input.active:
                if event.key == pygame.K_BACKSPACE:
                    input.text = input.text[:-1]
                elif input.rect.width-50 > input.text_surface.get_width():
                    input.text += event.unicode    
                input.text_surface = font.render(input.text, True, input.color)
                input.line.x = input.rect.centerx + input.text_surface.get_width()/2
    return None

    return None
def hide_all(target_surface):
    global buttons, labels, inputs
    buttons, labels, inputs = [], [], []

class Button:
    def __init__(self, dimensions=(100,100), position=(0,0),color=(255,255,255), text=''):
        self.rect  = pygame.Rect(position[0]-(dimensions[0]/2), position[1]-(dimensions[1]/2), dimensions[0], dimensions[1])
        self.color = color
        self.text  = text
        buttons.append(self)
    def update(self, dimensions=None, position=None, color=None, text=None):
        self.rect.width  = self.rect.width  if dimensions ==None else dimensions[0]
        self.rect.height = self.rect.height if dimensions==None  else dimensions[1]

        self.rect.centerx = self.rect.centerx if position==None else position[0]
        self.rect.centery = self.rect.centery if position==None else position[1] 

        self.color = self.color if color==None else color

        self.text  = self.text if text==None else text
    def toggle(self):
        buttons.remove(self) if self in buttons else buttons.append(self)

class Label:
    def __init__(self, position, color=(0, 0, 0), text='Title'):
        self.position = position
        self.color = color
        self.text  = text
        self.text_surface = font.render(text, False, color)
        labels.append(self)
    def update(self, position=None, color=None, text=None):
        self.color = self.color if color==None else color
        self.text  = self.text  if text==None  else text
        self.position = self.position if position==None else position
        self.text_surface = font.render(self.text, False, self.color)
    def toggle(self):
        labels.remove(self) if self in labels else labels.append(self)

class InputBox:
    def __init__(self, dimensions=(100, 50), position=(0, 0), color=(255, 255, 255), text=''):
        self.rect  = pygame.Rect(position[0]-(dimensions[0]/2), position[1]-(dimensions[1]/2), dimensions[0], dimensions[1])
        self.color = color
        self.text = text
        self.text_surface = font.render(text, False, self.color)
        self.active = False
        self.line = pygame.Rect(self.rect.centerx, self.rect.centery - self.rect.height/3, 0, self.rect.height/1.5)

        inputs.append(self)
    def update(self, dimensions=None, position=None, color=None, text=None):
        self.rect.width  = self.rect.width  if dimensions ==None else dimensions[0]
        self.rect.height = self.rect.height if dimensions==None  else dimensions[1]

        self.rect.centerx = self.rect.centerx if position==None else position[0]
        self.rect.centery = self.rect.centery if position==None else position[1] 

        self.color = self.color if color==None else color

        self.text  = self.text if text==None else text
    def toggle(self):
        inputs.remove(self) if self in inputs else inputs.append(self)