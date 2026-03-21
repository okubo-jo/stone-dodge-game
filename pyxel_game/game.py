import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
STONE_INTERVAL = 30
GAME_OVER_DISPLAY_TIME = 60
START_SCENE = "start"
PLAY_SCENE = "play"

class Stone:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        self.y += self.speed

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK)

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
        self.frame_count = 0
        self.score = 0
        self.stone_speed = 1

    def update_start_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.reset_play_scene()
            self.current_scene = PLAY_SCENE

    def update_play_scene(self):
        if self.is_collision:
            if self.game_over_display_timer > 0:
                self.game_over_display_timer -= 1
            else:
                self.current_scene = START_SCENE
            return

        # プレイヤー移動（速さアップ）
        move_speed = 2 if pyxel.btn(pyxel.KEY_SHIFT) else 1
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < SCREEN_WIDTH - 16:
            self.player_x += move_speed
        if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > 0:
            self.player_x -= move_speed

        # 石を追加
        if pyxel.frame_count % STONE_INTERVAL == 0:
            self.stones.append(Stone(pyxel.rndi(0, SCREEN_WIDTH - 8), 0, self.stone_speed))

        # 石落下と衝突判定
        for stone in self.stones.copy():
            stone.update()
            if (self.player_x - 4 <= stone.x <= self.player_x + 16 and
                self.player_y - 4 <= stone.y <= self.player_y + 16):
                self.is_collision = True
            if stone.y >= SCREEN_HEIGHT:
                self.stones.remove(stone)

        # スコア更新
        self.score += 1
        # 石の落下速度を徐々に増加
        if self.score % 200 == 0:
            self.stone_speed += 0.2

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if self.current_scene == START_SCENE:
            self.update_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()

    def draw_start_scene(self):
        pyxel.cls(pyxel.COLOR_NAVY)
        pyxel.text(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 10,
                   "落石回避ゲーム", pyxel.COLOR_YELLOW)
        pyxel.text(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 10,
                   "クリックでスタート", pyxel.COLOR_WHITE)

    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        for stone in self.stones:
            stone.draw()
        pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK)
        pyxel.text(5, 5, f"Score: {self.score}", pyxel.COLOR_WHITE)
        if self.is_collision:
            pyxel.text(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2,
                       "Game Over", pyxel.COLOR_RED)

    def draw(self):
        if self.current_scene == START_SCENE:
            self.draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.draw_play_scene()

App()