import arcade
import math
from random import random
from constants import *


class PlayerSprite(arcade.SpriteCircle):
    def __init__(self, posX):
        super().__init__(RADIUS, arcade.color.BLUE)
        self.center_x = posX
        self.center_y = SCREEN_HEIGHT / 2
        self.change_y = 0

    def on_update(self, delta_time):
        self.update()
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

#Author: Santoniche from open game art
class FoodTableSprite(arcade.Sprite):
    def __init__(self):
        super().__init__("resources/food_table_egg.png")
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

    def on_update(self, delta_time):
        self.update()
        #follow target
        self.center_x = self.target.center_x
        self.center_y = self.target.center_y

    def cook(self):
        self.set_texture(0)
        self.texture = arcade.load_texture("resources/egg_fried.png")

    def update_target(self, target):
        self.target = target


class PlateTableSprite(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("resources/table.png")
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
    def serve(self, comunity):
        if self.food:
            comunity.giveFood(self.food)
            self.food = None
            return True
        return False