import pygame
import sys
import pygame.locals
import random

PRINCIPALNUMBER = 20
FPS = 15

class colors():
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    GREEN = (0,255, 0)
    RED = (255, 0, 0)
WindowSize = {"x":720, "y":480}
COLOR = colors()

class Object():
    def __init__(self):
        self.X = 0
        self.Y = 1
        self.width = PRINCIPALNUMBER
        self.height = PRINCIPALNUMBER
        self.color = COLOR.WHITE
        self.start()
    def start(self):
        pass
    def draw(self, root, position_x, position_y):
        pygame.draw.rect(root, self.color, (position_x, position_y, self.width, self.height))
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

class Label():
    pygame.font.init()
    myfont = pygame.font.SysFont("None", 20)
    label = myfont.render("text here", 1, COLOR.WHITE)
    def text(self, text : str):
        self.label = self.myfont.render(text, 1, (255,255,255))
    def print(self, root, position=[0,0]):
        root.blit(self.label, (position[0], position[1]))


class Apple(Object):
    def start(self):
        self.position = [random.randrange(WindowSize["x"]),random.randrange(WindowSize["y"])]
        self.color = COLOR.RED
    def random(self):
        self.position = [random.randrange(WindowSize["x"]),random.randrange(WindowSize["y"])]

class Snake(Object):
    def start(self):
        self.color = COLOR.GREEN
        self.position = [int(WindowSize["x"]/2),int(WindowSize["y"]/2)]
        self.direction = [0,0]
        self.length = 0
        self.velocity = self.width
    def process(self):
        pressed = pygame.key.get_pressed()
        if (pressed[pygame.locals.K_RIGHT] or pressed[pygame.locals.K_d]) and self.position[self.X] < WindowSize["x"] - self.width:
            self.direction[self.X] = 1
            self.direction[self.Y] = 0
        elif (pressed[pygame.locals.K_LEFT] or pressed[pygame.locals.K_a]) and self.position[self.X] > 0:
            self.direction[self.X] = -1
            self.direction[self.Y] = 0
        elif (pressed[pygame.locals.K_UP] or pressed[pygame.locals.K_w]) :
            self.direction[self.Y] = -1
            self.direction[self.X] = 0
        elif (pressed[pygame.locals.K_DOWN] or pressed[pygame.locals.K_s]) :
            self.direction[self.Y] = 1
            self.direction[self.X] = 0
        if self.direction[self.X] == 1 and self.position[self.X] >= WindowSize["x"] - self.width:
            self.direction[self.X] = 0
        elif self.direction[self.X] == -1 and self.position[self.X] <= 0:
            self.direction[self.X] = 0
        if self.direction[self.Y] == 1 and self.position[self.Y] >= WindowSize["y"] - self.height:
            self.direction[self.Y] = 0
        elif self.direction[self.Y] == -1 and self.position[self.Y] <= 0:
            self.direction[self.Y] = 0
        self.position[self.X] += self.velocity * self.direction[self.X]
        self.position[self.Y] += self.velocity * self.direction[self.Y]

class Tail(Object):
    def __init__(self, snake : Snake):
        self.X = 0
        self.Y = 1
        self.width = PRINCIPALNUMBER
        self.height = PRINCIPALNUMBER
        self.color = COLOR.GREEN
        self.direction = [0,0]
        self.velocity = self.width
        self.lensnake = snake.length
        self.position = [snake.position[snake.X] - snake.direction[snake.X] * snake.width * snake.length, snake.position[snake.Y] - snake.direction[snake.Y] * snake.height * snake.length]
    def process(self, snake : Snake, beforeTail):
        self.position = [snake.position[snake.X] - snake.direction[snake.X] * snake.width * self.lensnake, snake.position[snake.Y] - snake.direction[snake.Y] * snake.height * self.lensnake]

pygame.init()
CLOCK = pygame.time.Clock()
Score = 0
def main():
    root = pygame.display.set_mode((WindowSize["x"], WindowSize["y"]))
    pygame.display.set_caption("snake")
    snake = Snake()
    apple = Apple()
    score_label = Label()
    tail = []
    
    while True:

        if len(tail) < snake.length:
            for i in range(snake.length - len(tail)):
                tail.append(Tail(snake))

        clear(root)
        snake, apple, score_label = mod(snake, apple, score_label)
        draw(root, snake, apple, score_label, tail)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
        CLOCK.tick(FPS)
def mod(snake, apple, score_label):
    global Score
    snake.process()
    if apple.collision_with(snake):
        apple.random()
        Score += 1
        snake.length += 1
    score_label.text(str(Score))
    return snake, apple, score_label
def clear(root):
    root.fill(COLOR.BLACK)
def draw(root, snake, apple, score_label, tail):
    apple.draw(root, apple.position[snake.X], apple.position[snake.Y])
    snake.draw(root, snake.position[snake.X], snake.position[snake.Y])
    for i in range(len(tail)):
        if i != 0:
            tail[i].process(snake, tail[i-1])
        else:
            tail[i].process(snake, snake)
        tail[i].draw(root, tail[i].position[tail[i].X], tail[i].position[tail[i].Y])
    score_label.print(root, [15,15])
if __name__ == "__main__":
    main()