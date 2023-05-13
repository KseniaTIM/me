import arcade
import os
from pyglet.math import Vec2
import random


scr_wid = 1600
scr_heig = 1000
scr_title = "Skateboarder"

# Player_options
player_size = 0.8
enemy_size = 3
tile_size = 0.8
player_speed = 5
player_run = 7
player_left = 0
player_right = 1
UPDATES_PER_FRAME = 4
CAMERA_SPEED = 0.1

def load_texture_pair(filename):
    return [
        arcade.load_texture(filename, flipped_horizontally=True),
        arcade.load_texture(filename)
    ]

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        # Default to face-right
        self.character_face_direction = player_left
        self.scale = player_size

        self.textures = []
        self.cur_texture = 0

        main_path = "sprites/"
        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair("sprites/boy_idle.png")


        # Load textures for walking
        self.walk_textures = []
        for i in range(24):
            texture = load_texture_pair(f"{main_path}walk/walk_{i}.png")
            self.walk_textures.append(texture)

        self.run_textures = []
        for i in range(24):
            texture = load_texture_pair(f"{main_path}run/run_{i}.png")
            self.run_textures.append(texture)


    def update_animation(self, delta_time: float = 1 / 60):

        # flip face left or right
        if self.change_x < 0 and self.character_face_direction == player_left:
            self.character_face_direction = player_right
        elif self.change_x > 0 and self.character_face_direction == player_right:
            self.character_face_direction = player_left

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Running animation
        if not self.change_x == 0 and not (self.change_x == player_speed or self.change_x == -player_speed):
            self.cur_texture += 1
            if self.cur_texture > 23 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.run_textures[frame][direction]

        if self.change_x == player_speed or self.change_x == -player_speed:
            self.cur_texture += 1
            if self.cur_texture > 23 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.walk_textures[frame][direction]



class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.facing_direction = player_right

        self.cur_texture = 0
        self.scale = enemy_size


        self.idle_texture_pair = load_texture_pair("sprites/enemy.png")

        self.texture = self.idle_texture_pair[0]


