import pygame
import random
import sys
import os
import math
from sprite import load_character_sprites
#from sprite import bfs

pygame.init()
#Font
large_font = pygame.font.SysFont('Monster', 74, italic=True)
small_font = pygame.font.SysFont('Comic Sans MS', 30)

#Game_window
WIDTH, HEIGHT = 1008, 640
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MazeEscapeGame")

#Time
clock = pygame.time.Clock()
total_time = 90 #seconds
start_ticks = pygame.time.get_ticks() #Starts timer
message_timer = 0
#Colors
BLUE = (3, 3, 40)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN =(0, 255, 0)
WHITE =  (255, 255, 255)
#file paths
base_dir = os.path.dirname(__file__)
assets = os.path.join(base_dir, "assets")
#Sound Effects
pygame.mixer.music.load(os.path.join( assets, "pacman background music.ogg"))
pygame.mixer.music.play(-1) #Indefinite loop
pygame.mixer.music.set_volume(0.5)
key_sound = pygame.mixer.Sound(os.path.join(assets, "snd_purchase.wav"))
key_sound.set_volume(1.0)
win_sound = pygame.mixer.Sound(os.path.join(assets, "round_end.wav"))
win_sound.set_volume(1.0)
orb_sound = pygame.mixer.Sound(os.path.join(assets, "SFX_Powerup_01.wav"))
orb_sound.set_volume(1.0)
game_over_sound = pygame.mixer.Sound(os.path.join(assets, "losegamemusic.ogg"))
game_over_sound.set_volume(1.0)
#Maze layout
block_size = 25
cols = WIDTH // block_size
rows = HEIGHT // block_size
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],  
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
#Assets
#Orb
orb_x, orb_y = 0, 0 #Position
orb_rotation = 0 #Rotation angle
orb_active = False 
orb_image = pygame.image.load(os.path.join(assets,"orb.png")).convert_alpha()
orb_image = pygame.transform.scale(orb_image, (block_size, block_size)) #Ensures it fits in block
#Enemy images
patrol_image = pygame.image.load(os.path.join(assets,"patrol.png")).convert_alpha()
patrol_image = pygame.transform.scale(patrol_image, (block_size, block_size)) #Ensures it fits in block
chaser_image = pygame.image.load(os.path.join(assets,"chaser.png")).convert_alpha()
chaser_image = pygame.transform.scale(chaser_image, (block_size, block_size)) #Ensures it fits in block
enemy_size = block_size
#Player image
idle_images, run_images = load_character_sprites()
player_size = block_size - 4
#Key position and status
key_x = 15 * block_size #Position 
key_y = 10 * block_size
has_key = False #Check if player has key
key_image = pygame.image.load(os.path.join(assets, 'key.png'))
key_image = pygame.transform.scale(key_image, (block_size, block_size))
#Door image
door_image = pygame.image.load(os.path.join(assets, "door.png")).convert_alpha()
door_image = pygame.transform.scale(door_image, (block_size, block_size)) #Ensures it fits in block

#Check for collisions with walls
def can_move(x, y, maze, size):
    # Corners of the rectangle (player or enemy)
    corners = [
        (x, y),  # top-left
        (x + size, y),  # top-right
        (x, y + size),  # bottom-left
        (x + size, y + size),  # bottom-right
    ]
    for cx, cy in corners:
        grid_x = cx // block_size
        grid_y = cy // block_size

        if grid_x < 0 or grid_y < 0 or grid_x >= len(maze[0]) or grid_y >= len(maze):
            return False
        if maze[grid_y][grid_x] == 1:
            return False

    return True

has_won = False #win text

