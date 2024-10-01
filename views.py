import arcade
import arcade.key
from utils import Items

class MenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view  # Save reference to the game view

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Buy Items Menu", self.window.width / 2, self.window.height - 50,
                         arcade.color.WHITE, 24, anchor_x="center")
        arcade.draw_text("O: Oven -- 100$", self.window.width / 2, self.window.height - 200,
                         arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("S: Super Oven -- 300$", self.window.width / 2, self.window.height - 230,
                         arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("P: Plates -- 200$", self.window.width / 2, self.window.height - 260,
                         arcade.color.WHITE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        # Close the menu when the player presses the M key again
        if key == arcade.key.ESCAPE or key == arcade.key.M:
            self.window.show_view(self.game_view)
        if key == arcade.key.O:
            self.game_view.buy(Items.OVEN)
            self.window.show_view(self.game_view)
        if key == arcade.key.S:
            self.game_view.buy(Items.SUPER_OVEN)
            self.window.show_view(self.game_view)
        if key == arcade.key.P:
            self.game_view.buy(Items.PLATE_TABLE)
            self.window.show_view(self.game_view)
