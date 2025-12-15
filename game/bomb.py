import pygame as pg

class Bomb(pg.sprite.Sprite):
    def __init__(self, pos, cell_size):
        super().__init__()
        self.image = pg.image.load("resources/sprites/bomb.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect(topleft=pos)