def get_random_empty_position():
    while True:
        x = random.randint(0, len(maze[0])- 1) * block_size
        y = random.randint(0, len(maze) - 1) * block_size
        if maze[y // block_size][x // block_size] == 0: #Posn not wall
            return x,y

def initialize_game():
    global direction, state, current_frame, player_x, player_y, enemies, orb_x, orb_y, orb_active, freeze_timer, key_x, key_y, has_key, has_won, start_ticks
    #Player start position in maze
    player_x = 25
    player_y = 25
    direction = 'right'
    state = 'idle'
    current_frame = 0

    orb_x, orb_y = get_random_empty_position() #Random position of powerUp
    orb_active = False
    freeze_timer = 0

    key_x, key_y = get_random_empty_position() #Random Position of Key
    has_key = False #Reset key status
    has_won = False #Resets win flag
    start_ticks = pygame.time.get_ticks() #Resets timer

    enemies = [
       {"x": 10 * block_size, "y": 7 * block_size, "speed_x": 10, "speed_y":10, "type": "chaser",'initial_speed_x': 10, 'initial_speed_y': 10},           
       {"x": 31 * block_size, "y": 2 * block_size, "speed_x": 5, "speed_y":10, "type": "patrol",'initial_speed_x': 5, 'initial_speed_y': 10},
       {"x": 8 * block_size, "y": 20 * block_size, "speed_x": 5, "speed_y":8, "type": "patrol",'initial_speed_x': 5, 'initial_speed_y': 8},
       {"x": 20 * block_size, "y": 14 * block_size, "speed_x": 10, "speed_y":10, "type": "chaser",'initial_speed_x': 10, 'initial_speed_y': 10},
       {"x": 20 * block_size, "y": 22 * block_size, "speed_x": 8, "speed_y":0, "type": "patrol",'initial_speed_x': 8, 'initial_speed_y': 0},
       {"x": 8 * block_size, "y": 11 * block_size, "speed_x": 8, "speed_y":0, "type": "patrol",'initial_speed_x': 8, 'initial_speed_y': 0},
       {"x": 23 * block_size, "y": 4 * block_size, "speed_x": 8, "speed_y":0, "type": "patrol",'initial_speed_x': 8, 'initial_speed_y': 0},
    ]

def move_enemies(maze, enemies, player_pos, block_size, step_size= block_size // 2):
    for enemy in enemies:
        ex, ey = enemy['x'], enemy['y']
        px, py = player_pos

        # Determine direction to move based on player's position
        if abs(px - ex) > abs(py - ey):  # Prioritize horizontal movement
            if px < ex and maze[ey // block_size][(ex - step_size) // block_size] == 0:
                enemy['x'] -= step_size  # Move left
            elif px > ex and maze[ey // block_size][(ex + step_size) // block_size] == 0:
                enemy['x'] += step_size  # Move right
        else:  # Prioritize vertical movement
            if py < ey and maze[(ey - step_size) // block_size][ex // block_size] == 0:
                enemy['y'] -= step_size  # Move up
            elif py > ey and maze[(ey + step_size) // block_size][ex // block_size] == 0:
                enemy['y'] += step_size  # Move down

def is_close(enemy_pos, player_pos, threshold=150):
    ex, ey = enemy_pos[0] + enemy_size // 2, enemy_pos[1] + enemy_size // 2
    px, py = player_pos[0] + player_size // 2, player_pos[1] + player_size // 2
    a = ex - px
    b = ey - py
    distance = math.sqrt(a ** 2 + b ** 2)
    #print(f"Distance to player: {distance}, Threshold: {threshold}")
    return distance < threshold

initialize_game()

# Main game loop
running = True
while running:
    
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill(BLUE) #Background
    #Draw maze
    for row in range(rows):
        for col in range(cols):
            if row < len(maze) and col < len(maze[row]): 
              if maze[row][col] == 1:
                color = BLACK 
                pygame.draw.rect(window, color, (col * block_size, row * block_size, block_size, block_size))
              elif maze[row][col] == 0:
                color = BLUE
                pygame.draw.rect(window,color,(col*block_size,row*block_size,block_size,block_size))
              elif maze[row][col] == 2: #Exit Door
                window.blit(door_image, (col * block_size, row * block_size))
            
    # Player movemnt
    player_speed = 5
    keys = pygame.key.get_pressed()
    #Direction Variables
    flip_horizontal = False
    rotation_angle = 0

    if keys[pygame.K_LEFT] and can_move(player_x - player_speed, player_y, maze, player_size):
        player_x -= player_speed
        state = "run"
        flip_horizontal = True
        rotation_angle = 0
    elif keys[pygame.K_RIGHT] and can_move(player_x + player_speed, player_y, maze, player_size ):
        player_x += player_speed
        state = "run"
        flip_horizontal = False
        rotation_angle = 0
    elif keys[pygame.K_UP] and can_move(player_x, player_y - player_speed, maze, player_size):
        player_y -= player_speed
        state = "run"
        flip_horizontal = False
        rotation_angle = 90
    elif keys[pygame.K_DOWN] and can_move(player_x, player_y + player_speed, maze, player_size):
        player_y += player_speed
        state = "run"
        flip_horizontal = False
        rotation_angle = 270
    else:
        state = "idle"
        rotation_angle = 0
    #Update player animation
    if state == 'run':
        character_image = run_images[current_frame]
    else:
        character_image = idle_images[current_frame]
    #Player Rotation
    if flip_horizontal:
        character_image = pygame.transform.flip(character_image, True, False)
    if rotation_angle != 0:
        character_image = pygame.transform.rotate(character_image, rotation_angle)
    #Animate Player
    current_frame = (current_frame + 1) % 10 #loops through 10 frames
    scaled_image = pygame.transform.scale(character_image, (player_size, player_size))
    #InsertPlayer
    window.blit(scaled_image, (player_x, player_y))
    # Enemy movement
    for enemy in enemies:
        if enemy["type"] == "patrol":
           enemy['speed_x'] = min(enemy['speed_x'], block_size)
           enemy['speed_y'] = min(enemy['speed_y'], block_size)
           
           if can_move(enemy['x'] + enemy['speed_x'], enemy['y'], maze, enemy_size):
            enemy['x'] += enemy['speed_x']
           else:
              enemy['speed_x'] *= -1 #Reverse direction
              if can_move(enemy['x'], enemy['y'] + enemy['speed_y'], maze, enemy_size):
                 enemy["y"] += enemy['speed_y']
              else:
                 enemy['speed_y'] *= -1

        elif enemy['type'] == "chaser":
            # Align enemy position to grid
            enemy['x'] = (enemy['x'] // block_size) * block_size
            enemy['y'] = (enemy['y'] // block_size) * block_size

            # Check if the enemy is close enough to start chasing
            if is_close((enemy['x'], enemy['y']), (player_x, player_y), threshold=150):
                px, py = player_x // block_size, player_y // block_size
                ex, ey = enemy['x'] // block_size, enemy['y'] // block_size

                dx = px - ex
                dy = py - ey
                # Initialize cooldown timer if not already set
                enemy["direction_cooldown"] = enemy.get("direction_cooldown", 0)

                # Reduce cooldown timer
                if enemy["direction_cooldown"] > 0:
                    enemy["direction_cooldown"] -= 1
                else:
                    # Store previous direction to avoid jittering
                    prev_direction = enemy.get("prev_direction", (0, 0))

                    # Prioritize movement direction
                    directions = []
                    if abs(dx) > abs(dy):  # Horizontal priority
                        directions = [(1 if dx > 0 else -1, 0), (0, 1 if dy > 0 else -1)]
                    else:  # Vertical priority
                        directions = [(0, 1 if dy > 0 else -1), (1 if dx > 0 else -1)]
                    
                    # Attempt movement in prioritized directions
                    moved = False
                    for step_x, step_y in directions:
                        new_x = enemy['x'] + step_x * block_size
                        new_y = enemy['y'] + step_y * block_size

                        # Avoids reversing direction unnecessarily
                        if (step_x, step_y) != (-prev_direction[0], -prev_direction[1]) and can_move(new_x, new_y, maze, enemy_size):
                           enemy['x'] += step_x * block_size
                           enemy['y'] += step_y * block_size
                           enemy["prev_direction"] = (step_x, step_y)  # Update previous direction
                           enemy["direction_cooldown"] = 5  # Sets cooldown period
                           moved = True
                           break
                    # If no movement is possible, resets previous direction
                    if not moved:
                       enemy["prev_direction"] = (0, 0)  # No movement

    # Check for collision with player
        if abs(enemy["x"] - player_x) < block_size and abs(enemy["y"] - player_y) < block_size: 
            game_over_sound.play()
            print('Game Over!')
            text = large_font.render("YOU WERE CAUGHT!", True, RED)
            window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000) #Waits3seconds
            initialize_game()
            start_ticks = pygame.time.get_ticks()
            continue #ResetsGame
        #Insert Enemy images 
        if enemy['type'] == 'patrol':
            window.blit(patrol_image, (enemy["x"], enemy["y"]))
        elif enemy["type"] == 'chaser':
            window.blit(chaser_image, (enemy["x"], enemy["y"]))
    
    #key rendering
    if not has_key:
        window.blit(key_image, (key_x, key_y)) #Inserts key image

    #Check if player has collected key
    if not has_key and abs(player_x - key_x) < block_size and abs(player_y - key_y) < block_size:
        key_sound.play()
        has_key = True #Key collected
        print('key collected')

    # Power-ups 
    if not orb_active and abs(player_x-orb_x) < block_size and abs(player_y - orb_y) < block_size:
        orb_sound.play()
        orb_active = True
        freeze_timer = pygame.time.get_ticks() # start timer freeze

    # Freeze time for 5secs
    if orb_active:
        for enemy in enemies:
            enemy["speed_x"] = 0
            enemy["speed_y"] = 0 #Stop all enemies

        # Unfreeze after 5 seconds
        if pygame.time.get_ticks() - freeze_timer > 5000:
            orb_active = False #Deactivates PowerUp
            orb_x, orb_y = get_random_empty_position() #Respawn orb
            for enemy in enemies:
                if "initial_speed_x" in enemy and "initial_speed_y" in enemy:
                  enemy["speed_x"] = enemy['initial_speed_x'] 
                  enemy["speed_y"] = enemy['initial_speed_y']  #Restore timer
    if not orb_active:
        orb_rotation = (orb_rotation + 5) % 360 #Rotates
        rotated_orb = pygame.transform.rotate(orb_image, orb_rotation)
        orb_rect = rotated_orb.get_rect(center =(orb_x + block_size // 2, orb_y + block_size // 2))
        window.blit(rotated_orb, orb_rect)
        
    if maze[player_y // block_size][player_x // block_size] == 2: #Win condition
        if not has_key:
            if message_timer == 0:
                message_timer = pygame.time.get_ticks()
            if pygame.time.get_ticks() - message_timer < 1000:
                get_key_text = large_font.render('Get key first!', True, WHITE)
                text_rect = get_key_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                window.blit(get_key_text, text_rect)
                pygame.display.flip()
            else:
                message_timer = 0
        else:
            win_sound.play()
            has_won = True #Win flag
            print("You Win")#Print win message once
            win_text = large_font.render("You Win!", True, GREEN)
            text_rect = win_text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
            window.blit(win_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)#Waits for 3 seconds
            initialize_game() #Resets game
            continue

    #Timer Display
    elapsed_ticks = pygame.time.get_ticks() - start_ticks
    remaining_time = total_time - elapsed_ticks // 1000

    if remaining_time <= 0 and not has_won:
        game_over_sound.play()
        game_over_text = large_font.render("TIME'S UP! GAME OVER!", True, WHITE)
        text_rect = game_over_text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        window.blit(game_over_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000) #waits for 3 seconds
        initialize_game() #ResetsGame
        continue

    else:
        #Remaining time in MM:SS
        minutes = remaining_time // 60 #minute
        seconds = remaining_time % 60 #reminder
        timer_text = small_font.render(f'Time left: {minutes:01}:{seconds:02}', True, WHITE)
    window.blit(timer_text, (800, 0)) #Top-left corner
    pygame.display.flip()   #Update the Display Window
    clock.tick(30) # Run loop at 30 Frames Per Second (FPS)

pygame.quit()
sys.exit()









