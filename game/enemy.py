import pygame as pg
import math
import random
from game.bullet import Bullet

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pg.Surface((40, 40)) 
        self.image.fill((0, 255, 0)) 
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.pos = pg.math.Vector2(x, y)
        self.player = player
        self.speed = 0.25
        self.health = 2
        self.shoot_cooldown = 0
        self.shoot_delay = 60

    def move_towards_player(self, walls):
        dir_vector = pg.math.Vector2(self.player.rect.center) - self.pos
        
        if dir_vector.length() > 0: # Evitam impartirea la 0
            dir_vector = dir_vector.normalize()
        
        self.pos += dir_vector * self.speed
        self.rect.center = round(self.pos.x), round(self.pos.y)

        # Check de coliziune cu peretii (sa nu treaca prin ei)
        for wall in walls:
            if self.rect.colliderect(wall):
                # Daca loveste un perete, dam inapoi
                self.pos -= dir_vector * self.speed
                self.rect.center = round(self.pos.x), round(self.pos.y)

    def update(self, walls):
        self.move_towards_player(walls)

    def shoot_at_player(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            return None # Inca incarca arma
        
        dist = self.pos.distance_to(self.player.rect.center)
        if dist > 400:
            return None

        self.shoot_cooldown = self.shoot_delay
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        angle_to_player = math.degrees(math.atan2(-dy, dx)) - 90
        
        spread = random.uniform(-30, 30)
        final_angle = angle_to_player + spread

        return Bullet(self.rect.centerx, self.rect.centery, final_angle)

    def update(self, walls):
        self.move_towards_player(walls)

def spawn_enemies(coords_list, player, enemy_group, camera_group): 
    # Stergem inamicii vechi
    for enemy in list(enemy_group):
        enemy.kill()

    for pos in coords_list:
        # Adaugam 20 pentru centrare
        x = pos[0] + 20
        y = pos[1] + 20
        new_enemy = Enemy(x, y, player)
        enemy_group.add(new_enemy)
        camera_group.add(new_enemy)
    
    print(f"Spawned {len(coords_list)} enemies.")