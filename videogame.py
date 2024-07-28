import cv2
import mediapipe as mp
import pygame
import sys
import random

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1260, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Eggs")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Load images
farmer_img = pygame.image.load("farmer.jpg")
egg_img = pygame.image.load("egg.jpg")
golden_egg_img = pygame.image.load("golden_egg.jpg")
bomb_img = pygame.image.load("bomb.png")
background_img = pygame.image.load("forest.jpg")

# Resize images
farmer_size = (farmer_img.get_width() // 2, farmer_img.get_height() // 2)
farmer_img = pygame.transform.scale(farmer_img, farmer_size)
egg_size = (farmer_size[0] // 3, farmer_size[1] // 2.3)  # Resize egg to one-third the farmer's size
egg_img = pygame.transform.scale(egg_img, egg_size)
golden_egg_img = pygame.transform.scale(golden_egg_img, egg_size)
bomb_img = pygame.transform.scale(bomb_img, egg_size)
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Player properties
player_pos = [WIDTH // 2, HEIGHT - farmer_size[1]]  # Ensure the farmer is placed at the bottom

# Enemy (egg) properties
enemy_size = egg_size
enemy_list = []

# Golden egg properties
golden_egg_list = []

# Bomb properties
bomb_list = []

# Game properties
SPEED = 5
score = 0
lives = 3
level = 1
max_level = 10

# Set clock
clock = pygame.time.Clock()

# Capture video from webcam
cap = cv2.VideoCapture(0)


def detect_hand_position():
    success, img = cap.read()
    if not success:
        return None

    # Convert the image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * WIDTH
            return x

    return None

def drop_items(item_list, item_type):
    delay = random.random()
    if len(item_list) < 10 and delay < 0.05:  # Adjusted to 0.05 to make items less frequent
        x_pos = random.randint(0, WIDTH - enemy_size[0])
        y_pos = 0
        item_list.append([x_pos, y_pos, item_type])

def draw_items(item_list):
    for item_pos in item_list:
        if item_pos[2] == "egg":
            screen.blit(egg_img, (item_pos[0], item_pos[1]))
        elif item_pos[2] == "golden_egg":
            screen.blit(golden_egg_img, (item_pos[0], item_pos[1]))
        elif item_pos[2] == "bomb":
            screen.blit(bomb_img, (item_pos[0], item_pos[1]))

def update_item_positions(item_list):
    for idx, item_pos in enumerate(item_list):
        if item_pos[1] >= 0 and item_pos[1] < HEIGHT:
            item_pos[1] += SPEED
        else:
            item_list.pop(idx)

def collision_check(item_list, player_pos):
    global score, lives
    for item_pos in item_list[:]:
        if detect_collision(player_pos, item_pos):
            if item_pos[2] == "egg":
                score += 1
            elif item_pos[2] == "golden_egg":
                score += 5
            elif item_pos[2] == "bomb":
                lives -= 1
            item_list.remove(item_pos)

def detect_collision(player_pos, item_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    p_width = farmer_size[0]
    p_height = farmer_size[1]

    i_x = item_pos[0]
    i_y = item_pos[1]
    i_width = enemy_size[0]
    i_height = enemy_size[1]

    if (i_x + i_width > p_x and i_x < p_x + p_width) and (i_y + i_height > p_y and i_y < p_y + p_height):
        return True
    return False

def show_score(score):
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def show_lives(lives):
    font = pygame.font.SysFont(None, 35)
    lives_text = font.render(f'Lives: {lives}', True, WHITE)
    screen.blit(lives_text, (WIDTH - 120, 10))

def show_level(level):
    font = pygame.font.SysFont(None, 35)
    level_text = font.render(f'Level: {level}', True, WHITE)
    screen.blit(level_text, (WIDTH // 2 - 50, 10))

def game_over_screen(score):
    font = pygame.font.SysFont(None, 75)
    game_over_text = font.render('GAME OVER', True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    show_score(score)
    pygame.display.update()
    pygame.time.wait(3000)
    sys.exit()

def main_menu():
    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 75)
        title_text = font.render('Catch the Eggs', True, WHITE)
        play_text = font.render('Play', True, WHITE)
        quit_text = font.render('Quit', True, WHITE)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_text.get_rect(topleft=(WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2)).collidepoint(mouse_pos):
                    return
                if quit_text.get_rect(topleft=(WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 100)).collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

# Show main menu before starting the game
main_menu()

game_over = False

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    hand_x = detect_hand_position()
    if hand_x is not None:
        player_pos[0] = int(hand_x - farmer_size[0] / 2)

    screen.blit(background_img, (0, 0))

    # Drop different items
    drop_items(enemy_list, "egg")
    drop_items(golden_egg_list, "golden_egg")
    drop_items(bomb_list, "bomb")

    # Update item positions
    update_item_positions(enemy_list)
    update_item_positions(golden_egg_list)
    update_item_positions(bomb_list)

    # Draw items
    draw_items(enemy_list)
    draw_items(golden_egg_list)
    draw_items(bomb_list)

    # Check for collisions and update score/lives
    collision_check(enemy_list, player_pos)
    collision_check(golden_egg_list, player_pos)
    collision_check(bomb_list, player_pos)

    screen.blit(farmer_img, (player_pos[0], player_pos[1]))

    show_score(score)
    show_lives(lives)
    show_level(level)

    # Check for game over
    if lives <= 0:
        game_over_screen(score)

    # Increase difficulty based on score
    if score // 10 > level:
        level += 1
        SPEED += 1
        if level > max_level:
            max_level = level

    clock.tick(30)
    pygame.display.update()

cap.release()
pygame.quit()
