import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
STONE_INTERVAL = 30
GAME_OVER_DISPLAY_TIME = 60
START_SCENE = "start"
PLAY_SCENE = "play"

class Stone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += 1

    def draw(self):
        pyxel.blt(self.x,  self.y, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="落石回避ゲーム")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")
        self.current_scene = START_SCENE
        pyxel.run(self.update, self.draw)

    def reset_play_scene(self):
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT * 4 // 5
        self.stones = []
        self.is_collision = False
        self.game_over_display_timer = GAME_OVER_DISPLAY_TIME
        
    def update_start_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.reset_play_scene()
            self.current_scene = PLAY_SCENE

    def update_play_scene(self):
        #ゲームオーバー時
        if self.is_collision:
            if self.game_over_display_timer > 0:
                self.game_over_display_timer -= 1
            else:
                self.current_scene = START_SCENE
            return
        
        #プレイヤーの移動コマンド
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < SCREEN_WIDTH - 12:
            self.player_x += 1
        elif pyxel.btn(pyxel.KEY_LEFT) and self.player_x > -4:
            self.player_x -= 1

        #石を追加
        if pyxel.frame_count % STONE_INTERVAL == 0:
            self.stones.append(Stone(pyxel.rndi(0, SCREEN_WIDTH - 8), 0))
        
        #石の落下コマンド
        for stone in self.stones.copy():
            stone.update()

            #衝突
            if (self.player_x <= stone.x <= self.player_x + 8 and
                self.player_y <= stone.y <= self.player_y + 8):
                self.is_collision = True

            #画面に出た石を削除
            if stone.y >= SCREEN_HEIGHT:
                self.stones.remove(stone)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.current_scene == START_SCENE:
            self.update_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()

    def draw_start_scene(self):
        pyxel.blt(0, 0, 0, 32, 0, 160, 120)
        pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10,
                   "Click to Start", pyxel.COLOR_PINK)

    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        #石
        for stone in self.stones:
            stone.draw()

        #プレイヤー
        pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16,
                  pyxel.COLOR_BLACK)
        
        if self.is_collision:
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2,
                       "Game Over", pyxel.COLOR_RED)
   
    def draw(self):
        if self.current_scene == START_SCENE:
            self.draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.draw_play_scene()
        
App()
