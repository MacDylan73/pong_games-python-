import pygame
import random
import sys
import time
screen_width = 1400
screen_height = 800


# setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong v3 by Dylan Folscroft')
pygame.display.set_icon(pygame.image.load("pongicon.png"))
clock = pygame.time.Clock()

# creating fonts
title_button_font = pygame.font.SysFont('candara', 25, True, True)
title_font = pygame.font.SysFont('candara', 75, True, False)
settings_label_font = pygame.font.SysFont('candara', 30, True, False)
countdown_font = pygame.font.SysFont('candara', 100, True, False)


class Button:
    def __init__(self, text, width, height, pos, elevation, center_override):
        # main attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y = pos[1]
        self.center_override = center_override

        # top rect
        self.top_rect = pygame.Rect(pos, (width, height))
        if self.center_override:
            self.top_rect.centerx = (screen_width / 2)
        self.top_color = '#ffffff'

        # bottom rect
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        if self.center_override:
            self.bottom_rect.centerx = (screen_width / 2)
        self.bottom_color = '#808080'

        # text
        self.text_surf = title_button_font.render(text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation
        self.top_rect.y = self.original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        # button
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius= 10)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius= 10)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#808080'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed is True:
                    main_menu.check_input()
                    settings.check_input()
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#ffffff'


class SettingsButton:
    def __init__(self, text, width, height, pos, elevation, center_override, color, player, is_difficulty, is_game_to):
        # main attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y = pos[1]
        self.center_override = center_override
        self.select_color = color
        self.what_player = player
        self.is_difficulty = is_difficulty
        self.is_game_to = is_game_to
        self.cycle = ['EASY', 'MEDIUM', 'HARD', 'EXTREME', 'IMPOSSIBLE']
        self.cycle2 = ['3', '5', '7', '10']
        self.index = 0
        self.index2 = 0

        self.gui_sound = pygame.mixer.Sound('gui_click.wav')

        # top rect
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_rect_outline = self.top_rect.copy()
        if self.center_override:
            self.top_rect.centerx = (screen_width / 2)
        self.top_color = self.select_color

        # bottom rect
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        if self.center_override:
            self.bottom_rect.centerx = (screen_width / 2)
        self.bottom_color = '#808080'

        # text
        self.text_surf = title_button_font.render(text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation
        self.top_rect.y = self.original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        # button
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius= 10)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius= 10)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

        if self.select_color == settings.player1_color and self.what_player == 'player_1':
            pygame.draw.rect(screen, '#ffffff', self.top_rect_outline, 4, border_radius= 10)
        elif self.select_color == settings.player2_color and self.what_player == 'player_2':
            pygame.draw.rect(screen, '#ffffff', self.top_rect_outline, 4, border_radius=10)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.select_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True

            else:
                self.dynamic_elevation = self.elevation
                if self.pressed is True:
                    if self.what_player == 'player_1':
                        pygame.mixer.Sound.play(self.gui_sound)
                        settings.player1_color = self.select_color
                    elif self.what_player == 'player_2':
                        pygame.mixer.Sound.play(self.gui_sound)
                        settings.player2_color = self.select_color
                    elif self.is_difficulty:
                        settings.check_input()
                        if self.index < 4:
                            self.index += 1
                            self.text_surf = title_button_font.render(self.cycle[self.index], True, '#000000')
                            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
                        else:
                            self.index = 0
                            self.text_surf = title_button_font.render(self.cycle[self.index], True, '#000000')
                            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
                    elif self.is_game_to:
                        settings.check_input()
                        if self.index2 < 3:
                            self.index2 += 1
                            self.text_surf = title_button_font.render(self.cycle2[self.index2], True, '#000000')
                            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
                        else:
                            self.index2 = 0
                            self.text_surf = title_button_font.render(self.cycle2[self.index2], True, '#000000')
                            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = self.select_color
        if self.select_color == settings.player1_color and self.what_player == 'player_1':
            self.dynamic_elevation = 0
        elif self.select_color == settings.player2_color and self.what_player == 'player_2':
            self.dynamic_elevation = 0


