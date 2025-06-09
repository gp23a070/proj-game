import pygame
import sys
import random
import time
import tkinter as tk
from tkinter import simpledialog
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
# 名前を入力する関数
def get_player_name():
    root = tk.Tk()
    root.withdraw()  # Tkinterウィンドウを非表示にする
    player_name = simpledialog.askstring("名前入力", "プレイヤーの名前を入力してください:")
    root.destroy()
    return player_name if player_name else "プレイヤー"

# ゲーム開始時に名前を取得
player_name = get_player_name()


# Pygame全体の初期化
pygame.init()
pygame.font.init()

# フォントパスとサイズを指定して日本語フォントを読み込む
# 日本語フォントのパスを正しい場所に変更
japanese_font_path = r"font\gl-novantiquaminamoto\GL-NovantiquaMinamoto-main\fonts\ttf\GL-NovantiquaMinamoto.ttf"
japanese_font = pygame.font.Font(japanese_font_path, 74)
small_japanese_font = pygame.font.Font(japanese_font_path, 36)


# スタート画面の日本語表示を追加
def show_start_screen():
    screen.fill(WHITE)
    title_text = japanese_font.render("捕食者と獲物", True, BLACK)
    start_text = small_japanese_font.render("キーを押してスタート", True, BLACK)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 400))
    pygame.display.flip()
    start_sound.play()
    wait_for_key()

# Pygameの初期化
pygame.init()

# 画面の幅と高さ
screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("捕食者と獲物のシミュレーション")  

# BGMの読み込みと再生
pygame.mixer.init()
pygame.mixer.music.load(r"sound\Cat_life.mp3")  # パスの指定
pygame.mixer.music.play(-1)  # ループ再生

# ゲームスタート音の読み込み
start_sound = pygame.mixer.Sound(r"sound\笛1.mp3")  # ゲームスタート音
# ボーナスタイムの音の読み込み
bonus_sound = pygame.mixer.Sound(r"sound\BATTLE_BONUS_3000獲得音.mp3")
#捕獲時の音
catch_sound = pygame.mixer.Sound(r"sound\捕獲音.mp3")  
# 背景画像の読み込み
background_image = pygame.image.load(r"image\background.jpg")  # 背景画像のパスを設定
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# 色の定義
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 画像の読み込み
ufo_image = pygame.image.load(r"image\UFO.png")
ufo_image = pygame.transform.scale(ufo_image, (125, 125))
ufo1_image = pygame.image.load(r"image\UFO_hikari.png")
ufo1_image = pygame.transform.scale(ufo1_image, (125, 125))
prey_large_image = pygame.image.load(r"image\cow-2.png")
prey_large_image = pygame.transform.scale(prey_large_image, (100, 100))
prey_medium_image = pygame.image.load(r"image\buta.png")
prey_medium_image = pygame.transform.scale(prey_medium_image, (80, 80))
prey_small_image = pygame.image.load(r"image\niwatori.png")
prey_small_image = pygame.transform.scale(prey_small_image, (60, 60))

# ボーナスタイムフレーム画像の読み込みを先に行う
bonus_frame_image = pygame.image.load(r"image\bonus_t.png").convert_alpha()
bonus_frame_image = pygame.transform.scale(bonus_frame_image, (screen_width, screen_height))
bonus_frame_image.set_alpha(128)  # 透明度の設定

