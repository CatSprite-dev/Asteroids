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
pygame.display.set_caption("Астероиды - Меню")
# Шрифт
font = pygame.font.Font(None, FONT_SIZE)

score = 0
def draw_score():
    score_text = font.render(f"Очки: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))


# Функция для создания текста
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Функция для создания кнопки
def draw_button(surface, color, x, y, width, height, text):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, font, BLACK, surface, x + width // 2, y + height // 2)

# Основная функция меню
def main_menu():
    global score
    while True:
        screen.fill(BLACK)

        # Заголовок меню
        draw_text("Астероиды", font, WHITE, screen, SCREEN_WIDTH // 2, 100)

        # Координаты и размеры кнопок
        button_start = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_quit = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Отрисовка кнопок
        draw_button(screen, WHITE, button_start.x, button_start.y, BUTTON_WIDTH, BUTTON_HEIGHT, "Начать игру")
        draw_button(screen, WHITE, button_quit.x, button_quit.y, BUTTON_WIDTH, BUTTON_HEIGHT, "Выход")

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                score = 0
                if button_start.collidepoint(mouse_pos):
                    main()
                    return "start"  # Возвращаем "start", чтобы начать игру
                if button_quit.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        draw_score()
        # Обновление экрана
        pygame.display.flip()


def main():
    global score
    
    # pygame.init()
    print("Starting Asteroids!")
    # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
                main_menu()
                draw_score()
        
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.check_collision(shot) == True:
                    asteroid.split()
                    shot.kill()
                    score += 10
                    
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)
        
        draw_score()
        pygame.display.flip()
         

        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == "start":
            main()