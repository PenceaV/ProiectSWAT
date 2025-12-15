import pygame as pg
import math

from pygame.time import wait
from game.bullet import Bullet

pg.mixer.init()

red = (255, 0, 0)
img_path = "resources/sprites/swat.png"
empty_mag_sound = pg.mixer.Sound("resources/sound/empty_mag.mp3")
shoot = pg.mixer.Sound("resources/sound/gun_shot.mp3")
reload = pg.mixer.Sound("resources/sound/reload.mp3")
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        raw_image = pg.image.load(img_path).convert_alpha()

        # Rescaling imagine
        current_size = raw_image.get_size()
        scale_factor = 1.35
        new_size = (current_size[0] * scale_factor, current_size[1] * scale_factor)

        self.original_image = pg.transform.scale(raw_image, new_size)
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.center = (1280 // 2, 720 // 2)

        self.start_pos = (self.rect.centerx, self.rect.centery)
        self.pos = pg.math.Vector2(self.rect.center)

        self.hitbox = pg.Rect(0, 0, 35, 35)
        self.hitbox.center = self.rect.center

        self.correction_angle = 90
        self.velocity = 5
        self.angle = 0

        self.shoot = False
        self.cooldown = 0
        self.health = 5

        self.max_mag_ammo = 12
        self.current_mag_ammo = 12
        self.reserve_ammo = 48

        self.is_reloading = False
        self.reload_timer = 0
        self.reload_duration = 60 

    def update(self, walls, trees):
        """Ii da update caracterului cu toate functionalitatile"""

        # Daca reincarca, scadem timer-ul
        if self.is_reloading:
            self.reload_timer -= 1
            if self.reload_timer <= 0:
                self.finish_reload()

        self.movement(walls, trees)
        self.rotate()

        if self.cooldown > 0:
            self.cooldown -= 1

    def start_reload(self):
        """Incepe procesul de reincarcare daca sunt indeplinite conditiile"""
        # Nu reincarcam daca: deja reincarcam, incarcatorul e plin, sau nu avem rezerva
        if not self.is_reloading and self.current_mag_ammo < self.max_mag_ammo and self.reserve_ammo > 0:
            self.is_reloading = True
            self.reload_timer = self.reload_duration
            reload.play()
            print("Reloading...")

    def finish_reload(self):
        """Calculeaza munitia finala dupa ce a trecut timpul de reload"""
        bullets_needed = self.max_mag_ammo - self.current_mag_ammo

        if self.reserve_ammo >= bullets_needed:
            self.reserve_ammo -= bullets_needed
            self.current_mag_ammo = self.max_mag_ammo
        else:
            self.current_mag_ammo += self.reserve_ammo
            self.reserve_ammo = 0

        self.is_reloading = False

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

    def movement(self, walls, trees):
        keys = pg.key.get_pressed()

        obstacles = walls + trees

        if keys[pg.K_w]:
            self.hitbox.y -= self.velocity
            for obstacle in obstacles:
                if self.hitbox.colliderect(obstacle):
                    self.hitbox.top = obstacle.bottom

        if keys[pg.K_s]:
            self.hitbox.y += self.velocity
            for obstacle in obstacles:
                if self.hitbox.colliderect(obstacle):
                    self.hitbox.bottom = obstacle.top
        if keys[pg.K_a]:
            self.hitbox.x -= self.velocity
            for obstacle in obstacles:
                if self.hitbox.colliderect(obstacle):
                    self.hitbox.left = obstacle.right
        if keys[pg.K_d]:
            self.hitbox.x += self.velocity
            for obstacle in obstacles:
                if self.hitbox.colliderect(obstacle):
                    self.hitbox.right = obstacle.left

        self.rect.center = self.hitbox.center
        self.pos = pg.math.Vector2(self.hitbox.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_shooting(self):
        # verificam daca reincarca sau daca nu mai are gloante
        if self.is_reloading:
            return None

        if self.current_mag_ammo <= 0:
            empty_mag_sound.play()
            wait(60)
            return None

        if self.cooldown == 0:
            self.cooldown = 20

            self.current_mag_ammo -= 1
            shoot.play()
            
            offset = pg.math.Vector2(20, -5)
            rotated_offset = offset.rotate(-self.angle)
            bullet_start_pos = self.rect.center + rotated_offset

            return Bullet(bullet_start_pos.x, bullet_start_pos.y, self.angle)
        return None