import pygame
import random
import time

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
WINNING_SCORE = 5

# Function to draw the center line
def draw_center_line(screen):
    for y in range(0, SCREEN_HEIGHT, 20):
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 1, y, 2, 10))


def main():
    pygame.init() # Initialize Pygame
    
    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Game")
    font = pygame.font.SysFont(None, 60)
    winner_font = pygame.font.SysFont(None, 80)

    # Create paddles and ball
    left_paddle = pygame.Rect(20, (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(SCREEN_WIDTH - 20 - PADDLE_WIDTH, (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
    ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

    clock = pygame.time.Clock()

    left_score = 0
    right_score = 0
    paused = False
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        draw_center_line(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    paused = not paused

        keys = pygame.key.get_pressed()

        if not paused:
            if keys[pygame.K_w] and left_paddle.top > 0:
                left_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_s] and left_paddle.bottom < SCREEN_HEIGHT:
                left_paddle.y += PADDLE_SPEED
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
                right_paddle.y += PADDLE_SPEED

            ball.x += ball_speed_x
            ball.y += ball_speed_y

            if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
                ball_speed_y *= -1
            if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
                ball_speed_x *= -1

            if ball.left <= 0:
                right_score += 1
                ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                ball_speed_x *= random.choice((1, -1))
                ball_speed_y *= random.choice((1, -1))

            if ball.right >= SCREEN_WIDTH:
                left_score += 1
                ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                ball_speed_x *= random.choice((1, -1))
                ball_speed_y *= random.choice((1, -1))

            if left_score == WINNING_SCORE:
                winner_text = winner_font.render("Left Player Wins!", True, GREEN)
                screen.blit(winner_text, (SCREEN_WIDTH//2 - winner_text.get_width()//2, SCREEN_HEIGHT//2 - 40))
                pygame.display.flip()
                time.sleep(5)
                left_score = 0
                right_score = 0

            elif right_score == WINNING_SCORE:
                winner_text = winner_font.render("Right Player Wins!", True, GREEN)
                screen.blit(winner_text, (SCREEN_WIDTH//2 - winner_text.get_width()//2, SCREEN_HEIGHT//2 - 40))
                pygame.display.flip()
                time.sleep(5)
                left_score = 0
                right_score = 0

        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (SCREEN_WIDTH//4, 20))
        screen.blit(right_text, (SCREEN_WIDTH*3//4, 20))
        pygame.draw.rect(screen, WHITE, screen.get_rect(), 4)

        if paused:
            pause_text = font.render("Paused", True, WHITE)
            screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()