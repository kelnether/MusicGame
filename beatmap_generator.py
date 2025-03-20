# -*- coding: utf-8 -*-
import librosa
import numpy as np
import random


class BeatmapGenerator:
    def __init__(self, song_path):
        """
        :param song_path: 歌曲文件路径，用于音频分析
        """
        self.song_path = song_path

    def generate(self):
        """
        分析音频文件，利用 Librosa 提取节拍信息，并生成 beatmap 数据列表。
        每个 beatmap 元素包含：
            - time: 节拍时刻，单位为毫秒
            - lane: 分配到的轨道（0~3），这里采用随机分配（实际可根据需要设计分配逻辑）
        返回示例：
            [{"time": 3123, "lane": 0}, {"time": 3321, "lane": 2}, ...]
        """
        # 加载音频，sr=None 表示保持原采样率
        y, sr = librosa.load(self.song_path, sr=None)

        # 使用 Librosa 的 beat_track 函数检测节拍
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        # 将帧转换为秒，再转换为毫秒
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        beat_times_ms = (beat_times * 1000).astype(int)

        # 生成 beatmap 数据，随机指定轨道（0~3）
        beatmap = []
        for t in beat_times_ms:
            lane = random.randint(0, 3)
            beatmap.append({"time": int(t), "lane": lane})
        return beatmap


# 以下代码仅供测试使用，可在独立运行时观察输出
if __name__ == "__main__":
    song_file = "assets/background.mp3"  # 请确保此路径和文件存在
    generator = BeatmapGenerator(song_file)
    beatmap = generator.generate()
    print("生成的 beatmap 数据：")
    for beat in beatmap:
        print(beat)
