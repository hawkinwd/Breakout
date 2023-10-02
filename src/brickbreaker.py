import pygame
import sys
import random
import time
import math


def get_number_of_items(seq, n):
    total = 0
    for k in range(len(seq)):
        if seq[k] == n:
            total += 1
    return total


def check_for_click(event, cont_rect, quit_rect):
    click_x, click_y = event.pos
    if cont_rect.x <= click_x <= cont_rect.x + cont_rect.width and cont_rect.y <= click_y <= cont_rect.y + cont_rect.height:
        return 1
    elif quit_rect.x <= click_x <= quit_rect.x + quit_rect.width and quit_rect.y <= click_y <= quit_rect.y + quit_rect.height:
        return 2
    return 0


def draw_powerup(brick, powerup):

    if brick.power_up == 1:
        powerup.screen.blit(powerup.slow_ball_image,
                            (brick.x + brick.width / 2 - 16, brick.y + brick.height / 2))
    elif brick.power_up == 2:
        powerup.screen.blit(powerup.long_paddle_image,
                            (brick.x + brick.width / 2 - 16, brick.y + brick.height / 2))
    elif brick.power_up == 3:
        powerup.screen.blit(powerup.big_ball_image,
                            (brick.x + brick.width / 2 - 16, brick.y + brick.height / 2))
    elif brick.power_up == 4:
        powerup.screen.blit(powerup.wrap_image,
                            (brick.x + brick.width / 2 - 16, brick.y + brick.height / 2))


def draw_x(screen, center_x, half_width, center_y):
    pygame.draw.line(screen, (255, 0, 0), (center_x - half_width, center_y + half_width),
                     (center_x + half_width, center_y - half_width), 10)
    pygame.draw.line(screen, (255, 0, 0), (center_x - half_width, center_y - half_width),
                     (center_x + half_width, center_y + half_width), 10)


def draw_triangle(screen, center_x, center_y, length):
    bisector_length = math.sqrt(0.75 * length ** 2)
    top_left = (center_x - (1 / 3) * bisector_length, center_y - length / 2)
    bottom_left = (center_x - (1 / 3) * bisector_length, center_y + length / 2)
    right = (center_x + (2 / 3) * bisector_length, center_y)
    pts = [top_left, bottom_left, right]
    pygame.draw.polygon(screen, pygame.Color('darkgreen'), pts)


