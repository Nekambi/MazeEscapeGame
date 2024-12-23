import pygame
import os 
from collections import deque
import os

assets = 'assets'
#Image loader
def load_images(folder_path, num_images):
    images = [] #holds loaded images
    
    for i in range(num_images): #loops through images
        image_path = os.path.join(folder_path, f"{os.path.basename(folder_path)}_{i}.png")
        image = pygame.image.load(image_path) #Loads image
        images.append(image) #Adds image to list
        
    return images

#Initialises the images
def load_character_sprites():
    idle_images = load_images(os.path.join(assets, "player", "idle"), 10)
    run_images = load_images(os.path.join(assets, "player", "run"), 10)
    return idle_images, run_images

#BFS for enenemy
def bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1] 
        
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #Only Vertical and horizontal movement
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols: #Checks Bounds
                if maze[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited: #Walkable check
                    #print(f'Adding neighbor {neighbor} to the queue.')
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current
                
    return[] #No path found