import pygame as pg
import math
import os

red = (255, 0, 0)
img_path = "resources/sprites/swat.png"

class Player:
    def __init__(self):
        raw_image = pg.image.load(img_path).convert_alpha()

        # Rescaling imagine - ! mai trb sa vedem aici cum se potriveste cel mai bine scaling_factor
        current_size = raw_image.get_size()
        scale_factor = 1.35
        new_size = (current_size[0] * scale_factor, current_size[1] * scale_factor)
        
        self.original_image = pg.transform.scale(raw_image, new_size)
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.center = (1280//2, 720//2)

        self.correction_angle = 90 # directia player
        self.velocity = 5

    def update(self):
        """Ii da update caracterului cu toate functionalitatile"""
        self.movement()
        self.rotate()

    def rotate(self):
        """Roteste caracterul dupa pozitia cursorului"""
        mx, my = pg.mouse.get_pos()
        dx, dy = mx - self.rect.centerx, my - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - self.correction_angle

        self.image = pg.transform.rotate(self.original_image, angle)

        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def movement(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.rect.y -= self.velocity
        if keys[pg.K_s]:
            self.rect.y += self.velocity
        if keys[pg.K_a]:
            self.rect.x -= self.velocity
        if keys[pg.K_d]:
            self.rect.x += self.velocity


    def draw(self, screen):
        screen.blit(self.image, self.rect)