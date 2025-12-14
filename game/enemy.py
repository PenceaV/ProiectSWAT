import pygame as pg
import math
import random
from shapely import geometry
from game.bullet import Bullet

import pygame as pg
import math
import random
from shapely import geometry
from game.bullet import Bullet


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        # 1. Incarcam imaginea si o salvam ca ORIGINAL_IMAGE
        raw_image = pg.image.load("resources/sprites/taliban.png").convert_alpha()
        self.original_image = pg.transform.scale(raw_image, (80, 80))

        # self.image este ceea ce desenam pe ecran (cea rotita)
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.pos = pg.math.Vector2(x, y)
        self.player = player
        self.speed = 1.5
        self.health = 2

        self.shoot_cooldown = 0
        self.shoot_delay = 80

        self.in_light = False
        self.activation_distance = 450

        self.image.set_alpha(0)

    def rotate(self):
        # Calculam diferentele de coordonate
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        # Calculam unghiul in grade
        # -dy este necesar pentru ca axa Y e inversata in Pygame
        # -90 este necesar daca sprite-ul tau original sta cu fata in SUS.
        # Daca sta cu fata la DREAPTA, sterge "- 90".
        angle = math.degrees(math.atan2(-dy, dx)) - 90

        # Rotim imaginea originala
        self.image = pg.transform.rotate(self.original_image, angle)

        # IMPORTANT: Recalculam rect-ul ca sa ramana centrat
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, walls, shadows, camera_offset):
        # 1. Rotim inamicul mereu spre jucator (chiar si in intuneric)
        # sau poti pune asta in if-ul de mai jos daca vrei sa se roteasca doar cand te vede
        self.rotate()

        # 2. Logica de distanta si umbre
        dist_to_player = self.pos.distance_to(self.player.rect.center)

        screen_x = self.rect.centerx - camera_offset[0]
        screen_y = self.rect.centery - camera_offset[1]
        enemy_point = geometry.Point(screen_x, screen_y)

        is_hidden = False
        for shadow in shadows:
            if shadow.polygon.contains(enemy_point):
                is_hidden = True
                break

        self.in_light = not is_hidden

        # 3. Aplicam transparenta DUPA rotire (pentru ca rotate creaza o suprafata noua)
        if self.in_light:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)

        # 4. Miscare
        if self.in_light or dist_to_player < self.activation_distance:
            self.move_towards_player(walls)
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1

    def move_towards_player(self, walls):
        dir_vector = pg.math.Vector2(self.player.rect.center) - self.pos

        if dir_vector.length() > 0:
            dir_vector = dir_vector.normalize()

        old_pos = self.pos.copy()

        self.pos += dir_vector * self.speed
        self.rect.center = round(self.pos.x), round(self.pos.y)

        for wall in walls:
            if self.rect.colliderect(wall):
                self.pos = old_pos
                self.rect.center = round(self.pos.x), round(self.pos.y)
                break

    def shoot_at_player(self, player_health):
        if not self.in_light:
            return None

        if not player_health:
            return None

        if self.shoot_cooldown > 0:
            return None

        dist = self.pos.distance_to(self.player.rect.center)
        if dist > 400:
            return None

        self.shoot_cooldown = self.shoot_delay

        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        angle_to_player = math.degrees(math.atan2(-dy, dx)) - 90

        spread = random.uniform(-10, 10)
        final_angle = angle_to_player + spread

        return Bullet(self.rect.centerx, self.rect.centery, final_angle)


def spawn_enemies(coords_list, player, enemy_group, camera_group):
    for enemy in list(enemy_group):
        enemy.kill()

    for pos in coords_list:
        x = pos[0] + 20
        y = pos[1] + 20
        new_enemy = Enemy(x, y, player)
        enemy_group.add(new_enemy)
        camera_group.add(new_enemy)

    print(f"Spawned {len(coords_list)} enemies.")