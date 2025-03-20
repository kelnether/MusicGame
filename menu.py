# -*- coding: utf-8 -*-
import pygame
import pygame_menu
import sys
from game import RhythmGame  # 导入实际游戏的入口类
print(pygame_menu.__version__)

# 登录验证函数（此处仅简单判断用户名密码）
from db_manager import verify_user
def login_verification(username, password):
    return verify_user(username, password)

from db_manager import register_user
import pygame_menu

def register_screen(surface, clock):
    reg_menu = pygame_menu.Menu('Register New User', 800, 600, theme=pygame_menu.themes.THEME_BLUE)
    # 保存文本输入框的引用
    username_input = reg_menu.add.text_input('Username:', default='', widget_id='username')
    password_input = reg_menu.add.text_input('Password:', default='', password=True, widget_id='password')
    confirm_input = reg_menu.add.text_input('Confirm Password:', default='', password=True, widget_id='confirm')

    def register_action():
        # 直接使用保存的引用获取输入框的值
        username = username_input.get_value().strip()
        pwd1 = password_input.get_value().strip()
        pwd2 = confirm_input.get_value().strip()
        print("username:", username, "pwd1:", pwd1, "pwd2:", pwd2)  # 用于调试
        if not username or not pwd1 or not pwd2:
            print("All fields must be filled in.")
            return
        if pwd1 != pwd2:
            print("Passwords do not match.")
            return
        if register_user(username, pwd1):
            print("Registration successful. Please log in.")
            login_screen(surface, clock)
        else:
            print("Username already taken or registration failed.")

    reg_menu.add.button('Register', register_action)
    reg_menu.add.button('Back', lambda: login_screen(surface, clock))

    while reg_menu.is_enabled():
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit_game()
        reg_menu.mainloop(surface, disable_loop=True)
        pygame.display.update()


# 当玩家点击开始游戏后调用，实际中可传入歌曲参数启动游戏
def start_game(selected_song):
    print("Start Game, Song:", selected_song)
    # 这里创建游戏实例并启动游戏
    # 可根据歌曲信息调整游戏参数
    game = RhythmGame(bg_mode='static')  # 例如使用静态背景
    game.run()


# 设置功能（此处仅打印提示，可根据需要扩展）
def set_settings():
    print("进入设置界面")
    # 在此处添加设置功能


def exit_game():
    pygame.quit()
    sys.exit()


# 登录页面：显示用户名和密码输入框
def login_screen(surface, clock):
    login_menu = pygame_menu.Menu('login', 800, 600, theme=pygame_menu.themes.THEME_BLUE)
    # 直接保存文本输入框引用，指定 widget_id 便于后续获取
    username_input = login_menu.add.text_input('username:', default='', widget_id='username')
    password_input = login_menu.add.text_input('password:', default='', password=True, widget_id='password')
    # 添加注册按钮，进入注册页面
    login_menu.add.button('register', lambda: register_screen(surface, clock))

    def login_action():
        # 直接使用保存的引用获取输入值
        username = username_input.get_value().strip()
        password = password_input.get_value().strip()
        if login_verification(username, password):
            print("login success!")
            main_menu(surface, clock)  # 登录成功后进入主菜单
        else:
            print("incorrect username or password!")

    login_menu.add.button('login', login_action)
    login_menu.add.button('quit', pygame_menu.events.EXIT)

    # 循环显示登录页面
    while login_menu.is_enabled():
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit_game()
        login_menu.mainloop(surface, disable_loop=True)
        pygame.display.update()


# 主菜单：登录后显示开始游戏、设置、退出按钮
def main_menu(surface, clock):
    menu = pygame_menu.Menu('main menu', 800, 600, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Game Start', song_selection_menu, surface, clock)
    menu.add.button('settings', set_settings)
    menu.add.button('quit', pygame_menu.events.EXIT)
    while menu.is_enabled():
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit_game()
        menu.mainloop(surface, disable_loop=True)
        pygame.display.update()


# 歌曲选择页面：下拉列表选择歌曲
def song_selection_menu(surface, clock):
    # 模拟多首歌曲列表；实际中可动态加载
    songs = ['Song A', 'Song B', 'C', 'D']
    selection_menu = pygame_menu.Menu('select Songs', 800, 600, theme=pygame_menu.themes.THEME_BLUE)
    selection_menu.add.selector('Song:', [(song, song) for song in songs])

    def start_callback():
        data = selection_menu.get_input_data()
        selected_song = data.get('Song:')
        start_game(selected_song)  # 调用游戏启动函数

    selection_menu.add.button('Start', start_callback)
    selection_menu.add.button('back', main_menu, surface, clock)

    while selection_menu.is_enabled():
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit_game()
        selection_menu.mainloop(surface, disable_loop=True)
        pygame.display.update()


# 外部调用入口
def run_menu():
    pygame.init()
    surface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Main")
    clock = pygame.time.Clock()
    login_screen(surface, clock)


if __name__ == '__main__':
    run_menu()
