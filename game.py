# kob4zh Karmina Buensuceso
# jns9uqs Jordan Stallard
#
# This game will involve a girl who is trying to collect fresh apples. There will be fresh apples and apple cores
# continuously falling from a tree, and the girl's objective is to collect as many fresh apples as possible and avoid
# collecting apple cores. The girl moves left and right to both collect (touch) fresh apples and avoid (not touch)
# apple cores. If the girl collects an apple core, she will lose health, and if she collects too many (3), the game
# will be over. The game can be restarted as many times as possible to try again.
#
# REQUIRED FEATURES
#
# User Input
#   - left and right arrow keys to move the girl
#   - space to start the fall of the fresh apples and apple cores
#
# Game Over
#   - girl collects 3 apple cores, her health bar runs out, and game_over screen appears
#
# Small Enough Window
#   - game window is 800 width, 600 height
#
# Graphics/Images
#   - the tree, apple cores, fresh apples, and girl are images
#
# OPTIONAL FEATURES
#
# Restart from Game Over
#   - press space to restart the game
#   - the game is restarted when the fresh apples and apple cores start falling again
#
# Enemies
#   - apple cores are not to be collected
#   - if the girl collects (touches) the apple cores, the health bar decreases
#
# Collectibles
#   - fresh apples are to be collected
#   - every fresh apple collected (touched) adds 1 to the girl's score
#
# Health Bar
#   - the health bar is split into 3 sections, and each section disappears after 1 apple core is collected (touched)
#   - when the health bar is empty, a game_over screen appears

import pygame, gamebox, random

screen_width = 800
screen_height = 600
camera = gamebox.Camera(screen_width, screen_height)
left_border = gamebox.from_color(-10, 0, 'white', 1, screen_height * 2)
right_border = gamebox.from_color(screen_width + 10, 0, 'white', 1, screen_height * 2)

# https://www.gameart2d.com/cute-girl-free-sprites.html
girl = gamebox.from_image(screen_width // 2, screen_height - 65, 'girl.png')
girl.scale_by(0.215)

# https://www.subpng.com/png-i8kjk2/
tree = gamebox.from_image(screen_width // 2, 150, 'tree.png')
tree.scale_by(0.1)

grass = gamebox.from_color(screen_width // 2, screen_height, 'dark green', screen_width, 175)

fa_list = []
ac_list = []
def apple_position():
    '''
    randomly positions the fresh apples and apple cores appearing from the top of the screen
    '''
    for i in range(4):
        # https://www.flaticon.com/free-icon/apple_415733?term=apple&page=1&position=1&page=1&position=1&related_id=415733&origin=search
        fresh_apple = gamebox.from_image(random.randrange(100, screen_width - 100), random.randrange(-100, -30), 'fresh_apple.png')
        fresh_apple.scale_by(0.1)
        fa_list.append(fresh_apple)

        # https://www.flaticon.com/free-icon/core_2371799?term=apple%20core&page=1&position=1&page=1&position=1&related_id=2371799
        apple_core = gamebox.from_image(random.randrange(100, screen_width - 100), random.randrange(-100, -30), 'apple_core.png')
        apple_core.scale_by(0.1)
        ac_list.append(apple_core)
apple_position()

game_on = False
instructions = gamebox.from_text(screen_width // 2, screen_height // 3, 'USE LEFT/RIGHT ARROW KEYS TO MOVE. PRESS SPACE TO START.', 30, 'black')
game_over = gamebox.from_text(screen_width // 2, screen_height // 3, 'GAME OVER. PRESS SPACE TO RESTART.', 30, 'black')
points = 0

rec1 = gamebox.from_color(screen_width - 300, 50, 'green', 100, 25)
rec2 = gamebox.from_color(screen_width - 200, 50, 'green', 100, 25)
rec3 = gamebox.from_color(screen_width - 100, 50, 'green', 100, 25)
health_bar = [rec1, rec2, rec3]
hb_text = gamebox.from_text(screen_width - 315, 25, 'HEALTH', 25, 'black')

def start_game(keys):
    '''
    starts the game if space is pressed
    '''
    global game_on
    if pygame.K_SPACE in keys:
        game_on = True

def girl_movement(keys):
    '''
    moves the girl using the left and right arrow keys, and she cannot go off of the screen.
    '''
    if pygame.K_LEFT in keys:
        girl.x -= 6
    elif pygame.K_RIGHT in keys:
        girl.x += 6

    if girl.touches(left_border):
        girl.move_to_stop_overlapping(left_border)
    elif girl.touches(right_border):
        girl.move_to_stop_overlapping(right_border)

def apple_movement():
    '''
    allows the apples to fall from the top of the screen
    '''
    global fa_list, ac_list, points, health_bar

    for each_fa in fa_list:
        each_fa.yspeed = 5
        each_fa.move_speed()
        if each_fa.touches(girl):
            each_fa.y = random.randrange(-100, -30)
            each_fa.x = random.randrange(100, screen_width - 100)
            points += 1
        elif each_fa.y > screen_height:
            each_fa.y = random.randrange(-100, -30)
            each_fa.x = random.randrange(100, screen_width - 100)

    for each_ac in ac_list:
        each_ac.yspeed = 5
        each_ac.move_speed()
        if each_ac.touches(girl):
            each_ac.y = random.randrange(-100, -30)
            each_ac.x = random.randrange(100, screen_width - 100)
            if len(health_bar) > 0:
                health_bar.pop()
        elif each_ac.y > screen_height:
            each_ac.y = random.randrange(-100, -30)
            each_ac.x = random.randrange(100, screen_width - 100)

        for each_fa in fa_list:
            for each_ac in ac_list:
                each_fa.move_to_stop_overlapping(each_ac)

def end_apple_movement():
    '''
    ends the fall of the apples
    '''
    for each_fa in fa_list:
        each_fa.y = -30

    for each_ac in ac_list:
        each_ac.y = -30

def reset_globals():
    '''
    resets the game statistics
    '''
    global game_on, fa_list, ac_list, points, health_bar, game_over
    game_on = False
    fa_list = []
    ac_list = []
    points = 0
    health_bar = [rec1, rec2, rec3]
    game_over = gamebox.from_text(screen_width // 2, screen_height // 3, 'GAME OVER. PRESS SPACE TO RESTART.', 30, 'black')

def tick(keys):
    '''
    implements the elements to allow the game to work
    '''
    global instructions, game_over
    camera.clear('light blue')
    camera.draw(grass)
    camera.draw(tree)
    camera.draw(girl)
    camera.draw(instructions)
    start_game(keys)
    girl_movement(keys)
    if game_on:
        instructions = gamebox.from_text(screen_width // 2, screen_height // 3, '', 30, 'black')
        apple_movement()
    for each_fa in fa_list:
        camera.draw(each_fa)
    for each_ac in ac_list:
        camera.draw(each_ac)
    for each_rec in health_bar:
        camera.draw(each_rec)
    camera.draw(hb_text)
    if health_bar == []:
        camera.draw(game_over)
        end_apple_movement()
        if pygame.K_SPACE in keys:
            game_over = gamebox.from_text(screen_width // 2, screen_height // 3, '', 50, 'black')
            reset_globals()
            apple_position()
            apple_movement()
    point_counter = gamebox.from_text(100, 25, 'POINTS: ' + str(points), 25, 'black')
    camera.draw(point_counter)
    camera.display()

gamebox.timer_loop(30, tick)