class Paddle:
    def __init__(self, screen):
        self.screen = screen
        self.length = 80
        self.speed = 10
        self.x = (self.screen.get_width() - self.length) // 2
        self.y = self.screen.get_height() - 25
        self.thickness = 16
        self.number_of_lives = 3

    def draw(self):
        pygame.draw.line(self.screen, (0, 0, 255), (self.x, self.y), (self.x + self.length, self.y), self.thickness)
        pygame.draw.circle(self.screen, (0, 0, 255), (self.x, self.y + 1), self.thickness // 2, self.thickness // 2)
        pygame.draw.circle(self.screen, (0, 0, 255), (self.x + self.length, self.y + 1),
                           self.thickness // 2, self.thickness // 2)

    def hit_by(self, ball):
        paddle_hitbox = pygame.Rect(self.x - (self.thickness // 2), self.y - (self.thickness // 2),
                                    self.length + self.thickness, self.thickness)
        return paddle_hitbox.collidepoint(ball.x, ball.y + ball.radius)


class Ball:
    def __init__(self, screen, paddle):
        self.screen = screen
        self.x = self.screen.get_width() // 2
        self.y = self.screen.get_height() - paddle.thickness - 25 - 5
        self.radius = 5
        self.speed_x = 3 * random.choice([-1, 1])
        self.speed_y = -4
        self.number_of_bounces = 0
        self.paddle = paddle
        self.color = pygame.Color('white')

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius, self.radius)

    def bounce_off_paddle(self, paddle_direction):
        x_direction = self.speed_x // abs(self.speed_x)
        if self.number_of_bounces % 5 == 0 and self.number_of_bounces != 0:
            self.speed_x = x_direction * (abs(self.speed_x) + 1.5)
            self.speed_y += 1.5
            if self.speed_x >= 12:
                self.speed_x = 12
            if self.speed_y >= 12:
                self.speed_y = 12
        if paddle_direction > 0:
            if self.paddle.x + self.paddle.length / 3 >= self.x:
                self.speed_y = -1 * self.speed_y
            elif self.paddle.x + 2 * self.paddle.length / 3 <= self.x:
                temp_speed_x = -1 * abs(self.speed_x)
                self.speed_x = self.speed_y * x_direction
                self.speed_y = temp_speed_x
            else:
                self.speed_y = -1 * self.speed_y
        elif paddle_direction < 0:
            if self.paddle.x + self.paddle.length / 3 >= self.x:
                temp_speed_x = -1 * abs(self.speed_x)
                self.speed_x = self.speed_y * x_direction
                self.speed_y = temp_speed_x
            elif self.paddle.x + 2 * self.paddle.length / 3 <= self.x:
                temp_speed_x = -1 * abs(self.speed_x)
                self.speed_x = self.speed_y * x_direction * -1
                self.speed_y = temp_speed_x
            else:
                self.speed_y = -1 * self.speed_y
        else:
            if self.paddle.x + self.paddle.length / 3 >= self.x:
                self.speed_x = abs(self.speed_x)
                self.speed_y = -1 * self.speed_y
            elif self.paddle.x + 2 * self.paddle.length / 3 <= self.x:
                self.speed_y = -1 * self.speed_y
            else:
                temp_speed_x = abs(self.speed_x)
                self.speed_x = self.speed_y * x_direction
                self.speed_y = -1 * temp_speed_x
        self.number_of_bounces += 1
        self.y = self.paddle.y - self.paddle.thickness // 2 - self.radius

    def reset(self):
        self.x = self.screen.get_width() // 2
        self.y = self.screen.get_height() - self.paddle.thickness - 25 - 5
        self.speed_x = random.choice([-1, 1]) * 3
        self.speed_y = -4
        self.number_of_bounces = 0
        self.radius = 5
        self.color = pygame.Color('white')


class Brick:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 75
        self.height = 15
        self.is_destroyed = False
        self.color = pygame.Color('red')
        self.power_up = 0
        self.score = 0

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def hit_by(self, ball):
        brick_hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if brick_hitbox.collidepoint(ball.x, ball.y + ball.radius):
            ball.speed_y = -1 * ball.speed_y
            return True
        if brick_hitbox.collidepoint(ball.x, ball.y - ball.radius):
            ball.speed_y = -1 * ball.speed_y
            return True
        if brick_hitbox.collidepoint(ball.x + ball.radius, ball.y):
            ball.speed_x = -1 * ball.speed_x
            return True
        if brick_hitbox.collidepoint(ball.x - ball.radius, ball.y):
            ball.speed_x = -1 * ball.speed_x
            return True


class Wall:
    def __init__(self, screen, number_of_rows):
        self.bricks = []
        self.number_of_rows = number_of_rows
        for k in range(self.number_of_rows):
            for j in range(10):
                brick = Brick(screen, 50 / 11, 100)
                brick.x += j * (brick.width + 50 / 11)
                brick.y += k * (brick.height + 50 / 11)
                if k % 4 == 1:
                    brick.color = pygame.Color('yellow')
                elif k % 4 == 2:
                    brick.color = pygame.Color('green')
                elif k % 4 == 3:
                    brick.color = pygame.Color('orange')
                brick.score = 10 * (self.number_of_rows - k)
                self.bricks.append(brick)
        self.special_bricks = random.sample(self.bricks, k=self.number_of_rows + 1)
        for special_brick in self.special_bricks:
            special_brick.power_up = random.randint(1, 4)
            special_brick.color = pygame.Color('royalblue2')

    def draw(self):
        for brick in self.bricks:
            brick.draw()

    def remove_hit_bricks(self):
        for k in range(len(self.bricks) - 1, -1, -1):
            if self.bricks[k].is_destroyed:
                del self.bricks[k]


class PowerUp:
    def __init__(self, screen, wall):
        self.wall = wall
        self.slow_ball = False
        self.slow_ball_image = pygame.image.load('snowflake.png')
        self.long_paddle = False
        self.long_paddle_image = pygame.image.load('arrows.png')
        self.big_ball = False
        self.big_ball_image = pygame.image.load('big.png')
        self.wrap = False
        self.wrap_image = pygame.image.load('wrap.png')
        self.speed = 2
        self.screen = screen
        self.active_powerups = []
        self.font = pygame.font.Font(None, 25)

    def draw(self, brick):
        draw_powerup(brick, self)

    def move(self):
        for brick in self.wall.special_bricks:
            if brick.is_destroyed:
                brick.y += self.speed
                draw_powerup(brick, self)

    def caught(self, paddle):
        paddle_hitbox = pygame.Rect(paddle.x - (paddle.thickness // 2), paddle.y - (paddle.thickness // 2),
                                    paddle.length + paddle.thickness, paddle.thickness)
        for brick in self.wall.special_bricks:
            if brick.is_destroyed:
                powerup_hitbox = pygame.Rect(brick.x + brick.width / 2 - 16, brick.y + brick.height / 2, 24, 24)
                if powerup_hitbox.colliderect(paddle_hitbox) == 1:
                    if brick.power_up == 1:
                        self.active_powerups.append(1)
                        self.slow_ball = True
                    elif brick.power_up == 2:
                        self.active_powerups.append(2)
                        self.long_paddle = True
                    elif brick.power_up == 3:
                        self.active_powerups.append(3)
                        self.big_ball = True
                    elif brick.power_up == 4:
                        self.active_powerups.append(4)
                        self.wrap = True
                    self.wall.special_bricks.remove(brick)
                    return True

    def remove_all(self):
        for brick in self.wall.special_bricks:
            if brick.is_destroyed:
                self.wall.special_bricks.remove(brick)

    def remove_one(self):
        for brick in self.wall.special_bricks:
            if brick.is_destroyed:
                if brick.y + brick.height / 2 >= self.screen.get_height():
                    self.wall.special_bricks.remove(brick)

    def active_string(self, seq_of_actives):
        a = 0
        for k in range(len(seq_of_actives)):
            if len(seq_of_actives[k]) > 0:
                text_image = self.font.render(seq_of_actives[k], True, (255, 255, 255))
                self.screen.blit(text_image, ((self.screen.get_width() - text_image.get_width()) / 2,
                                              5 * (a + 1) + text_image.get_height() * a))
                a += 1


class Scoreboard:
    def __init__(self, screen, level):
        self.screen = screen
        self.score = 0
        self.font = pygame.font.Font(None, 30)
        self.level = level

    def draw(self):
        score_string = 'Score: ' + str(self.score)
        score_image = self.font.render(score_string, True, (255, 255, 255))
        self.screen.blit(score_image, (5, 5))
        level_string = 'Level: ' + str(self.level)
        level_image = self.font.render(level_string, True, (255, 255, 255))
        self.screen.blit(level_image, (5, 5 + score_image.get_height()))


class LifeCounter:
    def __init__(self, screen):
        self.screen = screen
        self.lives = 3
        self.font = pygame.font.Font(None, 30)

    def draw(self):
        lives_image = self.font.render('Lives: ', True, (255, 255, 255))
        self.screen.blit(lives_image, (self.screen.get_width() - 156, 5))
        heart = pygame.image.load('heart.png')
        heart.set_colorkey((0, 0, 0,))
        for k in range(self.lives):
            self.screen.blit(heart, (self.screen.get_width() - 96 + 32 * k, 5))


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Breakout!')
    screen = pygame.display.set_mode((800, 500))

    paddle = Paddle(screen)
    ball = Ball(screen, paddle)
    level = 1
    wall = Wall(screen, level + 3)
    powerup = PowerUp(screen, wall)
    scoreboard = Scoreboard(screen, level)
    life_counter = LifeCounter(screen)

    start_time_slow_ball = start_time_long_paddle = start_time_big_ball = start_time_wrap = math.inf
    slow_ball_string = long_paddle_string = big_ball_string = wrap_string = ''
    active_powerup_seq = [slow_ball_string, long_paddle_string, big_ball_string, wrap_string]

    game_over_font = pygame.font.Font(None, 100)
    cont_and_quit_font = pygame.font.Font(None, 75)
    game_over_image = game_over_font.render('GAME OVER', True, (255, 255, 255))
    continue_image = cont_and_quit_font.render('Play Again', True, (255, 255, 255))
    quit_image = game_over_font.render('Quit', True, (255, 255, 255))

    is_game_over = False
    no_answer = False

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if is_game_over:
                screen.fill((0, 0, 0))
                life_counter.draw()
                scoreboard.draw()
                game_over_rect = pygame.Rect(screen.get_width() / 2 - 300, screen.get_height() / 2 - 150, 600, 300)
                pygame.draw.rect(screen, (0, 0, 0), game_over_rect)
                cont_rect = pygame.Rect(screen.get_width() / 2 + 300 - continue_image.get_width(),
                                        screen.get_height() / 2 + 50, continue_image.get_width(),
                                        continue_image.get_height())
                quit_rect = pygame.Rect(screen.get_width() / 2 - 300, screen.get_height() / 2 + 50,
                                        quit_image.get_width(), quit_image.get_height())
                draw_x(screen, quit_rect.centerx, quit_rect.width // 2, quit_rect.centery)
                draw_triangle(screen, cont_rect.centerx, cont_rect.centery, quit_rect.width)
                screen.blit(game_over_image, ((screen.get_width() - game_over_image.get_width()) / 2,
                                              (screen.get_height() - game_over_image.get_height()) / 2 - 100))
                screen.blit(continue_image, (screen.get_width() / 2 + 300 - continue_image.get_width(),
                                             screen.get_height() / 2 + 50))
                screen.blit(quit_image, (screen.get_width() / 2 - 300, screen.get_height() / 2 + 50))
                if event.type == pygame.MOUSEBUTTONUP:
                    if check_for_click(event, cont_rect, quit_rect) == 1:
                        return True
                    elif check_for_click(event, cont_rect, quit_rect) == 2:
                        sys.exit()
                    else:
                        no_answer = True
                pygame.display.update()
        if is_game_over:
            if no_answer:
                continue

        if len(wall.bricks) == 0:
            level += 1
            if level > 10:
                level = 10
            powerup.remove_all()
            wall = Wall(screen, 3 + level)
            powerup = PowerUp(screen, wall)
            ball.reset()
            scoreboard.level += 1
            slow_ball_string = long_paddle_string = big_ball_string = wrap_string = ''
            powerup.slow_ball = powerup.long_paddle = powerup.big_ball = powerup.wrap = False
            start_time_slow_ball = start_time_long_paddle = start_time_big_ball = start_time_wrap = math.inf
            screen.fill((0, 0, 0))
            text_image = pygame.font.Font(None, 100).render('Level {} passed!'.format(level - 1),
                                                            True, (255, 255, 255))
            screen.blit(text_image, ((screen.get_width() - text_image.get_width()) / 2,
                                     (screen.get_height() - text_image.get_height()) / 2))
            paddle.draw()
            pygame.display.update()
            time.sleep(1.5)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RIGHT] and paddle.x + paddle.length + (paddle.thickness // 2) < screen.get_width():
            paddle.x += paddle.speed
        if pressed_keys[pygame.K_LEFT] and paddle.x - (paddle.thickness // 2) > 0:
            paddle.x -= paddle.speed

        if paddle.hit_by(ball):
            if pressed_keys[pygame.K_RIGHT]:
                ball.bounce_off_paddle(1)
            elif pressed_keys[pygame.K_LEFT]:
                ball.bounce_off_paddle(-1)
            else:
                ball.bounce_off_paddle(0)

        if not powerup.slow_ball:
            ball.x += ball.speed_x
            ball.y += ball.speed_y
        else:
            ball.x += ball.speed_x / 2
            ball.y += ball.speed_y / 2

        if powerup.caught(paddle):
            if powerup.active_powerups[-1] == 1:
                start_time_slow_ball = time.time()
            elif powerup.active_powerups[-1] == 2:
                start_time_long_paddle = time.time()
            elif powerup.active_powerups[-1] == 3:
                start_time_big_ball = time.time()
            elif powerup.active_powerups[-1] == 4:
                start_time_wrap = time.time()
            if powerup.long_paddle and get_number_of_items(powerup.active_powerups, 2) == 1:
                paddle.length += 65
                paddle.x -= 65 / 2
            if powerup.big_ball and get_number_of_items(powerup.active_powerups, 3) == 1:
                ball.radius = 9

        if powerup.slow_ball and powerup.big_ball:
            ball.color = pygame.Color('powderblue')
        elif powerup.slow_ball and not powerup.big_ball:
            ball.color = pygame.Color('lightskyblue2')
        elif not powerup.slow_ball and powerup.big_ball:
            ball.color = pygame.Color('mediumpurple2')
        else:
            ball.color = pygame.Color('white')

        if powerup.slow_ball:
            slow_ball_string = 'Slow Ball: ' + str(int(6 - time.time() + start_time_slow_ball)) + 's'
        if powerup.long_paddle:
            long_paddle_string = 'Long Paddle: ' + str(int(6 - time.time() + start_time_long_paddle)) + 's'
        if powerup.big_ball:
            big_ball_string = 'Big Ball: ' + str(int(6 - time.time() + start_time_big_ball)) + 's'
        if powerup.wrap:
            wrap_string = 'Wrap Ball: ' + str(int(6 - time.time() + start_time_wrap)) + 's'

        if start_time_slow_ball + 5 <= time.time():
            powerup.slow_ball = False
            powerup.active_powerups = [i for i in powerup.active_powerups if i != 1]
            ball.color = pygame.Color('white')
            start_time_slow_ball = math.inf
            slow_ball_string = ''
        if start_time_long_paddle + 5 <= time.time():
            powerup.long_paddle = False
            powerup.active_powerups = [i for i in powerup.active_powerups if i != 2]
            paddle.length = 115
            paddle.x += 65 / 2
            start_time_long_paddle = math.inf
            long_paddle_string = ''
        if start_time_big_ball + 5 <= time.time():
            powerup.big_ball = False
            powerup.active_powerups = [i for i in powerup.active_powerups if i != 3]
            ball.radius = 5
            ball.color = pygame.Color('white')
            start_time_big_ball = math.inf
            big_ball_string = ''
        if start_time_wrap + 5 <= time.time():
            powerup.wrap = False
            powerup.active_powerups = [i for i in powerup.active_powerups if i != 4]
            start_time_wrap = math.inf
            wrap_string = ''

        active_powerup_seq[0] = slow_ball_string
        active_powerup_seq[1] = long_paddle_string
        active_powerup_seq[2] = big_ball_string
        active_powerup_seq[3] = wrap_string

        if not powerup.wrap:
            if ball.x - ball.radius <= 0:
                ball.speed_x = abs(ball.speed_x)

            elif ball.x + ball.radius > screen.get_width():
                ball.speed_x = -1 * abs(ball.speed_x)
        else:
            if ball.x <= 0:
                ball.x = screen.get_width()
            elif ball.x >= screen.get_width():
                ball.x = 0
        if ball.y - ball.radius < 0:
            ball.speed_y = abs(ball.speed_y)

        screen.fill((0, 0, 0))

        for brick in wall.bricks:
            if brick.hit_by(ball):
                if brick.power_up != 0:
                    powerup.draw(brick)
                brick.is_destroyed = True
                scoreboard.score += brick.score

        paddle.draw()
        ball.draw()
        scoreboard.draw()
        wall.draw()
        wall.remove_hit_bricks()
        life_counter.draw()
        powerup.move()
        powerup.active_string(active_powerup_seq)
        powerup.remove_one()
        if powerup.wrap:
            pygame.draw.line(screen, pygame.Color('gold2'), (0, 0), (0, screen.get_height()), 7)
            pygame.draw.line(screen, pygame.Color('gold2'), (screen.get_width(), 0),
                             (screen.get_width(), screen.get_height()), 7)

        if ball.y + ball.radius >= screen.get_height():
            life_counter.lives -= 1
            ball.reset()
            paddle.length = 115
            slow_ball_string = long_paddle_string = big_ball_string = wrap_string = ''
            start_time_slow_ball = start_time_long_paddle = start_time_big_ball = start_time_wrap = math.inf
            lost_life_image = cont_and_quit_font.render('-1 Life', True, (255, 255, 255))
            screen.blit(lost_life_image, ((screen.get_width() - lost_life_image.get_width()) / 2,
                                          (screen.get_height() - lost_life_image.get_height()) / 2))
            powerup.remove_all()
            powerup.slow_ball = powerup.long_paddle = powerup.big_ball = powerup.wrap = False
            pygame.display.update()
            if life_counter.lives > 0:
                time.sleep(2)
                ball = Ball(screen, paddle)
            else:
                is_game_over = True
                no_answer = True

        pygame.display.update()



main()
