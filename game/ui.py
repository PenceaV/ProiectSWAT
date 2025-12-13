import pygame as pg

class UI:
    def __init__(self, player):
        self.player = player
        self.heart_size = 30
        self.spacing = 10 
        self.heart_img = pg.Surface((self.heart_size, self.heart_size))
        self.heart_img.fill((255, 0, 0))

    def draw(self, screen):
        start_x = 1920 - 40 
        start_y = 20

        for i in range(self.player.health):
            offset = i * (self.heart_size + self.spacing)
            x = start_x - offset  
            y = start_y
            screen.blit(self.heart_img, (x, y))