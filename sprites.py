import arcade
import math
from random import random
from constants import *


class PlayerSprite(arcade.Sprite):
    def __init__(self, posX):
        super().__init__()
        # load character tileset
        self.sprites = arcade.load_spritesheet(
            "resources/player_tile.png", 20, 32, 3, 12)
        self.texture = self.sprites[0]
        self.scale = 2
        self.center_x = posX
        self.center_y = SCREEN_HEIGHT / 2
        self.change_y = 0
        self.food = None

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

    def receiveFood(self, food):
        self.food = food

    def hasFood(self):
        return self.food != None

    def giveFood(self):
        food = self.food
        self.food = None
        return food
# Author: Santoniche from open game art


class OvenSprite(arcade.Sprite):
    def __init__(self):
        super().__init__("resources/oven.png")
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.change_y = 0
        self.scale = 1.5
        self.food = None
        self.isCooking = False

    def on_update(self, delta_time):
        if self.isCooking:
            self.cooking(delta_time)

    def cook(self, food):
        self.time_cooking = 0
        self.food = food
        food.update_target(self)
        self.isCooking = True

    def cooking(self, delta_time):
        self.time_cooking += delta_time
        if self.time_cooking > self.food.time_to_cook:
            self.food.cook()
            self.isCooking = False

    def return_food(self, person):
        food = self.food
        food.update_target(person)
        self.food = None
        return food

    def is_ready(self):
        return self.isCooking == False and self.food != None


class FoodTableSprite(arcade.Sprite):  # from Bluerobin2 on open game art
    def __init__(self):
        super().__init__("resources/tabletop_egg.png")
        self.center_x = SCREEN_WIDTH - 32
        self.center_y = SCREEN_HEIGHT - 100
        self.change_y = 0
        self.scale = 1.5

    def on_update(self, delta_time):
        self.update()


class Food(arcade.Sprite):  # Food resources credit to ghostpixxells on itch.io
    def __init__(self, target):
        super().__init__("resources/egg_raw.png")
        self.target = target
        self.center_x = self.target.center_x
        self.center_y = self.target.center_y
        self.time_to_cook = 3
        self.cooked = False
        self.nutrition = 40

    def on_update(self, delta_time):
        self.update()
        # follow target
        self.center_x = self.target.center_x
        self.center_y = self.target.center_y

    def cook(self):
        self.set_texture(0)
        self.texture = arcade.load_texture("resources/egg_fried.png")
        self.nutrition = 60

    def update_target(self, target):
        self.target = target


class PlateTableSprite(arcade.Sprite):  # from Bluerobin2 on open game art
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
        # pop food
        food = self.food
        self.food = None
        return food

    def serve(self, comunity):
        if self.food:
            comunity.giveFood(self.food)
            self.food = None
            return True
        return False
