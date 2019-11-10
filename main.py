import random
import math
import pygame
import pygame.gfxdraw

# screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT
FPS = 60

# color definition (R, G, B):
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
TEAL = (0, 128, 128)
GREY = (211, 211, 211)

# Paddle
PADDLE_WIDTH = 75
PADDLE_HEIGHT = 15
PADDLE_X = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
PADDLE_Y = SCREEN_HEIGHT - 50
PADDLE_SPEED = 10

# blocks
BLOCK_WIDTH = 80
BLOCK_HEIGHT = 15
BLOCK_X = 20
BLOCK_Y = 20
SPACING = 5
COLUMNS = 9
ROWS = 7

# ball
BALL_WIDTH = BALL_HEIGHT = 16
ANGLE = 200
VELOCITY = 5
VELOCITY_X = random.randint(2, 7)
VELOCITY_Y = math.sqrt(VELOCITY_X * 2 + VELOCITY * 2)
BALL_X = PADDLE_X + PADDLE_WIDTH / 2 - BALL_WIDTH / 2
BALL_Y = PADDLE_Y - BALL_HEIGHT

# library init
pygame.init()

# screen creation, caption & size
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Arkanoid')

# clock definition
clock = pygame.time.Clock()


# Paddle definition
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # calling the parent class - Sprite
        # creating a paddle
        self.image = pygame.image.load("paddle.png")
        '''
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(WHITE)
        '''
        # paddle position
        self.rect = self.image.get_rect()
        self.rect.x = PADDLE_X
        self.rect.y = PADDLE_Y

        # movement characteristics
        self.movement = [0, 0]
        self.speed = PADDLE_SPEED

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)  # self.rect.move(self.movement) = self.rect + self.movement
        if self.rect.left < 0: self.rect.x = 0
        if self.rect.left >= SCREEN_WIDTH - PADDLE_WIDTH: self.rect.x = SCREEN_WIDTH - PADDLE_WIDTH

    def keypress_movement(self):  # definition of the movement
        if event.type == pygame.KEYDOWN:  # holding down the key
            if event.key == pygame.K_LEFT:
                self.movement[0] = -1 * self.speed  # moving left
            if event.key == pygame.K_RIGHT:
                self.movement[0] = self.speed  # moving right

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                mypaddle.movement[0] = 0


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("brick.png")
        '''
        self.image = pygame.Surface([BLOCK_WIDTH, BLOCK_HEIGHT])
        self.image.fill(WHITE)
        '''

        self.rect = self.image.get_rect()
        self.rect.x = BLOCK_X
        self.rect.y = BLOCK_Y

    def draw(self):
        screen.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # creation of the surface for the ball
        self.image = pygame.image.load("ball.png")
        '''
        self.image = pygame.Surface([BALL_WIDTH, BALL_HEIGHT])
        self.image.fill(TEAL)
        
        # creation of the round object
        pygame.gfxdraw.aacircle(self.image, 7, 7, 7, WHITE)
        pygame.gfxdraw.filled_circle(self.image, 7, 7, 7, WHITE)
        '''
        # position of the ball
        self.rect = self.image.get_rect(center=(0, 0))
        self.rect.x = BALL_X
        self.rect.y = BALL_Y

        # get attributes of the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        # velocity modifiers
        self.a = 1
        self.b = 1

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        # ball movement
        self.rect.x += VELOCITY_X * self.a
        self.rect.y -= VELOCITY_Y * self.b

        # boundaries
        if self.rect.x >= self.screenwidth - BALL_WIDTH: self.a *= -1  # right
        if self.rect.y <= 0: self.b *= -1  # top
        if self.rect.x <= 0: self.a *= -1  # left
        if self.rect.y >= self.screenheight:  # game over
            self.font = pygame.font.Font(None, 36)
            self.text = self.font.render("Game Over", True, RED)
            self.textpos = self.text.get_rect(centerx=screen.get_width() / 2)
            self.textpos.top = 300
            screen.blit(self.text, self.textpos)


# create paddle
mypaddle = Paddle()

# create ball
balls = pygame.sprite.Group()  # used to check for collisions
ball = Ball()
balls.add(ball)

# create blocks
blocks = pygame.sprite.Group()
for row in range(ROWS):
    for column in range(COLUMNS):
        block = Block()
        blocks.add(block)
        BLOCK_X += BLOCK_WIDTH + SPACING
    BLOCK_X = 20
    BLOCK_Y += BLOCK_HEIGHT + SPACING

# main loop of the game
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True

        mypaddle.keypress_movement()  # allow the paddle to move

    clock.tick(FPS)  # clock set
    screen.fill(TEAL)  # clear the screen

    if pygame.sprite.spritecollide(mypaddle, balls, False):  # paddle collision check
        ball.b *= -1

    if pygame.sprite.spritecollide(ball, blocks, True):  # blocks collision check, true - blocks are gone once hit
        ball.b *= -1

    # check if game is won:
    if len(blocks) == 0:
        font = pygame.font.Font(None, 36)
        won = font.render("You won!", True, RED)
        wonpos = won.get_rect(centerx=screen.get_width() / 2)
        wonpos.top = 300
        screen.blit(won, wonpos)
    else:
        mypaddle.update()  # update the position of the paddle
        ball.update()  # update the position of the ball
        ball.draw()  # draw the ball
        blocks.draw(screen)  # draw the blocks
        mypaddle.draw()  # draw the paddle (in the new position)

    pygame.display.update()

pygame.quit()
