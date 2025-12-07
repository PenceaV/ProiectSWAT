import pygame as pg
import math

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,angle):
        super().__init__()
        self.image = pg.Surface((5,5))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(center=(x,y))
        
        self.x=x
        self.y=y
        self.angle=angle+90  # ajustam pentru correction_angle

        self.speed=50
        self.x_velocity=math.cos(self.angle * (2*math.pi/360)) * self.speed
        self.y_velocity=-math.sin(self.angle * (2*math.pi/360)) * self.speed

    def movement(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update(self):
        self.movement()
        # Daca glontul iese de pe ecran il distrugem
        if self.rect.x < 0 or self.rect.x > 1280 or self.rect.y < 0 or self.rect.y > 720:
            self.kill()
