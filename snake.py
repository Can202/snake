import pygame
import sys
from pygame import rect
import pygame.locals
import random

PRINCIPALNUMBER = 20
FPS = 15

class colors():
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    GREEN = (0,255, 0)
    RED = (255, 0, 0)
WINDOW_SIZE = {"x":720, "y":480}
COLOR = colors()
class Apple():
    X = 0
    Y = 1
    position = [random.randrange(WINDOW_SIZE["x"]),random.randrange(WINDOW_SIZE["x"])]
    width = PRINCIPALNUMBER
    height = PRINCIPALNUMBER
    def draw(self, root, position_x, position_y):
        pygame.draw.rect(root, COLOR.RED, (position_x, position_y, self.width, self.height))
    def random(self):
        self.position = [random.randrange(WINDOW_SIZE["x"]),random.randrange(WINDOW_SIZE["y"])]
    def collision_with(self, object):
        if object.position[self.Y] >= self.position[self.Y] and object.position[self.Y] <= self.position[self.Y] + self.height and object.position[self.X] >= self.position[self.X] and object.position[self.X] <= self.position[self.X] + self.width:
            return True
        elif object.position[self.Y] + object.height >= self.position[self.Y] and object.position[self.Y] + object.height <= self.position[self.Y] + self.height and object.position[self.X] >= self.position[self.X] and object.position[self.X] <= self.position[self.X] + self.width:
            return True
        elif object.position[self.Y] + object.height >= self.position[self.Y] and object.position[self.Y] + object.height <= self.position[self.Y] + self.height and object.position[self.X] + object.width >= self.position[self.X] and object.position[self.X] + object.width <= self.position[self.X] + self.width:
            return True
        elif object.position[self.Y] >= self.position[self.Y] and object.position[self.Y] <= self.position[self.Y] + self.height and object.position[self.X] + object.width >= self.position[self.X] and object.position[self.X] + object.width <= self.position[self.X] + self.width:
            return True
        else:
            return False

class Snake():
    X = 0
    Y = 1
    position = [int(WINDOW_SIZE["x"]/2),int(WINDOW_SIZE["y"]/2)]
    direction = [0,0]
    length = 1
    width = PRINCIPALNUMBER
    height = PRINCIPALNUMBER
    velocity = width
    def draw(self, root, position_x, position_y):
        pygame.draw.rect(root, COLOR.GREEN, (position_x, position_y, self.width, self.height))
    def process(self):
        pressed = pygame.key.get_pressed()
        if (pressed[pygame.locals.K_RIGHT] or pressed[pygame.locals.K_d]) :
            self.direction[self.X] = 1
            self.direction[self.Y] = 0
        elif (pressed[pygame.locals.K_LEFT] or pressed[pygame.locals.K_a]) :
            self.direction[self.X] = -1
            self.direction[self.Y] = 0
        elif (pressed[pygame.locals.K_UP] or pressed[pygame.locals.K_w]) :
            self.direction[self.Y] = -1
            self.direction[self.X] = 0
        elif (pressed[pygame.locals.K_DOWN] or pressed[pygame.locals.K_s]) :
            self.direction[self.Y] = 1
            self.direction[self.X] = 0
        self.position[self.X] += self.velocity * self.direction[self.X]
        self.position[self.Y] += self.velocity * self.direction[self.Y]



pygame.init()
CLOCK = pygame.time.Clock()
def main():
    
    root = pygame.display.set_mode((WINDOW_SIZE["x"], WINDOW_SIZE["y"]))
    pygame.display.set_caption("snake")
    snake = Snake()
    apple = Apple()
    
    while True:
        
        clear(root)
        snake, apple = mod(snake, apple)
        draw(root, snake, apple)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
        CLOCK.tick(FPS)
def mod(snake, apple):
    snake.process()
    if apple.collision_with(snake):
        apple.random()
    return snake, apple
def clear(root):
    root.fill(COLOR.BLACK)
def draw(root, snake, apple):
    apple.draw(root, apple.position[snake.X], apple.position[snake.Y])
    snake.draw(root, snake.position[snake.X], snake.position[snake.Y])
if __name__ == "__main__":
    main()