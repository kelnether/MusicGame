import pygame
import sys
from note import Note
from beatmap_generator import BeatmapGenerator
from background_manager import BackgroundManager

class RhythmGame:
    def __init__(self, bg_mode):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("高级节奏游戏")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.combo = 0
        self.font = pygame.font.SysFont("Arial", 24)
        self.lane_positions = [150, 300, 450, 600]
        self.lane_keys = {
            0: pygame.K_d,
            1: pygame.K_f,
            2: pygame.K_j,
            3: pygame.K_k
        }
        self.hit_window = 100
        self.perfect_window = 50

        try:
            self.note_skin = pygame.image.load("assets/note_skin.png").convert_alpha()
        except Exception as e:
            print("加载 note_skin 失败：", e)
            self.note_skin = None

        # 这里示例使用 beatmap_generator 从歌曲中生成 beatmap 数据
        generator = BeatmapGenerator("assets/background.mp3")
        self.beatmap = generator.generate()
        self.notes = []
        self.load_beatmap()

        self.start_time = pygame.time.get_ticks()
        try:
            pygame.mixer.music.load("assets/background.mp3")
            pygame.mixer.music.play()
        except Exception as e:
            print("加载音乐失败：", e)

        # 根据玩家选择创建背景管理对象
        if bg_mode == 'static':
            bg_file = "assets/background_static.png"
        else:
            bg_file = "assets/background_mv.mp4"
        self.bg_manager = BackgroundManager(bg_mode, bg_file, (self.WIDTH, self.HEIGHT))

    def load_beatmap(self):
        for note_info in self.beatmap:
            note = Note(note_info["lane"], note_info["time"], skin=self.note_skin)
            self.notes.append(note)

    def handle_key(self, key, current_time):
        for lane, lane_key in self.lane_keys.items():
            if key == lane_key:
                hit_note = None
                best_offset = float('inf')
                for note in self.notes:
                    if note.lane == lane and not note.hit:
                        offset = abs(note.hit_time - current_time)
                        if offset < best_offset and offset <= self.hit_window:
                            best_offset = offset
                            hit_note = note
                if hit_note:
                    hit_note.hit = True
                    if best_offset <= self.perfect_window:
                        self.score += 100
                        print("Perfect!")
                    else:
                        self.score += 50
                        print("Good!")
                    self.combo += 1
                else:
                    self.combo = 0
                    print("Miss!")

    def update_notes(self, current_time):
        for note in self.notes:
            note.update(current_time, self.hit_window)
        self.notes = [note for note in self.notes if not (note.hit or note.missed)]

    def draw_ui(self, current_time):
        bg_surface = self.bg_manager.get_background(current_time)
        self.screen.blit(bg_surface, (0, 0))
        for x in self.lane_positions:
            pygame.draw.line(self.screen, (0, 255, 0), (x - 40, 500), (x + 40, 500), 5)
        for note in self.notes:
            lane = note.lane
            x = self.lane_positions[lane]
            note.draw(self.screen, x, current_time)
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        combo_text = self.font.render(f"Combo: {self.combo}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(combo_text, (10, 40))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks() - self.start_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.handle_key(event.key, current_time)
            self.update_notes(current_time)
            self.draw_ui(current_time)
            self.clock.tick(60)
        pygame.quit()
        sys.exit()
