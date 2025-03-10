import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot
count_dt = 0

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def engine_fire(self):
        forward = pygame.Vector2(0, -2).rotate(self.rotation)
        right = pygame.Vector2(0, 7).rotate(self.rotation + 90)
        i = pygame.Vector2(0, -20).rotate(self.rotation)
        a = self.position + forward * self.radius
        b = self.position + i - right
        c = self.position + i + right
        return [a, b, c]


    def draw(self, screen, dt):
        global count_dt
        keys = pygame.key.get_pressed()
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        if keys[pygame.K_w] and self.timer <= 0:
            pygame.draw.polygon(screen, "white", self.engine_fire(), 2)
            

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.timer -= dt
        
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt, 1)
        if keys[pygame.K_s]:
            self.move(dt, -1)

        self.velocity *= 0.99
        self.position += self.velocity * dt

        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        
        if keys[pygame.K_SPACE]:
            self.shoot()
        
    
    def move(self, dt, val):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * val
        self.position += self.velocity * dt


    def shoot(self):
        if self.timer <= 0:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.timer = PLAYER_SHOOT_COOLDOWN