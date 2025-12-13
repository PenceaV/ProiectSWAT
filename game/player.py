
import pygame as pg
import math
import os

from game.bullet import Bullet

red = (255, 0, 0)
img_path = "resources/sprites/swat.png"

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        raw_image = pg.image.load(img_path).convert_alpha()

        # Rescaling imagine - ! mai trb sa vedem aici cum se potriveste cel mai bine scaling_factor
        current_size = raw_image.get_size()
        scale_factor = 1.35
        new_size = (current_size[0] * scale_factor, current_size[1] * scale_factor)
        
        self.original_image = pg.transform.scale(raw_image, new_size)
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.center = (1280//2, 720//2)

        self.start_pos = (self.rect.centerx, self.rect.centery)
        self.pos = pg.math.Vector2(self.rect.center)

        # hitbox nou mai mic decat imaginea
        # mai usor sa intre pe usa
        self.hitbox = pg.Rect(0, 0, 35, 35)
        self.hitbox.center = self.rect.center

        self.correction_angle = 90 # directia player
        self.velocity = 5
        self.angle = 0

        self.shoot = False
        self.cooldown = 0
        self.health = 5

    def update(self, walls):
        """Ii da update caracterului cu toate functionalitatile"""
        self.movement(walls)
        self.rotate()

        if self.cooldown > 0:
            self.cooldown -= 1

    def rotate(self):
        mx, my = pg.mouse.get_pos()

        screen_center_x = 1280 // 2
        screen_center_y = 720 // 2

        dx = mx - screen_center_x
        dy = my - screen_center_y

        self.angle = math.degrees(math.atan2(-dy, dx)) - self.correction_angle
        self.image = pg.transform.rotate(self.original_image, self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = self.hitbox.center

    def movement(self, walls):
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.hitbox.y -= self.velocity
            for wall in walls:
                if self.hitbox.colliderect(wall):
                    self.hitbox.top = wall.bottom
        if keys[pg.K_s]:
            self.hitbox.y += self.velocity
            for wall in walls:
                if self.hitbox.colliderect(wall):
                    self.hitbox.bottom = wall.top
        if keys[pg.K_a]:
            self.hitbox.x -= self.velocity
            for wall in walls:
                if self.hitbox.colliderect(wall):
                    self.hitbox.left = wall.right
        if keys[pg.K_d]:
            self.hitbox.x += self.velocity
            for wall in walls:
                if self.hitbox.colliderect(wall):
                    self.hitbox.right = wall.left

        self.rect.center = self.hitbox.center
        self.pos = pg.math.Vector2(self.hitbox.center)


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_shooting(self):
        if self.cooldown == 0:
            self.cooldown = 20
            
            offset = pg.math.Vector2(20, -5)
            rotated_offset = offset.rotate(-self.angle)
            bullet_start_pos = self.rect.center + rotated_offset
            
            return Bullet(bullet_start_pos.x, bullet_start_pos.y, self.angle)   
        return None 