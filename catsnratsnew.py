# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 00:54:55 2024

@author: hebat
"""

# Importing necessary libraries
import pygame
import math
import copy
from borders import *  # Custom module for level borders

# Load images for game elements (cheese pellets and apple power-ups)
cheese_image = pygame.transform.scale(pygame.image.load('C:/Users/emaan/pacman/img/cheesepellet.png'), (30, 25))
apple_image = pygame.transform.scale(pygame.image.load('C:/Users/emaan/pacman/img/apple.png'), (30, 30))

# Class for enemy cat behavior
class EnemyCat:
    def __init__(self, x_position, y_position, target_position, movement_speed, sprite_image, current_direction, is_dead, in_start_box, unique_id):
        """
        Initializes the attributes of an enemy cat.
        
        Parameters:
        - x_position, y_position: Current position of the cat.
        - target_position: The position the cat is chasing.
        - movement_speed: The speed of the cat's movement.
        - sprite_image: The visual representation of the cat.
        - current_direction: Direction the cat is moving (0 = right, 1 = left, 2 = up, 3 = down).
        - is_dead: Whether the cat is dead.
        - in_start_box: Whether the cat is in its starting box.
        - unique_id: Unique identifier for the cat.
        """
        self.x_position = x_position
        self.y_position = y_position
        self.center_x = self.x_position + 22
        self.center_y = self.y_position + 22
        self.target_position = target_position
        self.movement_speed = movement_speed
        self.sprite_image = sprite_image
        self.current_direction = current_direction
        self.is_dead = is_dead
        self.in_start_box = in_start_box
        self.unique_id = unique_id
        self.possible_turns, self.in_start_box = self.check_collisions()
        self.bounding_box = self.draw_cat()

    def draw_cat(self):
        """
        Draws the cat sprite on the screen based on its current state.
        Returns:
        - A rectangle representing the cat's collision box.
        """
        if (not power_up_active and not self.is_dead) or (cats_eaten[self.unique_id] and power_up_active and not self.is_dead):
            screen.blit(self.sprite_image, (self.x_position, self.y_position))
        elif power_up_active and not self.is_dead and not cats_eaten[self.unique_id]:
            screen.blit(spooked_image, (self.x_position, self.y_position))
        else:
            screen.blit(dead_image, (self.x_position, self.y_position))
        
        return pygame.Rect(self.center_x - 18, self.center_y - 18, 36, 36)

    def check_collisions(self):
        """
        Checks possible turns and determines if the cat is in the start box.
        Returns:
        - possible_turns: List of boolean values indicating available turns.
        - in_start_box: Boolean indicating if the cat is inside the start box.
        """
        tile_height = (HEIGHT - 50) // 32
        tile_width = WIDTH // 30
        collision_offset = 15
        self.possible_turns = [False, False, False, False]
        
        if 0 < self.center_x // tile_width < 29:
            if level[(self.center_y - collision_offset) // tile_height][self.center_x // tile_width] == 9:
                self.possible_turns[2] = True
            if level[self.center_y // tile_height][(self.center_x - collision_offset) // tile_width] < 3:
                self.possible_turns[1] = True
            if level[self.center_y // tile_height][(self.center_x + collision_offset) // tile_width] < 3:
                self.possible_turns[0] = True
            if level[(self.center_y + collision_offset) // tile_height][self.center_x // tile_width] < 3:
                self.possible_turns[3] = True

        if 350 < self.x_position < 550 and 370 < self.y_position < 480:
            self.in_start_box = True
        else:
            self.in_start_box = False
        
        return self.possible_turns, self.in_start_box

    def move_cat(self):
        """
        Moves the cat based on its current direction and speed, 
        and updates its position according to its target.
        """
        if self.current_direction == 0:  # Moving right
            if self.target_position[0] > self.x_position and self.possible_turns[0]:
                self.x_position += self.movement_speed
            elif not self.possible_turns[0]:
                if self.target_position[1] > self.y_position and self.possible_turns[3]:
                    self.current_direction = 3
                    self.y_position += self.movement_speed
                elif self.target_position[1] < self.y_position and self.possible_turns[2]:
                    self.current_direction = 2
                    self.y_position -= self.movement_speed
                elif self.target_position[0] < self.x_position and self.possible_turns[1]:
                    self.current_direction = 1
                    self.x_position -= self.movement_speed
        elif self.current_direction == 1:  # Moving left
            if self.target_position[0] < self.x_position and self.possible_turns[1]:
                self.x_position -= self.movement_speed
        elif self.current_direction == 2:  # Moving up
            if self.target_position[1] < self.y_position and self.possible_turns[2]:
                self.y_position -= self.movement_speed
        elif self.current_direction == 3:  # Moving down
            if self.target_position[1] > self.y_position and self.possible_turns[3]:
                self.y_position += self.movement_speed
        
        # Handle wrapping around the screen
        if self.x_position < -30:
            self.x_position = 900
        elif self.x_position > 900:
            self.x_position -= 30
        
        return self.x_position, self.y_position, self.current_direction


# Example usage of the `EnemyCat` class
# Initialization and rendering should be done within the game loop.
