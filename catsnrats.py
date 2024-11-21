import pygame
import math
import copy
from borders import *

cheese_img = pygame.transform.scale(pygame.image.load('C:/Users/emaan/catsnrats/img/cheesepellet.png'), (30, 25))
superapple_img = pygame.transform.scale(pygame.image.load('C:/Users/emaan/catsnrats/img/apple.png'), (30, 30))

# define cat function
# this will move the cat, have it chase the target (rat), increment speed, change direction, and manage collisions
class cat:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 30
        self.center_y = self.y_pos + 30
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw_cats()
    
    # method to draw cats as dead, powerup, or normal
    def draw_cats(self):
        if (not powerup and not self.dead) or (eaten_cat[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_cat[self.id]:
            screen.blit(powerup_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        
        # variable to create a clear rectangle around cat image to detect collision
        cat_rect = pygame.rect.Rect(
            (self.center_x - 10, self.center_y - 10), (20, 20))
        return cat_rect
    
    def check_collisions(self):
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False] # right, left, up, down

        # self[0] -> right
        # self[1] -> left
        # self[2] -> up
        # self[3] -> down
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y //
                     num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y //
                              num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) //
                     num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) //
                              num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) //
                     num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) //
                              num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True
            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) //
                             num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) //
                                      num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) //
                             num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) //
                                      num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(
                        self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(
                                self.center_x - num2) // num2] == 9 and (
                                self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) //
                                                    num2] < 3 or (level[self.center_y //
                                                                        num1][(self.center_x + num2) // num2] == 9 and (
                                                        self.in_box or self.dead)):
                        self.turns[0] = True
            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) //
                             num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) //
                                      num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) //
                             num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) //
                                      num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(
                        self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(
                                self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(
                        self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(
                                self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True

        # statement to check if cats are in the box area in the middle of the screen
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box
    
    # method directs yellow cat, targets rat, and changed direction if collides
    def move_yellow(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30
        return self.x_pos, self.y_pos, self.direction
    
    # method directs orange cat, targets rat, and changed direction if collides
    def move_orange(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30
        return self.x_pos, self.y_pos, self.direction
    
    # method directs purple cat, targets rat, and changed direction if collides
    def move_purple(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30
        return self.x_pos, self.y_pos, self.direction
    
    # method directs blue cat, targets rat, and changed direction if collides
    def move_blue(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30
        return self.x_pos, self.y_pos, self.direction
    
# this function draws miscellaneous things like the scoring text, images of rat as lives, lives left and game over and victory screens
def draw_misc():
    # displays score
    score_text = font.render(f'Score: {score}', True, '#00e6fc')
    screen.blit(score_text, (10, 920))
    
    # displays power up indication
    if powerup:
        screen.blit(superapple_img, (140, 910))
    
    # displays number of lives left
    for i in range(lives):
        screen.blit(pygame.transform.scale(
            rat_images[0], (40, 40)), (650 + i * 40, 915))
    lives_text = font.render(f'{lives} lives left', True, '#FFFFFF')  # Number of lives
    screen.blit(lives_text, (650 + lives * 40 + 10, 920))  # Adjust position to align with icons

    # displays game over screen
    if game_over:
        pygame.draw.rect(screen, "#d52b1e",
                         [225, 390, 450, 90], 0, 10)
        gameover_text = font.render(
            'Game Over! Click the Space Bar to Restart', True, '#000000')
        screen.blit(gameover_text, (240, 430))

    # displays victory screen
    if victory:
        pygame.draw.rect(screen, "#339c21",
                         [225, 390, 450, 90], 0, 10)
        victory_text = font.render(
            'Victory! Click the Space Bar to Restart', True, '#000000')
        screen.blit(victory_text, (240, 430))

# this function checks collisions with the cheese pellets and apple pellets and counts scoring based on that
def check_collisions(score_inc, power, power_count, eaten_cats):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < rat_x < 870:
        # score increment when cheese eaten
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            score_inc += 10
        # score increment when apple is eaten
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            score_inc += 50
            power = True
            power_count = 0
            eaten_cats = [False, False, False, False]
    return score_inc, power, power_count, eaten_cats

# method that draws the borders (maze)
def draw_borders():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):

            # draws cheese pellets
            if level[i][j] == 1:
                screen.blit(cheese_img, (j * num2 + (0.5 * num2) - 10, i * num1 + (0.5 * num1) - 10))
            # draws apple pellets
            if level[i][j] == 2 and not flicker:
                screen.blit(superapple_img, (j * num2 + (0.5 * num2) - 10, i * num1 + (0.5 * num1) - 10))
            if level[i][j] == 3:
                pygame.draw.line(screen, color,
                                 (j * num2 + (0.5 * num2),
                                  i * num1),
                                 (j * num2 + (0.5 * num2),
                                  i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color,
                                 (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2,
                                  i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2,
                                 (i * num1 + (0.5 * num1)),
                                 num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)),
                                 (i * num1 + (0.5 * num1)),
                                 num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)),
                                 (i * num1 - (0.4 * num1)),
                                 num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2,
                                 (i * num1 - (0.4 * num1)),
                                 num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, color,
                                 (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2,
                                  i * num1 + (0.5 * num1)), 3)
                
def direction_rat():
    # moves rat to the right
    if direction == 0:
        screen.blit(rat_images[counter // 5],
                    (rat_x, rat_y))
    # moves rat to the left
    elif direction == 1:
        screen.blit(pygame.transform.flip(
            rat_images[counter // 5], True, False),
            (rat_x, rat_y))
    # moves rat up
    elif direction == 2:
        screen.blit(pygame.transform.rotate(
            rat_images[counter // 5], 90),
            (rat_x, rat_y))
    # moves rat down
    elif direction == 3:
        screen.blit(pygame.transform.rotate(
            rat_images[counter // 5], 270),
            (rat_x, rat_y))
        
def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True
        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True
    return turns

# moves rat based on user clicked keys
def move_rat(play_x, play_y):
    if direction == 0 and turns_allowed[0]:
        play_x += rat_speed # right
    elif direction == 1 and turns_allowed[1]:
        play_x -= rat_speed # left
    if direction == 2 and turns_allowed[2]:
        play_y -= rat_speed # up
    elif direction == 3 and turns_allowed[3]:
        play_y += rat_speed # down
    return play_x, play_y

# calculates target positions for each cat based on state of the game and rat position
def get_targets(orange_x, orange_y, purple_x, purple_y,
                blue_x, blue_y, yellow_x, yellow_y):
    if rat_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if rat_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        # orange cat targets rat
        if not orange.dead and not eaten_cat[0]:
            orange_target = (runaway_x, runaway_y)
        elif not orange.dead and eaten_cat[0]:
            if 340 < orange_x < 560 and 340 < orange_y < 500:
                orange_target = (400, 100)
            else:
                orange_target = (rat_x, rat_y)
        else:
            orange_target = return_target

        # purple cat targets rat
        if not purple.dead and not eaten_cat[1]:
            purple_target = (runaway_x, rat_y)
        elif not purple.dead and eaten_cat[1]:
            if 340 < purple_x < 560 and 340 < purple_y < 500:
                purple_target = (400, 100)
            else:
                purple_target = (rat_x, rat_y)
        else:
            purple_target = return_target
        
        # blue cat targets rat
        if not blue.dead:
            blue_target = (rat_x, runaway_y)
        elif not blue.dead and eaten_cat[2]:
            if 340 < blue_x < 560 and 340 < blue_y < 500:
                blue_target = (400, 100)
            else:
                blue_target = (rat_x, rat_y)
        else:
            blue_target = return_target
        
        # yellow cat targets rat
        if not yellow.dead and not eaten_cat[3]:
            yellow_target = (450, 450)
        elif not yellow.dead and eaten_cat[3]:
            if 340 < yellow_x < 560 and 340 < yellow_y < 500:
                yellow_target = (400, 100)
            else:
                yellow_target = (rat_x, rat_y)
        else:
            yellow_target = return_target
    else:
        # power up inactive orange cat
        if not orange.dead:
            if 340 < orange_x < 560 and 340 < orange_y < 500:
                orange_target = (400, 100)
            else:
                orange_target = (rat_x, rat_y)
        else:
            orange_target = return_target

        # power up inactive purple cat
        if not purple.dead:
            if 340 < purple_x < 560 and 340 < purple_y < 500:
                purple_target = (400, 100)
            else:
                purple_target = (rat_x, rat_y)
        else:
            purple_target = return_target
        
        # power up inactive blue cat
        if not blue.dead:
            if 340 < blue_x < 560 and 340 < blue_y < 500:
                blue_target = (400, 100)
            else:
                blue_target = (rat_x, rat_y)
        else:
            blue_target = return_target
        
        # power up inactive yellow cat
        if not yellow.dead:
            if 340 < yellow_x < 560 and 340 < yellow_y < 500:
                yellow_target = (400, 100)
            else:
                yellow_target = (rat_x, rat_y)
        else:
            yellow_target = return_target
    return [orange_target, purple_target,
            blue_target, yellow_target]

# sets position, initializes screen, loads cats/rat images
if __name__ == '__main__':
    pygame.init()
    WIDTH = 900
    HEIGHT = 950
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    timer = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font('freesansbold.ttf', 20)
    level = copy.deepcopy(borders)
    color = '#0000a6'
    PI = math.pi
    rat_images = []
    for i in range(1, 5):
        rat_images.append(pygame.transform.scale(pygame.image.load(
            f'catsnrats/img/{i}.png'), (50, 50)))
        orange_img = pygame.transform.scale(pygame.image.load(
            f'catsnrats/img/orange.png'), (50, 50))
        blue_img = pygame.transform.scale(pygame.image.load(
            f'catsnrats/img/blue.png'), (50, 50))
        purple_img = pygame.transform.scale(pygame.image.load(
            f'catsnrats/img/purple.png'), (50, 50))
        yellow_img = pygame.transform.scale(pygame.image.load(
            f'catsnrats/img/yellow.png'), (50, 50))
        powerup_img = pygame.transform.scale(pygame.image.load(
            f'catsnrats/img/powerup.png'), (50, 50))
        dead_img = pygame.transform.scale(pygame.image.load(
            f'catsnrats/img/dead.png'), (50, 50))
    
    # inital positions/ functions when game starts
    rat_x = 450
    rat_y = 663
    direction = 0
    orange_x = 56
    orange_y = 58
    orange_direction = 2
    purple_x = 440
    purple_y = 388
    purple_direction = 2
    blue_x = 440
    blue_y = 400
    blue_direction = 2
    yellow_x = 440
    yellow_y = 438
    yellow_direction = 2
    counter = 0
    flicker = False
    turns_allowed = [False, False, False, False]
    direction_command = 0
    rat_speed = 2
    score = 0
    powerup = False
    power_counter = 0
    eaten_cat = [False, False, False, False]
    targets = [(rat_x, rat_y),
               (rat_x, rat_y),
               (rat_x, rat_y),
               (rat_x, rat_y)]
    orange_dead = False
    purple_dead = False
    yellow_dead = False
    blue_dead = False
    orange_box = False
    purple_box = False
    yellow_box = False
    blue_box = False
    moving = False
    cat_speeds = [2, 2, 2, 2]
    startup_counter = 0
    lives = 3
    game_over = False
    victory = False

    # main game loop
    run = True
    while run:
        timer.tick(fps)

        if counter < 19:
            counter += 1
            if counter > 3:
                flicker = False
        else:
            counter = 0
            flicker = True
        
        if powerup and power_counter < 600:
            power_counter += 1
        elif powerup and power_counter >= 600:
            power_counter = 0
            powerup = False
            eaten_cat = [False, False, False, False]
        if startup_counter < 180 and not game_over and not victory:
            moving = False
            startup_counter += 1
        else:
            moving = True
        
        screen.fill('#000000') #background color
        draw_borders() # calls function to draw borders
        center_x = rat_x + 23
        center_y = rat_y + 24

        # speed of cat when it is a powerup (slows down)
        if powerup:
            cat_speeds = [1, 1, 1, 1]
        # speed of cat normally (same speed as rat)
        else:
            cat_speeds = [2, 2, 2, 2]
        if eaten_cat[0]:
            cat_speeds[0] = 2
        if eaten_cat[1]:
            cat_speeds[1] = 2
        if eaten_cat[2]:
            cat_speeds[2] = 2
        if eaten_cat[3]:
            cat_speeds[3] = 2
        if orange_dead:
            cat_speeds[0] = 4
        if purple_dead:
            cat_speeds[1] = 4
        if blue_dead:
            cat_speeds[2] = 4
        if yellow_dead:
            cat_speeds[3] = 4
        victory = True

        for i in range(len(level)):
            if 1 in level[i] or 2 in level[i]:
                victory = False
            
        # draws transparant margin
        rat_transparant_margin = pygame.Surface((50,50), pygame.SRCALPHA)
        transparent_color = (13, 17, 23, 0)
        rat_radius = 20
        rat_circle = pygame.draw.circle(rat_transparant_margin, transparent_color, (25, 25), 20)
        rat_rect = pygame.Rect(center_x - rat_radius, center_y - rat_radius, rat_radius * 2, rat_radius * 2)
        screen.blit(rat_transparant_margin, (center_x - 25, center_y - 25))
        

        direction_rat()
        orange = cat(orange_x, orange_y, targets[0],
                    cat_speeds[0], orange_img,
                    orange_direction, orange_dead,
                    orange_box, 0)
        purple = cat(purple_x, purple_y, targets[1],
                     cat_speeds[1], purple_img,
                     purple_direction, purple_dead,
                     purple_box, 1)
        blue = cat(blue_x, blue_y, targets[2],
                      cat_speeds[2], blue_img,
                      blue_direction, blue_dead,
                      blue_box, 2)
        yellow = cat(yellow_x, yellow_y, targets[3],
                       cat_speeds[3], yellow_img,
                       yellow_direction, yellow_dead,
                       yellow_box, 3)
        # calls function to draw the scoring, and end of game screens etc
        draw_misc()
        targets = get_targets(orange_x, orange_y, purple_x, purple_y,
                              blue_x, blue_y, yellow_x, yellow_y)
        turns_allowed = check_position(center_x, center_y)
        if moving:
            rat_x, rat_y = move_rat(rat_x, rat_y)
            if not orange_dead and not orange.in_box:
                orange_x, orange_y, orange_direction = orange.move_orange()
            else:
                orange_x, orange_y, orange_direction = orange.move_yellow()
            if not blue_dead and not blue.in_box:
                blue_x, blue_y, blue_direction = blue.move_blue()
            else:
                blue_x, blue_y, blue_direction = blue.move_yellow()
            if not purple_dead and not purple.in_box:
                purple_x, purple_y, purple_direction = purple.move_purple()
            else:
                purple_x, purple_y, purple_direction = purple.move_yellow()
            yellow_x, yellow_y, yellow_direction = yellow.move_yellow()
        score, powerup, power_counter, eaten_cat = check_collisions(
            score, powerup,
            power_counter, eaten_cat)
        
        # if the powerup oject is not active, check collisions between rat and cats
        if not powerup:

            # checks if rat collides with each cat and is not a dead one
            if (rat_rect.colliderect(orange.rect) and not orange.dead) or \
                    (rat_rect.colliderect(purple.rect) and not purple.dead) or \
                    (rat_rect.colliderect(blue.rect) and not blue.dead) or \
                    (rat_rect.colliderect(yellow.rect) and not yellow.dead):
                
                # check lives counter and plays game accordingly after game over
                if lives > 0:
                    lives -= 1 # reduces lives by 1
                    startup_counter = 0
                    powerup = False
                    power_counter = 0
                    rat_x = 450
                    rat_y = 663
                    direction = 0
                    direction_command = 0

                    # resets everything
                    orange_x = 56
                    orange_y = 58
                    orange_direction = 0
                    purple_x = 440
                    purple_y = 388
                    purple_direction = 2
                    blue_x = 440
                    blue_y = 438
                    blue_direction = 2
                    yellow_x = 440
                    yellow_y = 438
                    yellow_direction = 2
                    eaten_cat = [False, False,
                                   False, False]
                    orange_dead = False
                    purple_dead = False
                    yellow_dead = False
                    blue_dead = False
                else:
                    # if no more lives, game over state begins
                    game_over = True
                    moving = False
                    startup_counter = 0

        # if orange cat ower up collides with rat
        if powerup and rat_rect.colliderect(orange.rect) and\
                eaten_cat[0] and not orange.dead:
            
            # check if lives remain
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1 # reduce lives by 1
                startup_counter = 0
                rat_x = 450
                rat_y = 663
                direction = 0
                direction_command = 0

                # resets everything
                orange_x = 56
                orange_y = 58
                orange_direction = 0
                purple_x = 440
                purple_y = 388
                purple_direction = 2
                blue_x = 440
                blue_y = 438
                blue_direction = 2
                yellow_x = 440
                yellow_y = 438
                yellow_direction = 2
                eaten_cat = [False, False,
                               False, False]
                orange_dead = False
                purple_dead = False
                yellow_dead = False
                blue_dead = False

            # game over state
            else:
                game_over = True
                moving = False
                startup_counter = 0
        
        # if purple powerup collides with rat (similar to above)
        if powerup and rat_rect.colliderect(purple.rect) and\
                eaten_cat[1] and not purple.dead:
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                rat_x = 450
                rat_y = 663
                direction = 0
                direction_command = 0
                orange_x = 56
                orange_y = 58
                orange_direction = 0
                purple_x = 440
                purple_y = 388
                purple_direction = 2
                blue_x = 440
                blue_y = 438
                blue_direction = 2
                yellow_x = 440
                yellow_y = 438
                yellow_direction = 2
                eaten_cat = [False, False,
                               False, False]
                orange_dead = False
                purple_dead = False
                yellow_dead = False
                blue_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        
        # if blue powerup collides with rat (similar to above)
        if powerup and rat_rect.colliderect(blue.rect) and\
                eaten_cat[2] and not blue.dead:
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                rat_x = 450
                rat_y = 663
                direction = 0
                direction_command = 0
                orange_x = 56
                orange_y = 58
                orange_direction = 0
                purple_x = 440
                purple_y = 388
                purple_direction = 2
                blue_x = 440
                blue_y = 438
                blue_direction = 2
                yellow_x = 440
                yellow_y = 438
                yellow_direction = 2
                eaten_cat = [False, False,
                               False, False]
                orange_dead = False
                purple_dead = False
                yellow_dead = False
                blue_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0

        # if yellow powerup collides with rat (similar to above)
        if powerup and rat_rect.colliderect(yellow.rect) and\
                eaten_cat[3] and not yellow.dead:
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                rat_x = 450
                rat_y = 663
                direction = 0
                direction_command = 0
                orange_x = 56
                orange_y = 58
                orange_direction = 0
                purple_x = 440
                purple_y = 388
                purple_direction = 2
                blue_x = 440
                blue_y = 438
                blue_direction = 2
                yellow_x = 440
                yellow_y = 438
                yellow_direction = 2
                eaten_cat = [False, False,
                               False, False]
                orange_dead = False
                purple_dead = False
                yellow_dead = False
                blue_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        
        # deals with collisiosn between orange cat during powerup 
        if powerup and rat_rect.colliderect(orange.rect) and not\
                orange.dead and not eaten_cat[0]:
            orange_dead = True
            eaten_cat[0] = True
            score += (2 ** eaten_cat.count(True)) * 100
        
        # deals with collisiosn between purple cat during powerup 
        if powerup and rat_rect.colliderect(purple.rect) and not\
                purple.dead and not eaten_cat[1]:
            purple_dead = True
            eaten_cat[1] = True
            score += (2 ** eaten_cat.count(True)) * 100

        # deals with collisiosn between blue cat during powerup 
        if powerup and rat_rect.colliderect(blue.rect) and not\
                blue.dead and not eaten_cat[2]:
            blue_dead = True
            eaten_cat[2] = True
            score += (2 ** eaten_cat.count(True)) * 100
        
        # deals with collisiosn between yellow cat during powerup 
        if powerup and rat_rect.colliderect(yellow.rect) and not\
                yellow.dead and not eaten_cat[3]:
            yellow_dead = True
            eaten_cat[3] = True
            score += (2 ** eaten_cat.count(True)) * 100
        
        # game loop for when user presses up, down, left, right keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direction_command = 0
                if event.key == pygame.K_LEFT:
                    direction_command = 1
                if event.key == pygame.K_UP:
                    direction_command = 2
                if event.key == pygame.K_DOWN:
                    direction_command = 3
                
                # handle restart if game over or victory
                if event.key == pygame.K_SPACE and\
                        (game_over or victory):
                    powerup = False
                    power_counter = 0
                    lives -= 1
                    startup_counter = 0
                    rat_x = 450
                    rat_y = 663
                    direction = 0
                    direction_command = 0
                    orange_x = 56
                    orange_y = 58
                    orange_direction = 0
                    purple_x = 440
                    purple_y = 388
                    purple_direction = 2
                    blue_x = 440
                    blue_y = 438
                    blue_direction = 2
                    yellow_x = 440
                    yellow_y = 438
                    yellow_direction = 2
                    eaten_cat = [False, False,
                                   False, False]
                    orange_dead = False
                    purple_dead = False
                    yellow_dead = False
                    blue_dead = False
                    score = 0
                    lives = 3
                    level = copy.deepcopy(borders)
                    game_over = False
                    victory = False
            
            # user directions for keys
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and\
                        direction_command == 0:
                    direction_command = direction
                if event.key == pygame.K_LEFT and\
                        direction_command == 1:
                    direction_command = direction
                if event.key == pygame.K_UP and\
                        direction_command == 2:
                    direction_command = direction
                if event.key == pygame.K_DOWN and\
                        direction_command == 3:
                    direction_command = direction
        
        # update direction based on turns
        if direction_command == 0 and turns_allowed[0]:
            direction = 0
        if direction_command == 1 and turns_allowed[1]:
            direction = 1
        if direction_command == 2 and turns_allowed[2]:
            direction = 2
        if direction_command == 3 and turns_allowed[3]:
            direction = 3

        if rat_x > 900:
            rat_x = -47
        elif rat_x < -50:
            rat_x = 897

        # if cats go back in box, they are no longer dead cats
        if orange.in_box and orange_dead:
            orange_dead = False
        if purple.in_box and purple_dead:
            purple_dead = False
        if blue.in_box and blue_dead:
            blue_dead = False
        if yellow.in_box and yellow_dead:
            yellow_dead = False
        pygame.display.flip()
    
    pygame.quit()
