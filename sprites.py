import arcade
import math
from random import random
from constants import *

class PlayerSprite(arcade.Sprite):
    def __init__(self, posX):
        super().__init__()
        #load character tileset
        self.sprites = arcade.load_spritesheet("resources/player_tile.png", 20, 32, 3, 12)
        self.texture = self.sprites[0]
        self.scale = 2
        self.center_x = posX
        self.center_y = SCREEN_HEIGHT / 2
        self.change_y = 0

    def update_movement_texture(self):
        """Change the texture based on movement."""
        if self.change_y > 0:
            # Moving up
            self.texture = self.sprites[MOVE_UP_TEXTURE_INDEX]
        elif self.change_y < 0:
            # Moving down
            self.texture = self.sprites[MOVE_DOWN_TEXTURE_INDEX]
        elif self.change_x > 0:
            self.texture = self.sprites[MOVE_RIGHT_TEXTURE_INDEX]
        elif self.change_x < 0:
            self.texture = self.sprites[MOVE_LEFT_TEXTURE_INDEX]
        else:
            # No movement (idle)
            self.texture = self.sprites[IDLE_TEXTURE_INDEX]

    def on_update(self, delta_time):
        self.update()
        self.update_movement_texture()
        if self.center_y < self.height / 2:
            self.center_y = self.height / 2
        elif self.center_y > SCREEN_HEIGHT - self.height / 2:
            self.center_y = SCREEN_HEIGHT - self.height / 2

#Author: Santoniche from open game art
class OvenSprite(arcade.Sprite):
    def __init__(self):
        super().__init__("resources/oven.png")
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.change_y = 0
        self.scale = 1.5

    def on_update(self, delta_time):
        self.update()
        if self.center_y < self.height / 2:
            self.center_y = self.height / 2
        elif self.center_y > SCREEN_HEIGHT - self.height / 2:
            self.center_y = SCREEN_HEIGHT - self.height / 2

    def cook(self, food):
        food.cook()

#from Bluerobin2 on open game art
class FoodTableSprite(arcade.Sprite):
    def __init__(self):
        super().__init__("resources/tabletop_egg.png")
        self.center_x = SCREEN_WIDTH - 32
        self.center_y = SCREEN_HEIGHT - 100
        self.change_y = 0
        self.scale = 1.5

    def on_update(self, delta_time):
        self.update()

# Food resources credit to ghostpixxells on itch.io
class Food(arcade.Sprite):
    def __init__(self, target):
        super().__init__("resources/egg_raw.png")
        self.target = target
        self.center_x = self.target.center_x
        self.center_y = self.target.center_y
        self.cooked = False
        self.nutrition = 40

    def on_update(self, delta_time):
        self.update()
        #follow target
        self.center_x = self.target.center_x
        self.center_y = self.target.center_y

    def cook(self):
        self.set_texture(0)
        self.texture = arcade.load_texture("resources/egg_fried.png")
        self.nutrition = 60

    def update_target(self, target):
        self.target = target

#from Bluerobin2 on open game art
class PlateTableSprite(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("resources/tabletop_plate.png")
        self.center_x = x
        self.center_y = y
        self.change_y = 0
        self.scale = 2
        self.food = None

    def on_update(self, delta_time):
        self.update()

    def add_food(self, food):
        food.update_target(self)
        self.food = food
    def has_food(self):
        return self.food != None
    def get_food(self):
        #pop food
        food = self.food
        self.food = None
        return food
    def serve(self, comunity):
        if self.food:
            comunity.giveFood(self.food)
            self.food = None
            return True
        return False