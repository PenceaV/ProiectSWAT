import pygame as pg
import math
import random
from shapely import geometry
from game.bullet import Bullet

pg.mixer.init()
shoot = pg.mixer.Sound("resources/sound/gun_shot.mp3")

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        raw_image = pg.image.load("resources/sprites/taliban.png").convert_alpha()
        self.original_image = pg.transform.scale(raw_image, (80, 80))

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.pos = pg.math.Vector2(x, y)
        self.player = player
        self.speed = 1.5
        self.health = 2

        self.shoot_cooldown = 0
        self.shoot_delay = 60
        self.reaction_time = 40  
        self.current_reaction = self.reaction_time

        self.in_light = False
        self.activation_distance = 450

        self.image.set_alpha(0)

    def rotate(self):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - 90

        self.image = pg.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, walls, shadows, camera_offset):
        self.rotate()
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

        if self.in_light:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)

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

    def check_line_of_sight(self, walls):
        line_start = self.rect.center
        line_end = self.player.rect.center
        
        for wall in walls:
            # Clipline da check daca linia trece prin rect
            if wall.clipline(line_start, line_end):
                return False # Vederea e blocata de un perete
        return True

    def shoot_at_player(self, player_health, walls):
        if not self.in_light:
            return None

        if not player_health:
            return None

        if self.shoot_cooldown > 0:
            return None

        dist = self.pos.distance_to(self.player.rect.center)
        if dist > 400:
            return None
        
        can_see = self.check_line_of_sight(walls)
        
        if not can_see:
            # Daca s a ascuns, resetam
            self.current_reaction = self.reaction_time
            return None
        
        if self.current_reaction > 0:
            self.current_reaction -= 1
            return None

        self.shoot_cooldown = self.shoot_delay

        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        angle_to_player = math.degrees(math.atan2(-dy, dx)) - 90

        spread = random.uniform(-10, 10)
        final_angle = angle_to_player + spread
        shoot.play()

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