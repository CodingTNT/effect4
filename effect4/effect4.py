import pygame
import random
import time

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Responsive Rain Effect with Thunder, Lightning, and Umbrella")

original_drop_image = pygame.image.load("drop.png")
drop_width, drop_height = original_drop_image.get_size()

umbrella_image = pygame.image.load("umbrella.png")
umbrella_scale_factor = 0.25 
umbrella_width = int(umbrella_image.get_width() * umbrella_scale_factor)
umbrella_height = int(umbrella_image.get_height() * umbrella_scale_factor)
umbrella_image = pygame.transform.scale(umbrella_image, (umbrella_width, umbrella_height))


pygame.mixer.init()
pygame.mixer.music.load("rainfall.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

thunder_sound = pygame.mixer.Sound("Thunder.wav")
thunder_sound.set_volume(0.8)  

NUM_DROPS = 100
drops = [
    {
        "x": random.randint(0, SCREEN_WIDTH - drop_width),
        "y": random.randint(-SCREEN_HEIGHT, 0),
        "speed": random.randint(2, 7),
        "scale": random.uniform(0.3, 0.8), 
        "alpha": random.randint(50, 200),  
    }
    for _ in range(NUM_DROPS)
]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
clock = pygame.time.Clock()

flash_screen = False
flash_duration = 10  
flash_counter = 0
flash_time = 0  

running = True
while running:
    current_time = time.time() 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            flash_time = current_time + 0.5 
            flash_screen = True  
            flash_counter = flash_duration  

            
            pygame.time.set_timer(pygame.USEREVENT, 500) 

            
            for drop in drops:
                drop["speed"] += random.randint(2, 5)  

    
    if flash_screen:
        if flash_counter > 0:
            if flash_counter % 2 == 0:
                screen.fill(WHITE)  
            else:
                screen.fill(BLACK)  
            flash_counter -= 1
        else:
            flash_screen = False 

    
    for drop in drops:
        drop["y"] += drop["speed"]

        
        umbrella_x, umbrella_y = pygame.mouse.get_pos()
        umbrella_x -= umbrella_width // 2
        umbrella_y -= umbrella_height // 2
        
        if umbrella_x < drop["x"] < umbrella_x + umbrella_width and umbrella_y < drop["y"] < umbrella_y + umbrella_height:
            drop["alpha"] = 0  

       
        if drop["y"] > SCREEN_HEIGHT:
            drop["y"] = random.randint(-drop_height, 0)
            drop["x"] = random.randint(0, SCREEN_WIDTH - drop_width)
            drop["speed"] = random.randint(2, 7)
            drop["scale"] = random.uniform(0.2, 0.8) 
            drop["alpha"] = random.randint(50, 500)


    mouse_x, mouse_y = pygame.mouse.get_pos()
    umbrella_x = mouse_x - umbrella_width // 2
    umbrella_y = mouse_y - umbrella_height // 2

    
    if not flash_screen:  
        screen.fill(BLACK)

   
    for drop in drops:
        
        scaled_width = int(drop_width * drop["scale"])
        scaled_height = int(drop_height * drop["scale"])
        scaled_image = pygame.transform.scale(original_drop_image, (scaled_width, scaled_height))
        
        scaled_image.set_alpha(drop["alpha"])
        
        screen.blit(scaled_image, (drop["x"], drop["y"]))

    screen.blit(umbrella_image, (umbrella_x, umbrella_y))

    pygame.display.flip()
    clock.tick(FPS)

    if current_time >= flash_time and flash_time > 0:
        thunder_sound.play()
        flash_time = 0  

pygame.mixer.music.stop()
pygame.quit()