class MainMenu:
    def __init__(self):
        self.play_button = Button('PLAY', 200, 40, ((screen_width / 2), 300), 5, True)
        self.settings_button = Button('SETTINGS', 200, 40, ((screen_width / 2), 400), 5, True)
        self.exit_button = Button('EXIT', 200, 40, ((screen_width / 2), 500), 5, True)
        self.title_surf = title_font.render('PONG V3', True, '#FFFFFF')
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.center = ((screen_width / 2), 150)
        self.creator_surf = settings_label_font.render('Created by Dylan Folscroft', True, '#ffffff')
        self.creator_surf_rect = self.creator_surf.get_rect()
        self.creator_surf_rect.center = 1150, 750

        self.gui_sound = pygame.mixer.Sound('gui_click.wav')

        # creating bg
        self.border = pygame.Rect((screen_width / 2, screen_height / 2), (screen_width - 10, screen_height - 10))
        self.border.center = (screen_width / 2, screen_height / 2)

        self.left_p_rect = pygame.Rect((self.border.left + 20, self.border.height / 2), (20, 100))
        self.right_p_rect = pygame.Rect((self.border.right - 40, self.border.height / 2), (20, 100))
        self.left_p_rect.centery = self.border.height / 2
        self.right_p_rect.centery = self.border.height / 2
        self.left_p_y = self.left_p_rect.y
        self.right_p_y = self.right_p_rect.y

        self.ball_rect = pygame.Rect((self.border.width / 2 - 10, self.border.height / 2 - 10), (20, 20))
        self.ball_rect.center = screen_width / 2, screen_height / 2
        self.ball_x = self.ball_rect.x
        self.ball_y = self.ball_rect.y

        self.horizontal = random.choice([-1, 1])
        self.vertical = random.choice([1, -1])

    def check_input(self):
        if game_states.current_state == 'MainMenu':
            if self.play_button.pressed:
                pygame.mixer.Sound.play(self.gui_sound)
                game_states.current_state = 'game'
                game.is_countdown = True
                game.start_countdown_time = pygame.time.get_ticks()
                game.l_score = 0
                game.r_score = 0
                game.speed_addition = 0
            elif self.settings_button.pressed:
                pygame.mixer.Sound.play(self.gui_sound)
                game_states.current_state = 'settings'
            elif self.exit_button.pressed:
                pygame.mixer.Sound.play(self.gui_sound)
                pygame.quit()
                sys.exit()

    def animate_bg(self):
        self.ball_x += self.horizontal * delta_time * game.speed
        self.ball_y += self.vertical * delta_time * game.speed
        round(self.ball_x)
        round(self.ball_y)
        self.ball_rect.topleft = (self.ball_x, self.ball_y)
        if self.ball_y < 5:
            self.ball_rect.top = self.border.top
            self.vertical *= -1
        elif self.ball_y > 775:
            self.ball_rect.bottom = self.border.bottom
            self.vertical *= -1

        if (self.left_p_rect.centery < self.ball_rect.centery and self.ball_x < 800) or (self.ball_x > 800 and self.left_p_rect.centery > self.ball_rect.centery):
            if self.left_p_y < 700:
                self.left_p_y += 1 * delta_time * game.speed
                round(self.left_p_y)
                self.left_p_rect.y = self.left_p_y

        elif (self.left_p_rect.centery > self.ball_rect.centery and self.ball_x < 800) or (self.ball_x > 800 and self.left_p_rect.centery < self.ball_rect.centery):
            if self.left_p_y > 0:
                self.left_p_y += -1 * delta_time * game.speed
                round(self.left_p_y)
                self.left_p_rect.y = self.left_p_y

        if (self.right_p_rect.centery < self.ball_rect.centery and self.ball_x > 600) or (self.ball_x < 600 and self.right_p_rect.centery > self.ball_rect.centery):
            if self.right_p_y < 700:
                self.right_p_y += 1 * delta_time * game.speed
                round(self.right_p_y)
                self.right_p_rect.y = self.right_p_y
        elif (self.right_p_rect.centery > self.ball_rect.centery and self.ball_x > 600) or (self.ball_x < 600 and self.right_p_rect.centery < self.ball_rect.centery):
            if self.right_p_y > 0:
                self.right_p_y += -1 * delta_time * game.speed
                round(self.right_p_y)
                self.right_p_rect.y = self.right_p_y

        if self.ball_rect.colliderect(self.left_p_rect) or self.ball_rect.colliderect(self.right_p_rect):
            self.horizontal *= -1

    def make_bg(self):
        self.animate_bg()
        pygame.draw.rect(screen, '#808080', self.border, 2)
        pygame.draw.rect(screen, settings.player1_color, self.left_p_rect)
        pygame.draw.rect(screen, settings.player2_color, self.right_p_rect)
        pygame.draw.rect(screen, '#FFFFFF', self.ball_rect)

    def update(self):
        screen.fill('#000000')
        self.make_bg()
        screen.blit(self.title_surf, self.title_rect)
        screen.blit(self.creator_surf, self.creator_surf_rect)
        self.play_button.draw()
        self.settings_button.draw()
        self.exit_button.draw()


