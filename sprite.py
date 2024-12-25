import pygame
import os

base_dir = os.path.dirname(__file__)
assets = os.path.join(base_dir, "assets")

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