# フォントの定義
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# 捕食者クラスの定義
class Predator:
    def __init__(self):
        self.size = 30
        self.position = pygame.Vector2(screen_width // 2, screen_height // 2)
        self.image = ufo_image  # 画像の初期設定
        self.switch_time = None  # 画像切り替え時間の初期値

    def draw(self, screen):
        screen.blit(self.image, (int(self.position.x - self.image.get_width() // 2), 
                                 int(self.position.y - self.image.get_height() // 2)))

    def follow_mouse(self):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        self.position = mouse_position

    def check_collision(self, prey):
        distance = self.position.distance_to(prey.position)
        return distance < self.size + prey.size

    def switch_to_catch_image(self):  # 捕獲時の画像切り替え
        self.image = ufo1_image
        self.switch_time = time.time()

    def reset_image(self):  # 画像を元に戻す処理
        if self.switch_time and time.time() - self.switch_time > 0.3:
            self.image = ufo_image
            self.switch_time = None

# 獲物クラスの定義
class Prey:
    def __init__(self):
        self.size = 15
        self.position = pygame.Vector2(random.randint(screen_width // 4, screen_width * 3 // 4),
                                       random.randint(screen_height // 4, screen_height * 3 // 4))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 0.5
        self.score_value = 100

    def draw(self, screen):
        screen.blit(prey_medium_image, (int(self.position.x - prey_medium_image.get_width() // 2), 
                                 int(self.position.y - prey_medium_image.get_height() // 2)))

    def move(self, predator):
        distance_to_predator = self.position.distance_to(predator.position)
        if distance_to_predator < 1000:
            direction = self.position - predator.position
            if direction.length() != 0:
                direction = direction.normalize() * 0.025
                self.velocity += direction
        else:
            self.velocity += pygame.Vector2(random.uniform(-0.05, 0.05), random.uniform(-0.05, 0.05))
            if self.velocity.length() > 0.1:
                self.velocity = self.velocity.normalize() * 0.01

        self.position += self.velocity

        if self.position.x - self.size <= 0:
            self.position.x = self.size
            self.velocity.x *= -1
        elif self.position.x + self.size >= screen_width:
            self.position.x = screen_width - self.size
            self.velocity.x *= -1

        if self.position.y - self.size <= 0:
            self.position.y = self.size
            self.velocity.y *= -1
        elif self.position.y + self.size >= screen_height:
            self.position.y = screen_height - self.size
            self.velocity.y *= -1

# 速い獲物クラスの定義
class FastPrey(Prey):
    def __init__(self):
        super().__init__()
        self.size = 10
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 0.5
        self.score_value = 300

    def draw(self, screen):
        screen.blit(prey_small_image, (int(self.position.x - prey_small_image.get_width() // 2), 
                                      int(self.position.y - prey_small_image.get_height() // 2)))

# ランダムに動く獲物クラスの定義
class RandomPrey(Prey):
    def __init__(self):
        super().__init__()
        self.size = 20
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 0.25
        self.score_value = 200

    def move(self, predator):
        super().move(predator)
        if random.random() < 0.1:
            self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 0.1

    def draw(self, screen):
        screen.blit(prey_large_image, (int(self.position.x - prey_large_image.get_width() // 2), 
                                        int(self.position.y - prey_large_image.get_height() // 2)))

# スタート画面の表示
def show_start_screen():
    screen.fill(WHITE)
    title_text = japanese_font.render("捕食者と獲物", True, BLACK)
    name_text = small_japanese_font.render(f"プレイヤー: {player_name}", True, BLACK)
    start_text = small_japanese_font.render("キーを押してスタート", True, BLACK)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
    screen.blit(name_text, (screen_width // 2 - title_text.get_width() // 2, 600))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 400))
    
    # 獲物の画像とポイントを表示
    screen.blit(prey_medium_image, (screen_width // 2 - 200, 300))
    prey_score_text = small_japanese_font.render(f"100", True, BLACK)
    screen.blit(prey_score_text, (screen_width // 2 - 200 + 50, 300))

    screen.blit(prey_small_image, (screen_width // 2, 300))
    fast_prey_score_text = small_japanese_font.render(f"300", True, BLACK)
    screen.blit(fast_prey_score_text, (screen_width // 2 + 50, 300))

    screen.blit(prey_large_image, (screen_width // 2 + 200, 300))
    random_prey_score_text = small_japanese_font.render(f"200", True, BLACK)
    screen.blit(random_prey_score_text, (screen_width // 2 + 200 + 50, 300))

    pygame.display.flip()
    start_sound.play()
    wait_for_key()


# キーが押されるまで待機
def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

# 各獲物の捕獲数を追跡する辞書を追加

def save_and_get_top_scores(score, player_name, top_n=5):
    # 名前とスコアをファイルに追加で保存
    with open("scores.txt", "a", encoding="utf-8") as f:
        f.write(f"{player_name},{score}\n")
    
    # ファイルからスコアを読み込み
    with open("scores.txt", "r", encoding="utf-8") as f:
        scores = []
        for line in f:
            if line.strip():
                try:
                    name, score_str = line.strip().split(',')
                    scores.append((name, int(score_str)))
                except ValueError:
                    pass

    # スコアを降順にソートして上位5つを取得
    top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:top_n]
    return top_scores


# タイムアップ画面の表示
def show_game_over_screen(score):
    global player_name
    screen.fill(WHITE)
    game_over_text = japanese_font.render("タイムアップ", True, BLACK)
    score_text = small_japanese_font.render(f"最終スコア: {score}", True, BLACK)
    restart_text = small_japanese_font.render("キーを押してリスタート", True, BLACK)
    
    # 上位5スコアとプレイヤーネームの表示
    top_scores = save_and_get_top_scores(score, player_name)
    top_scores_text = [
        small_japanese_font.render(f"{i+1}位: {name} - {s}", True, BLACK)
        for i, (name, s) in enumerate(top_scores)
    ]

    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 5))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 3))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 1.5))

    for i, score_surface in enumerate(top_scores_text):
        screen.blit(score_surface, (screen_width // 2 - score_surface.get_width() // 2, screen_height // 1.5 + 40 + i * 30))

    pygame.display.flip()
    wait_for_key()
    player_name = get_player_name()  # ゲーム再開時に新しい名前を入力


# メインゲームループ
def game_loop():
    global catch_counts  # グローバル変数として宣言し、リセットする
    catch_counts = { "prey": 0, "fast_prey": 0, "random_prey": 0 }  # 捕獲数をリセット
    
    predator = Predator()
    preys = [random.choice([Prey, FastPrey, RandomPrey])() for _ in range(10)]
    score = 0

    start_time = time.time()
    game_duration = 60
    bonus_duration = 10
    cooldown_duration = 20

    is_bonus_active = False
    is_cooldown_active = False
    bonus_time_start = None
    cooldown_start_time = None
    last_score_check_time = time.time()
    score_in_last_10_seconds = 0

    clock = pygame.time.Clock()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > game_duration:
            show_game_over_screen(score)
            break

        if is_cooldown_active:
            if current_time - cooldown_start_time >= cooldown_duration:
                is_cooldown_active = False
                last_score_check_time = current_time
                score_in_last_10_seconds = 0
        elif is_bonus_active:
            if current_time - bonus_time_start >= bonus_duration:
                is_bonus_active = False
                is_cooldown_active = True
                cooldown_start_time = current_time
        else:
            if current_time - last_score_check_time >= 10:
                if score_in_last_10_seconds >= 2500:
                    is_bonus_active = True
                    bonus_time_start = current_time
                    bonus_sound.play()
                score_in_last_10_seconds = 0
                last_score_check_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        # 背景を描画し、捕食者をマウス位置に合わせる
        screen.blit(background_image, (0, 0))
        predator.follow_mouse()

        for prey in preys[:]:
            prey.move(predator)
            if predator.check_collision(prey):
                # 捕獲した獲物の種類を判別し、カウントアップ
                if isinstance(prey, Prey):
                    catch_counts["prey"] += 1
                elif isinstance(prey, FastPrey):
                    catch_counts["fast_prey"] += 1
                elif isinstance(prey, RandomPrey):
                    catch_counts["random_prey"] += 1

                preys.remove(prey)
                preys.append(random.choice([Prey, FastPrey, RandomPrey])())
                score += prey.score_value
                score_in_last_10_seconds += prey.score_value
                predator.switch_to_catch_image()  # 捕獲時に画像を切り替え
                catch_sound.play()  # 獲物を捕まえたときの効果音

        # 捕獲画像を元に戻す処理
        predator.reset_image()

        # 捕食者と獲物を描画
        predator.draw(screen)
        for prey in preys:
            prey.draw(screen)

        score_text = small_japanese_font.render(f"スコア: {score}", True, BLACK)
        time_text = small_japanese_font.render(f"残り時間: {int(game_duration - elapsed_time)}秒", True, BLACK)
        name_text = small_japanese_font.render(f"プレイヤー: {player_name}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (screen_width - time_text.get_width() - 10, 10))
        screen.blit(name_text, (screen_width // 2 - name_text.get_width() // 2, 10))

        if is_bonus_active:
            screen.blit(bonus_frame_image, (0, 0))
            bonus_text = small_japanese_font.render("ボーナスタイム中!", True, BLACK)
            screen.blit(bonus_text, (screen_width // 2 - bonus_text.get_width() // 2, screen_height // 1.5))

        pygame.display.flip()
        clock.tick(60)

# ゲーム開始
show_start_screen()
start_sound.play()  # ゲーム開始時の効果音
while True:
    game_loop()