class Settings:
    def __init__(self):
        self.title_surf = title_font.render('SETTINGS', True, '#FFFFFF')
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.center = ((screen_width / 2), 150)
        self.return_button = Button('RETURN', 200, 40, ((screen_width / 2), 700), 5, True)

        self.gui_sound = pygame.mixer.Sound('gui_click.wav')

        # labels
        self.player1_label = pygame.Rect((200, 450), (200, 40))
        self.player2_label = pygame.Rect((200, 550), (200, 40))
        self.player1_text = settings_label_font.render('P1 COLOR', True, '#000000')
        self.player1_text_rect = self.player1_text.get_rect()
        self.player1_text_rect.center = pygame.Rect((200, 450), (200, 40)).center
        self.player2_text = settings_label_font.render('P2 COLOR', True, '#000000')
        self.player2_text_rect = self.player2_text.get_rect()
        self.player2_text_rect.center = pygame.Rect((200, 550), (200, 40)).center

        self.difficulty_label = pygame.Rect((200, 350), (200, 40))
        self.difficulty_label_text = settings_label_font.render('DIFFICULTY', True, '#000000')
        self.difficulty_label_text_rect = self.difficulty_label_text.get_rect()
        self.difficulty_label_text_rect.center = pygame.Rect((200, 350), (200, 40)).center

        self.game_to_label = pygame.Rect((200, 250), (200, 40))
        self.game_to_label_text = settings_label_font.render('GAME TO', True, '#000000')
        self.game_to_label_text_rect = self.game_to_label_text.get_rect()
        self.game_to_label_text_rect.center = pygame.Rect((200, 250), (200, 40)).center

        self.player1_color = '#ffffff'
        self.player2_color = '#ffffff'

        # color buttons
        self.player1_pink = SettingsButton('', 40, 40, (450, 450), 2, False, '#ffc0cb', 'player_1', 0, 0)
        self.player1_red = SettingsButton('', 40, 40, (525, 450), 2, False, '#ff0000', 'player_1', 0, 0)
        self.player1_orange = SettingsButton('', 40, 40, (600, 450), 2, False, '#ffa500', 'player_1', 0, 0)
        self.player1_yellow = SettingsButton('', 40, 40, (675, 450), 2, False, '#ffff00', 'player_1', 0, 0)
        self.player1_green = SettingsButton('', 40, 40, (750, 450), 2, False, '#00ff00', 'player_1', 0, 0)
        self.player1_purple = SettingsButton('', 40, 40, (825, 450), 2, False, '#800080', 'player_1', 0, 0)
        self.player1_blue = SettingsButton('', 40, 40, (900, 450), 2, False, '#0000ff', 'player_1', 0, 0)
        self.player1_white = SettingsButton('', 40, 40, (975, 450), 2, False, '#ffffff', 'player_1', 0, 0)

        self.player2_pink = SettingsButton('', 40, 40, (450, 550), 2, False, '#ffc0cb', 'player_2', 0, 0)
        self.player2_red = SettingsButton('', 40, 40, (525, 550), 2, False, '#ff0000', 'player_2', 0, 0)
        self.player2_orange = SettingsButton('', 40, 40, (600, 550), 2, False, '#ffa500', 'player_2', 0, 0)
        self.player2_yellow = SettingsButton('', 40, 40, (675, 550), 2, False, '#ffff00', 'player_2', 0, 0)
        self.player2_green = SettingsButton('', 40, 40, (750, 550), 2, False, '#00ff00', 'player_2', 0, 0)
        self.player2_purple = SettingsButton('', 40, 40, (825, 550), 2, False, '#800080', 'player_2', 0, 0)
        self.player2_blue = SettingsButton('', 40, 40, (900, 550), 2, False, '#0000ff', 'player_2', 0, 0)
        self.player2_white = SettingsButton('', 40, 40, (975, 550), 2, False, '#ffffff', 'player_2', 0, 0)

        # difficulty button
        self.difficulty = 'EASY'
        self.difficulty_button = SettingsButton(self.difficulty, 200, 40, (975, 350), 5, True, '#ffffff', 'none', 1, 0)

        # game to button
        self.game_to = '3'
        self.game_to_button = SettingsButton(self.game_to, 200, 40, (975, 250), 5, True, '#ffffff', 'none', 0, 1)

    def check_input(self):
        if self.return_button.pressed:
            pygame.mixer.Sound.play(self.gui_sound)
            game_states.current_state = 'MainMenu'
        if self.difficulty_button.pressed:
            pygame.mixer.Sound.play(self.gui_sound)
            if self.difficulty == 'EASY':
                self.difficulty = 'MEDIUM'
            elif self.difficulty == 'MEDIUM':
                self.difficulty = 'HARD'
            elif self.difficulty == 'HARD':
                self.difficulty = 'EXTREME'
            elif self.difficulty == 'EXTREME':
                self.difficulty = 'IMPOSSIBLE'
            elif self.difficulty == 'IMPOSSIBLE':
                self.difficulty = 'EASY'
            game.what_is_difficulty = self.difficulty
            game.check_input()
        if self.game_to_button.pressed:
            pygame.mixer.Sound.play(self.gui_sound)
            if self.game_to == '3':
                self.game_to = '5'
            elif self.game_to == '5':
                self.game_to = '7'
            elif self.game_to == '7':
                self.game_to = '10'
            elif self.game_to == '10':
                self.game_to = '3'
            game.what_is_game_to = self.game_to
            game.check_input()

    def update(self):
        screen.fill('#000000')
        screen.blit(self.title_surf, self.title_rect)
        self.return_button.draw()
        self.difficulty_button.draw()
        self.game_to_button.draw()

        # labels
        pygame.draw.rect(screen, '#FFFFFF', self.player1_label, border_radius=10)
        screen.blit(self.player1_text, self.player1_text_rect)
        pygame.draw.rect(screen, '#FFFFFF', self.player2_label, border_radius=10)
        screen.blit(self.player2_text, self.player2_text_rect)
        pygame.draw.rect(screen, '#FFFFFF', self.difficulty_label, border_radius=10)
        screen.blit(self.difficulty_label_text, self.difficulty_label_text_rect)
        pygame.draw.rect(screen, '#ffffff', self.game_to_label, border_radius=10)
        screen.blit(self.game_to_label_text, self.game_to_label_text_rect)

        # color buttons
        self.player1_pink.draw()
        self.player1_red.draw()
        self.player1_orange.draw()
        self.player1_yellow.draw()
        self.player1_green.draw()
        self.player1_purple.draw()
        self.player1_blue.draw()
        self.player1_white.draw()

        self.player2_pink.draw()
        self.player2_red.draw()
        self.player2_orange.draw()
        self.player2_yellow.draw()
        self.player2_green.draw()
        self.player2_purple.draw()
        self.player2_blue.draw()
        self.player2_white.draw()


