import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick

pygame.init()

# Dimensions of the screen
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
DARKBLUE = (36, 90, 190)
LIGHTBLUE = (0, 176, 240)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)

# Window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout")

# game running
running = True

# to control the frame rate
clock = pygame.time.Clock()

# window screen
def message_display(surface, text, width, height):
    font = pygame.font.Font('freesansbold.ttf', 74)
    label = font.render(text, 1, WHITE)
    label_rect = label.get_rect()
    label_rect.center = ((width/2),(height/2))
    screen.blit(label, label_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

# text objects
def text_objects(text, font):
    textSurface = font.render(text, True, DARKBLUE)
    return textSurface, textSurface.get_rect()

# game loop
def game_loop(gameExit):
    score = 0
    lives = 3
    
    # Create a list of sprites
    list_of_sprites = pygame.sprite.Group()

    # new object: Paddle
    paddle = Paddle(LIGHTBLUE, 100, 10)
    paddle.rect.x = 350
    paddle.rect.y = 560

    # new object: Ball
    ball = Ball(WHITE, 10, 10)
    ball.rect.x = 345
    ball.rect.y = 195

    # new objects: bricks
    list_of_bricks = pygame.sprite.Group()
    for i in range(7):
        brick = Brick(RED,80,30)
        brick.rect.x = 60+i*100
        brick.rect.y = 60
        list_of_sprites.add(brick)
        list_of_bricks.add(brick)
    for i in range(7):
        brick = Brick(ORANGE,80,30)
        brick.rect.x = 60+i*100
        brick.rect.y = 100
        list_of_sprites.add(brick)
        list_of_bricks.add(brick)
    for i in range(7):
        brick = Brick(YELLOW,80,30)
        brick.rect.x = 60+i*100
        brick.rect.y = 140
        list_of_sprites.add(brick)
        list_of_bricks.add(brick)

    # Add any object to the list of sprites
    list_of_sprites.add(paddle)
    list_of_sprites.add(ball)

    while gameExit:
        # --- event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # input: move the paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.moveLeft(5)
        if keys[pygame.K_RIGHT]:
            paddle.moveRight(5)
        
        # --- game logic
        list_of_sprites.update()

        # check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x >= 790:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x <= 0:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y > 590:
            ball.velocity[1] = -ball.velocity[1]
            lives -= 1
            if lives == 0:
                # display game over screen for 3 seconds
                message_display(screen, "GAME OVER", WIDTH, HEIGHT)
                # stop the game
                gameExit = False
        if ball.rect.y < 40:
            ball.velocity[1] = -ball.velocity[1]

        # detect collisions between the ball and the paddles
        if pygame.sprite.collide_mask(ball, paddle):
            ball.rect.x -= ball.velocity[0]
            ball.rect.y -= ball.velocity[1]
            ball.bounce()
        
        # check if there is the ball collides with any of bricks
        list_of_brick_collisions = pygame.sprite.spritecollide(ball, list_of_bricks, False)
        for brick in list_of_brick_collisions:
            ball.bounce()
            score += 1
            brick.kill()
            if len(list_of_bricks) == 0:
                # display level complete screen for 3 seconds
                message_display(screen, "LEVEL COMPLETE", WIDTH, HEIGHT)
                # stop the game
                gameExit = False

        # --- draw
        # 1. clear the screen
        screen.fill(DARKBLUE)
        pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

        # 2. display the score and the number of lives at the top of the screen
        font = pygame.font.Font('freesansbold.ttf', 34)
        text = font.render("Score: " + str(score), 1, WHITE)
        screen.blit(text, (20,10))
        text = font.render("Lives: " + str(lives), 1, WHITE)
        screen.blit(text, (650,10))

        # 3. draw list of sprites
        list_of_sprites.draw(screen)

        # --- update the screen
        pygame.display.flip()

        # --- Frame limit of 60 FPS
        clock.tick(60)

# game intro
intro = True
while intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                game_loop(running)
    
    screen.fill(WHITE)
    largeText = pygame.font.Font('freesansbold.ttf', 74)
    TextSurf, TextRect = text_objects("Breakout 2.0", largeText)
    TextRect.center = ((WIDTH/2),(HEIGHT/2))
    screen.blit(TextSurf, TextRect)
    smallText = pygame.font.Font('freesansbold.ttf', 40)
    TextStartSurf, TextStartRect = text_objects("Press SPACE to start", smallText)
    TextStartRect.center = ((WIDTH/2),(HEIGHT/2+100))
    screen.blit(TextStartSurf, TextStartRect)
    pygame.display.update()
    clock.tick(15)

# close the game
pygame.quit()
quit()




