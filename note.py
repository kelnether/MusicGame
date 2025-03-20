import pygame

class Note:
    def __init__(self, lane, hit_time, skin=None):
        """
        :param lane: 音符所属轨道（0~3）
        :param hit_time: 预定的命中时间（毫秒）
        :param skin: 传入的皮肤贴图（Surface 对象），用于绘制该音符
        """
        self.lane = lane
        self.hit_time = hit_time
        self.hit = False
        self.missed = False
        self.width = 50
        self.height = 20
        self.spawn_y = -50
        self.hit_y = 500
        self.travel_time = 2000
        self.skin = skin  # 保存皮肤素材

    def get_position(self, current_time):
        spawn_time = self.hit_time - self.travel_time
        if current_time < spawn_time:
            return None
        progress = (current_time - spawn_time) / self.travel_time
        progress = min(progress, 1)
        y = self.spawn_y + progress * (self.hit_y - self.spawn_y)
        return y

    def update(self, current_time, hit_window=100):
        if not self.hit and current_time > self.hit_time + hit_window:
            self.missed = True

    def draw(self, screen, x, current_time):
        pos_y = self.get_position(current_time)
        if pos_y is not None:
            if self.skin:
                # 若提供皮肤，使用皮肤贴图
                # 这里假设皮肤大小与音符大小一致，可根据需要调整缩放
                rect = self.skin.get_rect(center=(x, pos_y + self.height // 2))
                screen.blit(self.skin, rect)
            else:
                # 默认绘制红色矩形
                pygame.draw.rect(screen, (255, 0, 0), (x - self.width // 2, pos_y, self.width, self.height))
