# -*- coding: utf-8 -*-
import pygame
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip


class BackgroundManager:
    def __init__(self, mode, file_path, screen_size):
        """
        :param mode: 'static' 或 'video'
        :param file_path: 静态背景图片或视频文件路径
        :param screen_size: (width, height) 元组，屏幕尺寸
        """
        self.mode = mode
        self.file_path = file_path
        self.screen_size = screen_size
        if self.mode == 'static':
            self.background = pygame.image.load(file_path).convert()
            self.background = pygame.transform.scale(self.background, screen_size)
        elif self.mode == 'video':
            # 使用 moviepy 加载视频文件，并调整尺寸
            self.clip = VideoFileClip(file_path)
            self.clip = self.clip.resize(screen_size)
        else:
            raise ValueError("无效的背景模式，请选择 'static' 或 'video'")

    def get_background(self, current_time):
        """
        :param current_time: 游戏运行的当前时间（毫秒）
        :return: pygame.Surface 对象，当前背景画面
        """
        if self.mode == 'static':
            return self.background
        elif self.mode == 'video':
            # 将当前时间（毫秒）转换为秒，循环播放视频
            t = (current_time / 1000.0) % self.clip.duration
            # 从视频中获取当前帧（返回 numpy 数组，形状为 (H, W, 3)）
            frame = self.clip.get_frame(t)
            # 将 numpy 数组转换为 pygame.Surface
            # 注意：moviepy 返回的帧是 RGB 格式，而 pygame.surfarray.make_surface 要求数组形状为 (W, H, 3)
            frame = np.uint8(frame)
            surface = pygame.surfarray.make_surface(np.flipud(np.rot90(frame)))
            return surface
