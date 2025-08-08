import pygame
import random
import sys
import time


pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Pong v2 by Dylan Folscroft")
pygame.display.set_icon(pygame.image.load("pongicon.png"))
# clock = pygame.time.Clock()

font = pygame.font.SysFont('Roboto Mono', 35)
font2 = pygame.font.SysFont('Roboto Mono', 25)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, move_keys):
        self.x = x
        self.y_pos = (screen.get_height() / 2)
        self.y_move = 0
        self.move_keys = move_keys
        self.paddle = pygame.Surface((20, 100))
        self.paddle.fill('white')
        self.rect = self.paddle.get_rect(topleft = (self.x, self.y_pos))

    def move(self):
        keys = pygame.key.get_pressed()
        if self.move_keys == "letters":
            if keys[pygame.K_s] and self.rect.bottom < 800:
                self.y_move = 10
            elif keys[pygame.K_w] and self.rect.top > 0:
                self.y_move = -10
            else:
                self.y_move = 0
        if self.move_keys == "arrows":
            if keys[pygame.K_DOWN] and self.rect.bottom < 800:
                self.y_move = 10
            elif keys[pygame.K_UP] and self.rect.top > 0:
                self.y_move = -10
            else:
                self.y_move = 0

    def update(self, dt):
        self.move()
        self.y_pos += self.y_move * dt * 45
        self.rect.topleft = (round(self.x), round(self.y_pos))


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.horizontal = random.choice([-10, 10])
        self.vertical = random.choice([-10, 10])
        self.ball = pygame.Surface((20, 20))
        self.ball.fill('white')
        self.rect = self.ball.get_rect(topleft = (self.x, self.y))
        self.speed = 25
        self.lscore = 0
        self.rscore = 0

    def movement(self):
        self.y += self.vertical * dt * self.speed
        round(self.y)
        if self.y < 0:
            self.y = 0
            self.vertical *= -1
        elif self.y > 780:
            self.y = 780
            self.vertical *= -1

        self.x += self.horizontal * dt * self.speed
        round(self.x)
        if ball.rect.colliderect(left_paddle.rect):
            self.x = 40
            self.horizontal *= -1
            self.speed += 2
        elif ball.rect.colliderect(right_paddle.rect):
            self.x = 1140
            self.horizontal *= -1
            self.speed += 2
        elif ball.rect.left <= 0:
            self.rscore += 1
            self.speed = 25
            self.horizontal = 10
            self.vertical = random.choice([-10, 10])
            self.x = 570
            self.y = 360
        elif ball.rect.right >= 1200:
            self.lscore += 1
            self.speed = 25
            self.horizontal = -10
            self.vertical = random.choice([-10, 10])
            self.x = 570
            self.y = 360

        self.rect.topleft = (self.x, self.y)
        text = font.render(str(self.lscore) + " - " + str(self.rscore), True, (255, 255, 255))
        text2 = font2.render("Pong v2 by Dylan Folscroft - Control Paddles Using W, S, Up Arrow, And Down Arrow", True, (255, 255, 255))
        text_rect = text.get_rect()
        text2_rect = text2.get_rect()
        text_rect.center = ((screen.get_width() / 2), 750)
        text2_rect.center = ((screen.get_width() / 2), 50)
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)


def create_screen():
    screen.fill('black')

    screen.blit(left_paddle.paddle, left_paddle.rect)
    screen.blit(right_paddle.paddle, right_paddle.rect)
    screen.blit(ball.ball, ball.rect)
    left_paddle.update(dt)
    right_paddle.update(dt)
    ball.movement()

    pygame.display.update()


left_paddle = Paddle(20, "letters")
right_paddle = Paddle(1160, "arrows")
ball = Ball((screen.get_width() / 2), (screen.get_height() / 2))


last_frame = time.time()
while 1:
    dt = time.time() - last_frame
    last_frame = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    create_screen()
    # clock.tick(10)







