import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Initialize sound mixer
pygame.mixer.init()

# Load sound effects
snd_paddle = pygame.mixer.Sound("sounds/paddle_hit.wav")
snd_wall = pygame.mixer.Sound("sounds/wall_hit.wav")
snd_brick = pygame.mixer.Sound("sounds/brick_break.mp3")
snd_win = pygame.mixer.Sound("sounds/win_jingle.wav")
snd_lose = pygame.mixer.Sound("sounds/lose_jingle.wav")
snd_brick.set_volume(0.6)  # 0.0 to 1.0

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 8
BRICK_ROWS, BRICK_COLS = 5, 10
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
BRICK_GAP = 5
PADDLE_SPEED = 6

# Colors
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
BRICK_COLORS = [(255, 65, 54), (255, 133, 27), (255, 220, 0), (46, 204, 64), (0, 116, 217)]

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Clone")
clock = pygame.time.Clock()

# Game state
paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
ball_x, ball_y = WIDTH // 2, HEIGHT - 50
ball_dx, ball_dy = 4, -4
score, lives = 0, 3
game_over = False

# Create bricks
bricks = []
for row in range(BRICK_ROWS):
    brick_row = []
    for col in range(BRICK_COLS):
        x = col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP
        y = row * (BRICK_HEIGHT + BRICK_GAP) + 50
        brick_row.append(pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT))
    bricks.append(brick_row)
brick_active = [[True for _ in range(BRICK_COLS)] for _ in range(BRICK_ROWS)]

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += PADDLE_SPEED

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Wall collision
        if ball_x - BALL_RADIUS < 0 or ball_x + BALL_RADIUS > WIDTH:
            snd_wall.play()
            ball_dx = -ball_dx
        if ball_y - BALL_RADIUS < 0:
            snd_wall.play()
            ball_dy = -ball_dy

        # Bottom out
        if ball_y + BALL_RADIUS > HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
                snd_lose.play()
            else:
                # Reset ball and paddle
                ball_x, ball_y = WIDTH // 2, HEIGHT - 50
                ball_dx, ball_dy = 4, -4
                paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2

        # Paddle collision
        paddle_rect = pygame.Rect(paddle_x, HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
        if paddle_rect.collidepoint(ball_x, ball_y + BALL_RADIUS):
            snd_paddle.play()
            ball_dy = -abs(ball_dy)
            hit_pos = (ball_x - paddle_x) / PADDLE_WIDTH
            ball_dx = 8 * (hit_pos - 0.5) + random.uniform(-1, 1)
            if abs(ball_dx) < 1:
                ball_dx = 1 if ball_dx >= 0 else -1

        # Brick collision
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                if brick_active[row][col]:
                    brick_rect = bricks[row][col]
                    if brick_rect.collidepoint(ball_x, ball_y):
                        brick_active[row][col] = False
                        snd_brick.play()
                        ball_dy = -ball_dy
                        score += 10
                        print('Score ='+ str(score))
                        print('Max score ='+ str(BRICK_ROWS * BRICK_COLS * 10))
                        # Win condition
                        if score == BRICK_ROWS * BRICK_COLS * 10:
                            game_over = True
                            snd_win.play()

    # Draw bricks
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            if brick_active[row][col]:
                pygame.draw.rect(screen, BRICK_COLORS[row], bricks[row][col])

    # Draw paddle
    pygame.draw.rect(screen, CYAN, (paddle_x, HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_RADIUS)

    # Draw score and lives
    font = pygame.font.SysFont("Arial", 20)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))

    if game_over:
        end_font = pygame.font.SysFont("Arial", 48)
        if score == BRICK_ROWS * BRICK_COLS * 10:
            msg = "🎉 You Win! 🎉"
        else:
            msg = "💀 Game Over 💀"
        msg_text = end_font.render(msg, True, WHITE)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, HEIGHT // 2 - 30))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
