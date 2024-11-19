import arcade
import arcade.key
import math
from sprites import *
from constants import *
from views import MenuView, InitView
from agent import Comunity
from restaurant import Restaurant
from utils import *


class ComuniCook(arcade.View):
    def __init__(self):
        super().__init__()
        # set up the window
        arcade.set_background_color(arcade.color.GRAY)
        self.background = arcade.load_texture("resources/background.png")

        # set up obj lists
        self.entities = arcade.SpriteList()
        self.ovens = []
        self.plate_tables = []
        # create objects
        oven = Oven(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.food_table = FoodTable()
        self.player = Player(100)
        self.assisants = []
        plate_table = PlateTable(50, 70)
        # add objects to lists
        self.entities.append(oven)
        self.entities.append(self.player)
        self.entities.append(self.food_table)
        self.entities.append(plate_table)
        self.ovens.append(oven)
        self.plate_tables.append(plate_table)

        # Game state
        self.restaurant = Restaurant(self.plate_tables, self.entities)
        self.comunity = Comunity(self.restaurant)
        # PLAYER PHYSICS ENGINE
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.entities)
        self.setup()
        # UI
        self.money_text = None
        self.comunity_text = None
        self.happiness_text = None
        self.queue_text = None
        self.how_to_text = None
        self.hunger_texts = []
        self.create_UI_texts()
        # others
        self.foods = arcade.SpriteList()

    def setup(self):
        self.walls = arcade.SpriteList()
        left_wall = arcade.SpriteSolidColor(
            1, SCREEN_HEIGHT, arcade.color.BLACK)
        left_wall.center_x = 0
        left_wall.center_y = SCREEN_HEIGHT / 2
        self.walls.append(left_wall)
        right_wall = arcade.SpriteSolidColor(
            1, SCREEN_HEIGHT, arcade.color.BLACK)
        right_wall.center_x = SCREEN_WIDTH
        right_wall.center_y = SCREEN_HEIGHT / 2
        self.walls.append(right_wall)
        top_wall = arcade.SpriteSolidColor(
            SCREEN_WIDTH, 1, arcade.color.BLACK)
        top_wall.center_x = SCREEN_WIDTH / 2
        top_wall.center_y = SCREEN_HEIGHT
        self.walls.append(top_wall)
        bottom_wall = arcade.SpriteSolidColor(
            SCREEN_WIDTH, 1, arcade.color.BLACK)
        bottom_wall.center_x = SCREEN_WIDTH / 2
        bottom_wall.center_y = 0
        self.walls.append(bottom_wall)
        self.entities.extend(self.walls)

    def create_UI_texts(self):
        self.money_text = arcade.Text(
            text=f"Money: {math.floor(self.restaurant.get_money())}",
            start_x=SCREEN_WIDTH - 120,
            start_y=SCREEN_HEIGHT - 30,
            color=arcade.color.GREEN_YELLOW,
            font_size=14
        )

        self.comunity_text = arcade.Text(
            text=f"Comunity: {self.comunity.get_size()} people",
            start_x=SCREEN_WIDTH - 500,
            start_y=SCREEN_HEIGHT - 30,
            color=arcade.color.GREEN_YELLOW,
            font_size=14
        )

        self.happiness_text = arcade.Text(
            text=f"Happiness: {self.comunity.get_happiness()}",
            start_x=20,
            start_y=SCREEN_HEIGHT - 30,
            color=arcade.color.GREEN_YELLOW,
            font_size=14
        )

        self.queue_text = arcade.Text(
            text=f"Queue: {self.restaurant.get_queue_size()}",
            start_x=SCREEN_WIDTH / 2,
            start_y=SCREEN_HEIGHT - 30,
            color=arcade.color.GREEN_YELLOW,
            font_size=14
        )

        self.how_to_text = arcade.Text(
            text="Press SPACE to interact",
            start_x=SCREEN_WIDTH / 2 -80,
            start_y=15,
            color=arcade.color.GREEN_YELLOW,
            font_size=14
        )

    def draw_UI(self):
        # Draw all UI text objects
        self.money_text.draw()
        self.comunity_text.draw()
        self.happiness_text.draw()
        self.queue_text.draw()
        self.how_to_text.draw()
        self.draw_hunger()

    def draw_hunger(self):
        top_queue = self.restaurant.get_top_queue()

        for i, person in enumerate(top_queue):
            if i < len(self.hunger_texts):
                self.hunger_texts[i].text = f"{
                    i+1}: {math.floor(person.hunger)}"
            else:
                hunger_text = arcade.Text(
                    text=f"{i+1}: {math.floor(person.hunger)}",
                    start_x=20,
                    start_y=SCREEN_HEIGHT - 60 - i * 30,
                    color=arcade.color.GREEN_YELLOW,
                    font_size=14
                )
                self.hunger_texts.append(hunger_text)

        if len(self.hunger_texts) > len(top_queue):
            self.hunger_texts = self.hunger_texts[:len(top_queue)]

        for hunger_text in self.hunger_texts:
            hunger_text.draw()

    def update_UI_texts(self):
        self.money_text.text = f"Money: {
            math.floor(self.restaurant.get_money())}"
        self.comunity_text.text = f"Comunity: {
            self.comunity.get_size()} people"
        self.happiness_text.text = f"Happiness: {
            self.comunity.get_happiness()}"
        self.queue_text.text = f"Queue: {self.restaurant.get_queue_size()}"

    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                    SCREEN_WIDTH, SCREEN_HEIGHT,
                                    self.background)
        self.entities.draw()
        self.foods.draw()
        self.draw_UI()

    def on_update(self, delta_time):
        self.entities.on_update(delta_time)
        self.comunity.update(delta_time)
        self.restaurant.update(delta_time)
        self.foods.on_update(delta_time)
        self.update_UI_texts()
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
        objects = self.ovens + [self.food_table] + self.plate_tables
        for obj in objects:
            distance = arcade.get_distance_between_sprites(self.player, obj)
            if distance < proximity_threshold:
                if isinstance(obj, Oven):
                    if self.player.hasFood():
                        obj.cook(self.player.giveFood())
                    elif obj.is_ready():
                        self.player.receiveFood(obj.return_food(self.player))
                    break
                elif isinstance(obj, FoodTable):
                    self.foods.append(Food(self.player))
                    self.player.receiveFood(self.foods[-1])
                    break
                elif isinstance(obj, PlateTable):
                    if self.player.hasFood():
                        obj.add_food(self.player.giveFood())
                    break

    def buy(self, item):
        if not self.restaurant.buy(item):
            return
        match item:
            case Items.OVEN:
                self.addItem(Oven, self.ovens)
            case Items.SUPER_OVEN:
                self.addItem(SuperOven, self.ovens)
            case Items.PLATE_TABLE:
                self.addItem(PlateTable, self.plate_tables)
            case Items.ASSISTANT:
                new_assistant = Assistant(200, [self.food_table], self.ovens, self.plate_tables, self.entities)
                self.entities.append(new_assistant)
                self.assisants.append(new_assistant)


    def addItem(self, item, item_list):
        if len(item_list) > 5:
            return
        last_item = item_list[-1]
        new_x = last_item.center_x
        new_y = last_item.center_y + 160

        if new_y > SCREEN_HEIGHT - 100:
            new_row_item = item_list[len(item_list) - 2 % 3]
            new_x = new_row_item.center_x + 160
            new_y = new_row_item.center_y

        new_item = item(new_x, new_y)
        self.entities.append(new_item)
        item_list.append(new_item)


if __name__ == '__main__':

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = ComuniCook()
    init_view = InitView(game_view)
    window.show_view(init_view)
    arcade.run()