class Game:
    def __init__(self):
        self.l_score = 0
        self.r_score = 0
        self.horizontal = random.choice([-1, 1])
        self.vertical = random.choice([-1, 1])
        self.keys = ''
        self.what_is_difficulty = settings.difficulty
        self.is_countdown = True
        self.start_countdown_time = None
        self.current_time = None
        self.speed = 175
        self.what_is_game_to = '3'
        self.game_end = False
        self.speed_addition = 0

        self.pong_sound = pygame.mixer.Sound('pong.wav')
        self.game_over_sound = pygame.mixer.Sound('game_over.wav')
        self.score_sound = pygame.mixer.Sound('score.wav')

        # game border
        self.border = pygame.Rect((screen_width / 2, screen_height / 2), (screen_width - 10, screen_height - 10))
        self.border.center = (screen_width / 2, screen_height / 2)

        # paddles
        self.left_p_rect = pygame.Rect((self.border.left + 20, self.border.height / 2), (20, 100))
        self.right_p_rect = pygame.Rect((self.border.right - 40, self.border.height / 2), (20, 100))
        self.left_p_rect.centery = self.border.height / 2
        self.right_p_rect.centery = self.border.height / 2
        self.left_p_y = self.left_p_rect.y
        self.right_p_y = self.right_p_rect.y

        # ball
        self.ball_rect = pygame.Rect((self.border.width / 2 - 10, self.border.height / 2 - 10), (20, 20))
        self.ball_rect.center = screen_width / 2, screen_height / 2
        self.ball_x = self.ball_rect.x
        self.ball_y = self.ball_rect.y

        # countdown
        self.countdown5 = countdown_font.render('5', True, '#ffffff')
        self.countdown4 = countdown_font.render('4', True, '#ffffff')
        self.countdown3 = countdown_font.render('3', True, '#ffffff')
        self.countdown2 = countdown_font.render('2', True, '#ffffff')
        self.countdown1 = countdown_font.render('1', True, '#ffffff')

        self.countdown5_rect = self.countdown5.get_rect()
        self.countdown4_rect = self.countdown4.get_rect()
        self.countdown3_rect = self.countdown3.get_rect()
        self.countdown2_rect = self.countdown2.get_rect()
        self.countdown1_rect = self.countdown1.get_rect()

        self.countdown5_rect.center = (screen_width / 2, 200)
        self.countdown4_rect.center = (screen_width / 2, 200)
        self.countdown3_rect.center = (screen_width / 2, 200)
        self.countdown2_rect.center = (screen_width / 2, 200)
        self.countdown1_rect.center = (screen_width / 2, 200)

        # score
        self.score = settings_label_font.render((str(self.l_score) + ' - ' + str(self.r_score)), True, '#ffffff')
        self.score_rect = self.score.get_rect()
        self.score_rect.center = screen_width / 2, 750

        # game over message
        self.game_over_text = countdown_font.render('', True, '#ffffff')
        self.game_over_text_rect = self.game_over_text.get_rect()
        self.game_over_text_rect.center = screen_width / 2, 750

    def move_ball(self):
        if not self.is_countdown:

            self.ball_x += self.horizontal * delta_time * (self.speed + self.speed_addition)
            self.ball_y += self.vertical * delta_time * (self.speed + self.speed_addition)
            print(self.speed_addition)
            round(self.ball_x)
            round(self.ball_y)
            self.ball_rect.topleft = (self.ball_x, self.ball_y)
            if self.ball_y < 5 and self.vertical < 0:
                self.ball_rect.top = self.border.top
                self.vertical *= -1
                pygame.mixer.Sound.play(self.pong_sound)
            elif self.ball_y > 775 and self.vertical > 0:
                self.ball_rect.bottom = self.border.bottom
                self.vertical *= -1
                pygame.mixer.Sound.play(self.pong_sound)

            if self.ball_rect.colliderect(self.left_p_rect) and self.horizontal < 0:
                self.horizontal *= -1
                pygame.mixer.Sound.play(self.pong_sound)
                self.speed_addition += 10
            elif self.ball_rect.colliderect(self.right_p_rect) and self.horizontal > 0:
                self.horizontal *= -1
                pygame.mixer.Sound.play(self.pong_sound)
                self.speed_addition += 10

            # if ball exits screen (somebody scored)
            if self.ball_x < 5:
                self.speed_addition = 0
                # reset ball and paddles
                self.ball_x = screen_width / 2
                self.ball_y = screen_height / 2
                self.ball_rect.center = self.ball_x, self.ball_y

                self.left_p_y = self.border.height / 2
                self.left_p_rect.y = self.left_p_y
                self.right_p_y = self.border.height / 2
                self.right_p_rect.y = self.right_p_y
                # add a point, check if player won
                self.r_score += 1
                pygame.mixer.Sound.play(self.score_sound)
                if self.r_score >= int(self.what_is_game_to):
                    self.is_countdown = True
                    self.game_over_text = countdown_font.render('PLAYER 2 WINS', True, '#ffffff')
                    self.game_over_text_rect = self.game_over_text.get_rect()
                    self.game_over_text_rect.center = screen_width / 2, 200
                    self.game_end = True
                    self.start_countdown_time = pygame.time.get_ticks()
                    pygame.mixer.Sound.play(self.game_over_sound)

                # initiate the countdown to continue game
                else:
                    self.is_countdown = True
                    self.start_countdown_time = pygame.time.get_ticks()
            elif self.ball_x > 1395:
                self.speed_addition = 0

                self.ball_x = screen_width / 2
                self.ball_y = screen_height / 2
                self.ball_rect.center = self.ball_x, self.ball_y

                self.left_p_y = self.border.height / 2
                self.left_p_rect.centery = self.left_p_y
                self.right_p_y = self.border.height / 2
                self.right_p_rect.centery = self.right_p_y

                self.l_score += 1
                pygame.mixer.Sound.play(self.score_sound)
                if self.l_score >= int(self.what_is_game_to):
                    self.is_countdown = True
                    self.game_over_text = countdown_font.render('PLAYER 1 WINS', True, '#ffffff')
                    self.game_over_text_rect = self.game_over_text.get_rect()
                    self.game_over_text_rect.center = screen_width / 2, 200
                    self.game_end = True
                    self.start_countdown_time = pygame.time.get_ticks()
                    pygame.mixer.Sound.play(self.game_over_sound)
                else:
                    self.is_countdown = True
                    self.start_countdown_time = pygame.time.get_ticks()

    def check_input(self):
        if game_states.current_state == 'game':
            self.keys = pygame.key.get_pressed()
            if self.keys[pygame.K_w] and self.left_p_rect.top > 6:
                self.left_p_y += -1 * delta_time * 500
            elif self.keys[pygame.K_s] and self.left_p_rect.bottom < 794:
                self.left_p_y += 1 * delta_time * 500

            if self.keys[pygame.K_UP] and self.right_p_rect.top > 6:
                self.right_p_y += -1 * delta_time * 500
            elif self.keys[pygame.K_DOWN] and self.right_p_rect.bottom < 794:
                self.right_p_y += 1 * delta_time * 500
        self.left_p_rect.y = round(self.left_p_y)
        self.right_p_rect.y = round(self.right_p_y)

        if self.what_is_difficulty == 'EASY':
            self.speed = 225
        elif self.what_is_difficulty == 'MEDIUM':
            self.speed = 300
        elif self.what_is_difficulty == 'HARD':
            self.speed = 415
        elif self.what_is_difficulty == 'EXTREME':
            self.speed = 545
        elif self.what_is_difficulty == 'IMPOSSIBLE':
            self.speed = 700

    def update_portion(self):
        self.score = settings_label_font.render((str(self.l_score) + ' - ' + str(self.r_score)), True, '#ffffff')
        self.score_rect = self.score.get_rect()
        self.score_rect.center = screen_width / 2, 750

        screen.fill('#000000')
        pygame.draw.rect(screen, '#808080', self.border, 2)
        pygame.draw.rect(screen, settings.player1_color, self.left_p_rect)
        pygame.draw.rect(screen, settings.player2_color, self.right_p_rect)
        pygame.draw.rect(screen, '#FFFFFF', self.ball_rect)
        screen.blit(self.score, self.score_rect)

    def update(self):
        if self.is_countdown and game_states.current_state == 'game':
            if self.game_end:
                self.update_portion()
                self.current_time = pygame.time.get_ticks()
                if self.current_time - self.start_countdown_time < 3200:
                    screen.blit(self.game_over_text, self.game_over_text_rect)
                elif self.current_time - self.start_countdown_time > 3200:
                    game_states.current_state = 'MainMenu'
                    self.is_countdown = False
                    self.game_end = False
            else:
                self.update_portion()
                self.current_time = pygame.time.get_ticks()
                if self.current_time - self.start_countdown_time < 5100:
                    if self.current_time - self.start_countdown_time < 1000:
                        screen.blit(self.countdown5, self.countdown5_rect)
                    elif 1000 < self.current_time - self.start_countdown_time < 2000:
                        screen.blit(self.countdown4, self.countdown4_rect)
                    elif 2000 < self.current_time - self.start_countdown_time < 3000:
                        screen.blit(self.countdown3, self.countdown3_rect)
                    elif 3000 < self.current_time - self.start_countdown_time < 4000:
                        screen.blit(self.countdown2, self.countdown2_rect)
                    elif 4000 < self.current_time - self.start_countdown_time < 5100:
                        screen.blit(self.countdown1, self.countdown1_rect)
                elif self.current_time - self.start_countdown_time > 5100:
                    self.is_countdown = False
        elif not self.is_countdown and game_states.current_state == 'game':
            self.what_is_difficulty = settings.difficulty

            self.update_portion()

            self.move_ball()
            self.check_input()


class GameStates:
    def __init__(self):
        self.current_state = 'MainMenu'

    def state_manager(self):
        if self.current_state == 'MainMenu':
            main_menu.update()
        if self.current_state == 'settings':
            settings.update()
        if self.current_state == 'game':
            game.update()


# instances of the classes
game_states = GameStates()
main_menu = MainMenu()
settings = Settings()
game = Game()


# delta time and run loop
last_frame = time.time()
while 1:
    delta_time = time.time() - last_frame
    last_frame = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game_states.state_manager()
    pygame.display.update()
    clock.tick(60)