class Level(arcade.Window):

     def __init__(self):
        super().__init__(scr_wid, scr_heig, scr_title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.scene = None

        # lists_____________

        self.player_sprite_list = None
        self.enemy_sprite_list = None
       # bg______________

        self.background = None
        self.grass = None
        arcade.set_background_color(arcade.color.AMAZON)

        # player______________

        self.player_sprite = None
        self.score = 0
        self.won = False

        #keyboard______________

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shift_pressed = False

        self.camera_sprites = arcade.Camera(scr_wid, scr_heig)
        self.camera_gui = arcade.Camera(scr_wid, scr_heig)
        
        self.filter_on = True


        # Create the crt filter
        self.crt_filter = arcade.experimental.CRTFilter(scr_wid, scr_heig,
                                                        resolution_down_scale=5.0,
                                                        hard_scan=-8.0,
                                                        hard_pix=-3.0,
                                                        display_warp= Vec2(1.0 / 32.0, 1.0 / 24.0),
                                                        mask_dark=0.5,
                                                        mask_light=1.5)
        

        self.collect_coin_sound = arcade.load_sound("sprites/getpoint.wav")
        self.game_over_sound = arcade.load_sound("sprites/gong.wav")
        self.win_sound = arcade.load_sound("sprites/levelup2.wav")

     def setup(self):
        self.draw_text_timer = 5.0
        self.scene = arcade.Scene()

        # bg________________

        self.background = arcade.load_texture("sprites/bg/bg_station.png")

        # player_______________
        self.player_sprite_list = arcade.SpriteList()
        self.enemy_sprite_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        self.score = 0

        for i in range (15):
            coin = arcade.Sprite("sprites/coin.png", 0.03)
            coin.center_x = random.randrange(-6400, 6400, random.randrange(1000, 1600))
            coin.center_y = 250
            self.coin_list.append(coin)


        self.player_sprite = Player()
        self.player_sprite.center_x = 200
        self.player_sprite.center_y = 320

        self.player_sprite_list.append(self.player_sprite)


        self.enemy_sprite = Enemy()
        self.enemy_sprite.center_x = 3600
        self.enemy_sprite.center_y = 320
        self.enemy_sprite_list.append(self.enemy_sprite)


        self.enemy_start()
        
     def draw(self):
        self.clear()
        self.camera_sprites.use()
        arcade.start_render()
        for i in range(-12800, 12800, 1600):
            arcade.draw_lrwh_rectangle_textured(i, 0,scr_wid, scr_heig,self.background)
        self.scene.draw()
        self.coin_list.draw()
        self.player_sprite_list.draw()
        self.enemy_sprite_list.draw()

     
     def on_draw(self):
        """ Render the screen. """

        if self.filter_on:
            # CRT filter
            self.crt_filter.use()
            self.crt_filter.clear()
            self.draw()

            self.use()
            self.clear()

            self.crt_filter.draw()
        else:
            # Draw CRT into the screen
            self.use()
            self.clear()
            self.draw()
        
        self.camera_gui.use()

        score_text = f"coins collected: {self.score}"
        arcade.draw_text(
            score_text,
             10,
            self.height - 25,
            arcade.csscolor.WHITE,
            18,
            font_name="Kenney Mini Square"
        )
        arcade.draw_text(
            "A, D - move character\nSHIFT - sprint\nE - collect coin",
            10,
            self.height - 70,
            arcade.csscolor.WHITE,
            18,
            multiline=True,
            width=300,
            font_name="Kenney Mini Square"
        )

        if self.draw_text_timer > 0.0:
            arcade.draw_text(
                    "Tip: stand still when approached by a train",
                    self.width // 2,
                    self.height // 2 + 300,
                    arcade.csscolor.WHITE,
                    36,
                    font_name="Kenney Mini Square",
                    anchor_x="center",
                    )
        
        if self.won:
            arcade.draw_rectangle_filled(self.width // 2,
                                    self.height // 2,
                                    self.width,
                                    self.height,
                                    arcade.color.ORANGE_PEEL)
            arcade.draw_text(
                        "YOU WON",
                        self.width // 2,
                        self.height // 2,
                        arcade.csscolor.WHITE,
                        72,
                        font_name="Kenney Mini Square",
                        anchor_x="center",
                        )
            self.setup()
            

     def update_player_movement(self):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
       

        if self.left_pressed and not self.right_pressed:           
            self.player_sprite.change_x = -player_speed
            if self.shift_pressed:
                self.player_sprite.change_x = self.player_sprite.change_x * 2

        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = player_speed
            if self.shift_pressed:
                self.player_sprite.change_x = self.player_sprite.change_x * 2


     def enemy_start(self):
        if self.enemy_sprite.change_x == 0:
            self.enemy_sprite.change_x = player_speed * 3
      
     def on_update(self, delta_time):

        self.enemy_sprite_list.update()
        self.player_sprite_list.update()
        self.player_sprite_list.update_animation()

        self.draw_text_timer -= delta_time
        
        player_collision_list = arcade.check_for_collision_with_list(
            self.player_sprite,
            self.enemy_sprite_list
        )


        for collision in player_collision_list:

            if self.enemy_sprite_list in collision.sprite_lists:
                if not self.player_sprite.change_x == 0:   
                    arcade.play_sound(self.game_over_sound)
                    self.setup()
                    return

        #boundaries
        if self.player_sprite.center_x <= -9600:
            self.player_sprite.center_x = -9600
        if self.player_sprite.center_x >= 9600:
            self.player_sprite.center_x = 9600
        


        if self.enemy_sprite.center_x >= 9600 or self.enemy_sprite.center_x <= -9600:
            self.enemy_sprite.change_x *= -1

        self.scroll_to_player()

        if self.score >=10:
            arcade.play_sound(self.win_sound)
            self.won=True
            self.score -= 1

     def scroll_to_player(self):

        position = Vec2(self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 3.1)
        self.camera_sprites.move_to(position, CAMERA_SPEED)  

     def on_key_press(self, key, modifiers):
        

        if key == arcade.key.A:
            self.left_pressed = True
            self.update_player_movement()
        elif key == arcade.key.D:
            self.right_pressed = True
            self.update_player_movement()
        elif  modifiers == arcade.key.MOD_SHIFT:
            self.shift_pressed = True
            self.update_player_movement()
        elif key == arcade.key.E:
            self.search()
            
            

     def on_key_release(self, key, modifiers):
        if  modifiers == arcade.key.MOD_SHIFT:
            self.shift_pressed = False
            self.update_player_movement()
        elif key == arcade.key.A:
            self.left_pressed = False
            self.shift_pressed = False
            self.update_player_movement()
        elif key == arcade.key.D:
            self.right_pressed = False
            self.shift_pressed = False
            self.update_player_movement()   

     def search(self):
         pickable_coins = arcade.check_for_collision_with_list(
             self.player_sprite, self.coin_list
         )
         for sprite in pickable_coins:
            sprite.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.collect_coin_sound)


def main():

    open_game = Level()
    open_game.setup()
    arcade.run()


if __name__ == "__main__":
    main()