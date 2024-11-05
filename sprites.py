import arcade
import math
from random import random, randint
from constants import *


class Character(arcade.Sprite):
    def __init__(self, posX, posY, texture_path):
        super().__init__()
        self.sprites = arcade.load_spritesheet(texture_path, 20, 32, 3, 12)
        self.texture = self.sprites[0]
        self.scale = 2
        self.center_x = posX
        self.center_y = posY
        self.change_y = 0
        self.change_x = 0

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


class Player(Character):
    def __init__(self, posX):
        super().__init__(posX, SCREEN_HEIGHT / 2, "resources/player_tile.png")


# Character srpite author: Santoniche from open game art
class Assistant(Character):
    def __init__(self, posX, food_tables, ovens, plate_tables, entities):
        assistant_texture_number = randint(1, 3)
        assistant_texture = f"resources/assistant_{
            assistant_texture_number}.png"
        super().__init__(posX, SCREEN_HEIGHT / 2, assistant_texture)
        self.food_tables = food_tables
        self.ovens = ovens
        self.plate_tables = plate_tables
        self.state = "FETCH_FOOD"
        self.entities = entities
        self.food = None
        self.target_food_table = None
        self.target_oven = None
        self.target_plate_table = None

    def on_update(self, delta_time):
        """Update the assistant's state and behavior."""
        if self.state == "FETCH_FOOD":
            self.fetch_food()
        elif self.state == "COOK_FOOD":
            self.cook_food()
        elif self.state == "SERVE_FOOD":
            self.serve_food()
        elif self.state == "WAIT_FOR_COOKING":
            self.wait_for_cooking()
        self.update()

    def follow_sprite(self, sprite, speed=4):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """

        if self.center_y < sprite.center_y:
            self.center_y += min(speed, sprite.center_y - self.center_y)
            self.texture = self.sprites[MOVE_UP_TEXTURE_INDEX]
        elif self.center_y > sprite.center_y:
            self.center_y -= min(speed, self.center_y - sprite.center_y)
            self.texture = self.sprites[MOVE_DOWN_TEXTURE_INDEX]

        if self.center_x < sprite.center_x:
            self.center_x += min(speed, sprite.center_x - self.center_x)
            self.texture = self.sprites[MOVE_RIGHT_TEXTURE_INDEX]
        elif self.center_x > sprite.center_x:
            self.center_x -= min(speed, self.center_x - sprite.center_x)
            self.texture = self.sprites[MOVE_LEFT_TEXTURE_INDEX]

    def fetch_food(self):
        if self.target_food_table == None:
            self.target_food_table = self.food_tables[randint(
                0, len(self.food_tables) - 1)]
        self.follow_sprite(self.target_food_table)
        if arcade.check_for_collision(self, self.target_food_table):
            self.food = self.target_food_table.get_food()
            self.food.update_target(self)
            self.entities.append(self.food)
            if self.food:
                self.state = "COOK_FOOD"

    def cook_food(self):
        if self.target_oven == None:
            self.target_oven = self.ovens[randint(0, len(self.ovens) - 1)]
        if self.food:
            self.follow_sprite(self.target_oven)
            if arcade.check_for_collision(self, self.target_oven):
                is_cooking = self.target_oven.cook(self.food)
                if not is_cooking:
                    self.target_oven = None
                    return
                self.food = None
                self.state = "WAIT_FOR_COOKING"


    def wait_for_cooking(self):
        if self.target_oven.is_ready():
            # Retrieve the cooked food from the oven
            self.food = self.target_oven.return_food(self)
            self.state = "SERVE_FOOD"
            self.target_oven = None

    def serve_food(self):
        if self.target_plate_table == None:
            self.target_plate_table = self.plate_tables[randint(
                0, len(self.plate_tables) - 1)]
        if self.food:
            self.follow_sprite(self.target_plate_table)
            if arcade.check_for_collision(self, self.target_plate_table):
                added = self.target_plate_table.add_food(self.food)
                if not added:
                    self.target_plate_table = None
                    return
                self.food = None
                self.state = "FETCH_FOOD"
                self.target_food_table = None


class Oven(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("resources/oven.png")
        self.center_x = x
        self.center_y = y
        self.change_y = 0
        self.scale = 1.2
        self.food = None
        self.oven_speed = 1
        self.is_cooking = False

    def on_update(self, delta_time):
        if self.is_cooking:
            self.cooking(delta_time)

    def cook(self, food):
        if self.food:
            return False
        self.time_cooking = 0
        self.food = food
        food.update_target(self)
        self.is_cooking = True
        return True

    def cooking(self, delta_time):
        self.time_cooking += delta_time * self.oven_speed
        if self.time_cooking > self.food.time_to_cook:
            self.food.cook()
            self.is_cooking = False

    def return_food(self, person):
        food = self.food
        food.update_target(person)
        self.food = None
        return food

    def is_ready(self):
        return self.is_cooking == False and self.food != None


class SuperOven(Oven):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = arcade.load_texture("resources/super_oven.png")
        self.oven_speed = 3


class FoodTable(arcade.Sprite):  # from Bluerobin2 on open game art
    def __init__(self):
        super().__init__("resources/tabletop_egg.png")
        self.center_x = SCREEN_WIDTH - 32
        self.center_y = SCREEN_HEIGHT - 100
        self.change_y = 0
        self.scale = 1

    def on_update(self, delta_time):
        self.update()

    def get_food(self):
        food = Food(self)
        return food


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


class PlateTable(arcade.Sprite):  # from Bluerobin2 on open game art
    def __init__(self, x, y):
        super().__init__("resources/tabletop_plate.png")
        self.center_x = x
        self.center_y = y
        self.change_y = 0
        self.scale = 1
        self.food = None

    def on_update(self, delta_time):
        self.update()

    def add_food(self, food):
        if self.food:
            return False
        food.update_target(self)
        self.food = food
        return True

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
