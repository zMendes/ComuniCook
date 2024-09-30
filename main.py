import arcade
import arcade.key
from random import random
import math
from sprites import PlayerSprite, OvenSprite, FoodTableSprite, Food, PlateTableSprite
from constants import *
from views import MenuView
from agent import Comunity
from restaurant import Restaurant


class ComuniCook(arcade.View):
    def __init__(self):
        super().__init__()
        # set up the window
        arcade.set_background_color(arcade.color.GRAY)

        # set up obj lists
        self.entities = arcade.SpriteList()
        self.ovens = []
        self.plate_tables = []
        # create objects
        self.oven = OvenSprite()
        self.food_table = FoodTableSprite()
        self.player = PlayerSprite(100)
        plate_table = PlateTableSprite(50, 70)
        # add objects to lists
        self.entities.append(self.oven)
        self.entities.append(self.player)
        self.entities.append(self.food_table)
        self.entities.append(plate_table)
        self.ovens.append(self.oven)
        self.plate_tables.append(plate_table)

        # Game state
        self.restaurant = Restaurant(self.plate_tables)
        self.comunity = Comunity(self.restaurant)
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.entities)
        self.setup()
        # others
        self.food = None

    def setup(self):
        self.walls = arcade.SpriteList()
        left_wall = arcade.SpriteSolidColor(
            10, SCREEN_HEIGHT, arcade.color.BLACK)
        left_wall.center_x = 0
        left_wall.center_y = SCREEN_HEIGHT / 2
        self.walls.append(left_wall)
        right_wall = arcade.SpriteSolidColor(
            10, SCREEN_HEIGHT, arcade.color.BLACK)
        right_wall.center_x = SCREEN_WIDTH
        right_wall.center_y = SCREEN_HEIGHT / 2
        self.walls.append(right_wall)
        top_wall = arcade.SpriteSolidColor(
            SCREEN_WIDTH, 12, arcade.color.BLACK)
        top_wall.center_x = SCREEN_WIDTH / 2
        top_wall.center_y = SCREEN_HEIGHT
        self.walls.append(top_wall)
        bottom_wall = arcade.SpriteSolidColor(
            SCREEN_WIDTH, 12, arcade.color.BLACK)
        bottom_wall.center_x = SCREEN_WIDTH / 2
        bottom_wall.center_y = 0
        self.walls.append(bottom_wall)
        self.entities.extend(self.walls)

    def on_draw(self):
        arcade.start_render()
        self.entities.draw()
        self.draw_UI()
        if self.food:
            self.food.draw()

    def draw_UI(self):
        arcade.draw_text(f"Money: {math.floor(
            self.restaurant.get_money())}", SCREEN_WIDTH - 120, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14)
        arcade.draw_text(f"Comunity: {self.comunity.get_size(
        )} people", SCREEN_WIDTH - 500, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14)
        self.draw_hunger()
        arcade.draw_text(f"Happiness: {self.comunity.get_happiness(
        )}", 20, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14)
        arcade.draw_text(
            f"Queue: {self.restaurant.get_queue_size()}", SCREEN_WIDTH/2, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14)

    def draw_hunger(self):
        for i, person in enumerate(self.restaurant.get_top_queue()):
            arcade.draw_text(f"{i+1}: {math.floor(person.hunger)}",
                             20, SCREEN_HEIGHT - 60 - i * 30, arcade.color.WHITE, 14)

    # called 60 times per second to update game state
    def on_update(self, delta_time):
        self.entities.on_update(delta_time)
        self.comunity.update(delta_time)
        self.restaurant.update(delta_time)

        if self.food:
            self.food.on_update(delta_time)

        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # If the player presses a key, update the speed
        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.M:
            menu_view = MenuView(self)
            self.window.show_view(menu_view)
        elif key == arcade.key.SPACE:
            self.interact()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def interact(self):  # not the best way to do this
        proximity_threshold = 90

        for oven in self.ovens:
            distance_to_oven = arcade.get_distance_between_sprites(
                self.player, oven)
            if distance_to_oven < proximity_threshold and self.food:
                oven.cook(self.food)
                break

        distance_to_food_table = arcade.get_distance_between_sprites(
            self.player, self.food_table)
        if distance_to_food_table < proximity_threshold:
            self.food = Food(self.player)

        for plate_table in self.plate_tables:
            distance_to_plate_table = arcade.get_distance_between_sprites(
                self.player, plate_table)
            if distance_to_plate_table < proximity_threshold and self.food:
                plate_table.add_food(self.food)
                break

    def buy_plate_table(self):
        y = self.plate_tables[-1].center_y + 160
        x = self.plate_tables[-1].center_x
        if y > SCREEN_HEIGHT - 100:
            y = self.plate_tables[0].center_y
            x = self.plate_tables[0].center_x + 160
        plate_table = PlateTableSprite(x, y)
        self.entities.append(plate_table)
        self.plate_tables.append(plate_table)


if __name__ == '__main__':
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = ComuniCook()
    window.show_view(game_view)
    arcade.run()
