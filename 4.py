import pygame
import sys
import random
import time
from math import *
import Pause as p


pygame.init()
width = 1400
height = 800
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Shooter Game PBL Project")
done = False
clock = pygame.time.Clock()


margin = 150
lowerBound = 120
score = 0


white = (230, 230, 230)
lightBlue = (4, 27, 96)
red = (231, 76, 60)
lightGreen = (25, 111, 61)
darkGray = (40, 55, 71)
darkBlue = (64, 178, 239)
green = (35, 155, 86)
yellow = (244, 208, 63)
blue = (46, 134, 193)
purple = (155, 89, 182)
orange = (243, 156, 18)
black = (0,0,0)



font = pygame.font.SysFont("Algerian", 35)


class Balloon:
    
    def __init__(self, speed):
        self.a = random.randint(50, 90)
        self.b = self.a + random.randint(0, 50)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 200
        self.speed = -speed
        self.proPool= [-1, -1, -1, 0, 0, 0, 2, 2, 2, 2]
        self.length = random.randint(100, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue, darkGray, darkBlue, lightGreen, lightBlue])
        
    
    def move(self):
        direct = random.choice(self.proPool)

        if direct == -1:
            self.angle += -8
        elif direct == 0:
            self.angle += 2
        else:
            self.angle += 6

        self.y += self.speed*sin(radians(self.angle))
        self.x += self.speed*cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height/5:
                self.x -= self.speed*cos(radians(self.angle)) 
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 3:
            self.reset()
            
    
    def show(self):
        pygame.draw.line(display, black, (self.x + self.a/2, self.y + self.b), (self.x + self.a/2, self.y + self.b + self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, 2*self.a, 2*self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a/2 - 5, self.y + 2*self.b - 8, 10, 10))
            
    
    def burst(self):
        global score
        pos = pygame.mouse.get_pos()

        if isonBalloon(self.x, self.y, 2*self.a, 2*self.b, pos):
            score += 1
            self.reset()
            
    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound 
        self.angle = 90
        self.speed -= 0.002
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue, darkGray, darkBlue, lightGreen, lightBlue])
is_paused = False






balloons = []
noBalloon = 10

time_limit = 10
start_time = time.time()
print (start_time)



for i in range(noBalloon):
    obj = Balloon(random.choice([5, 5, 5, 5, 6, 5, 3, 3, 3, 4]))
    balloons.append(obj)


def isonBalloon(x, y, a, b, pos):
    if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
    else:
        return False
    

def pointer():
    pos = pygame.mouse.get_pos()
    r = 25
    l = 20
    color = red
    for i in range(noBalloon):
        if isonBalloon(balloons[i].x, balloons[i].y, balloons[i].a, balloons[i].b, pos):
            color = red
    pygame.draw.ellipse(display, color, (pos[0] - r/2, pos[1] - r/2, r, r), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] - l/2), (pos[0], pos[1] - l), 4)
    pygame.draw.line(display, color, (pos[0] + l/2, pos[1]), (pos[0] + l, pos[1]), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] + l/2), (pos[0], pos[1] + l), 4)
    pygame.draw.line(display, color, (pos[0] - l/2, pos[1]), (pos[0] - l, pos[1]), 4)


def lowerPlatform():
    pygame.draw.rect(display, darkGray, (0, height - lowerBound, width, lowerBound))
    

def showScore():
    scoreText = font.render("Balloons Bursted : " + str(score), True, white)
    display.blit(scoreText, (150, height - lowerBound + 50))


    
    

def close():
    pygame.quit()
    sys.exit()
   


def game():
    global score
    loop = True

    while loop:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    score = 0
                    game()
                if event.key == pygame.K_p:
                    p.pause()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i in range(noBalloon):
                            balloons[i].burst()

        display.fill(white)
        
        for i in range(noBalloon):
            balloons[i].show()

        pointer()
        
        for i in range(noBalloon):
            balloons[i].move()

        
        lowerPlatform()
        showScore()
        pygame.display.update()
        clock.tick(60)
        
game()

