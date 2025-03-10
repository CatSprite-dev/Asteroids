import sys
import pygame
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import *
from circleshape import CircleShape
from shot import Shot

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Астероиды")

font = pygame.font.Font(None, FONT_SIZE) 
score = 0
players = {"unknown": 0}
current_user = "unknown"

def draw_score():
    score_text = font.render(f"{current_user}: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(surface, color, x, y, width, height, text):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, font, BLACK, surface, x + width // 2, y + height // 2)

def main_menu():
    global score
    global current_user
    while True:
        screen.fill(BLACK)
        
        # Заголовок меню
        draw_text("Астероиды", font, WHITE, screen, SCREEN_WIDTH // 2, 100)

        button_start = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_quit = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_new_player = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT)

        draw_button(screen, WHITE, button_start.x, button_start.y, BUTTON_WIDTH, BUTTON_HEIGHT, "Начать игру")
        draw_button(screen, WHITE, button_quit.x, button_quit.y, BUTTON_WIDTH, BUTTON_HEIGHT, "Выход")
        draw_button(screen, WHITE, button_new_player.x, button_new_player.y, BUTTON_WIDTH, BUTTON_HEIGHT, "Новый игрок")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_start.collidepoint(mouse_pos):
                    main()
                if button_new_player.collidepoint(mouse_pos):
                    current_user = input_name()
                if button_quit.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        draw_score()

    
        pygame.display.flip()

def input_name():
    input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 70, 334, 140, 32) 
    user_text = ""
    while True:
        screen.fill(BLACK)
        
        # Заголовок меню
        draw_text("Введите имя игрока:", font, WHITE, screen, SCREEN_WIDTH // 2, 250)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    players[user_text] = score
                    return user_text
                else: 
                    user_text += event.unicode

        pygame.draw.rect(screen, GRAY, input_rect)
        draw_text(user_text, font, WHITE, screen, SCREEN_WIDTH // 2, 350)

        pygame.display.flip()

def main():
    global score
    score = 0
    clock = pygame.time.Clock()
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2   )
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        updatable.update(dt)  
        for asteroid in asteroids:
            if asteroid.check_collision(player) == True:
                print("Game Over!")
                return
        
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.check_collision(shot) == True:
                    asteroid.split()
                    shot.kill()
                    if asteroid.radius == ASTEROID_MAX_RADIUS: 
                        score += 1
                    elif asteroid.radius == ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS:
                        score += 2
                    else:
                        score += 3
                    
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen, dt)
        
        draw_score()
        pygame.display.flip()
         

        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    main_menu()
        