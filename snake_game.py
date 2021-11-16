# creating a snake game

import math
import tkinter as tk
import pygame
import random
from tkinter import messagebox


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx = 1, dirny = 0, color =( 255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color


# for movement in the environment
    #dir = direction
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)


    def draw(self,surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        # drawing the rectangle
        pygame.draw.rect(surface, self.color,( i * dis + 1, j * dis+1, dis-2,dis-2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j * dis + 8)
            circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)



class snake(object):
    # creating a snake body so that when it takes food it grows
    body = []
    turns = {}

    # pos = position
    def __init__(self, color, pos):
        # color of the snake
        self.color = color
        # knowing the position of the snake head
        self.head = cube(pos)
        self.body.append(self.head)

        # keeping track on the direction of the snake
        dirnx = 0
        dirny = 1


    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()



            # to check if the player press any key
            keys = pygame.key.get_pressed()


            for key in keys:
                if keys[pygame.K_LEFT]:
                    # moving left
                    self.dirnx = -1
                    # to prevent going to diagonal
                    self.dirny = 0

                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]


                elif keys[pygame.K_RIGHT]:
                    # moving right
                    self.dirnx = 1
                    # to prevent going to diagonal
                    self.dirny = 0

                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    # moving up
                    self.dirnx = 0
                    # to prevent going to diagonal
                    self.dirny = -1

                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    # moving down
                    self.dirnx = 0
                    # to prevent going to diagonal
                    self.dirny = 1

                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i  == len(self.body) - 1:
                    self.turns.pop(p)

            # if you are reached the left edge of the screen you come out from the right age, vice versa

            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])

                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])

                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)

                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    c.move(c.dirnx, c.dirny)


    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = { }
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny


        # appending a new cube to the snake

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

# drawing small lines or boxes in the surface or the environment
def drawGrid(w, rows, surface):
    sizeBtw = w // rows

    x = 0
    y = 0

    for lines in range(rows):
        x = x + sizeBtw
        y = y + sizeBtw

        # draw the line on the surface and the color is white
        pygame.draw.line(surface, (0, 0, 255), (x,0), (x,w))
        pygame.draw.line(surface, (0, 0 ,255),   (0,y), (w,y))



def redrawWindow(surface):
    global rows, width, s, snack

    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    # drawing the grid
    drawGrid(width,rows,surface)
    pygame.display.update()


# adding the food the snake is going to eat

def randomSnack(rows, item):

    position = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        # making sure that the food those not appear at the snake tail
        if len(list(filter(lambda z:z.pos  == (x,y), position))) > 0:
            continue
        else:
            break

    return(x, y)





def messageBox(subject, content):
    root = tk.Tk()

    # let the window show ontop of any window that is currently open
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500
    #height = 600
    rows = 20
    # trying to draw a square shape that why it is width and widht

    win = pygame.display.set_mode((width, width))
# set the color and position of the snake
    s = snake((255,0,0), (10,10))
    # setting the snack
    snack = cube(randomSnack(rows, s), color = (0, 255, 0))

    # setting the speed of the game
    flag = True

    clock = pygame.time.Clock()

    while flag:
        # the lower delay goes the faster the game
        pygame.time.delay(50)

        # the higher tick goise the faster the game
        clock.tick(10)
        # initializing the movement of the snake
        s.move()
        # checking if the snake has eaten the snake
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color = (0, 255, 0))

        # checking if the snake collided with it body
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1: ])):
                print("Score ", len(s.body))
                messageBox("You Lost!!", "Try again")
                s.reset((10,10))
                break



        # adding the window
        redrawWindow(win)


main()