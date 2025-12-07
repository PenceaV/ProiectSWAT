import pygame as pg
from game.player import Player

pg.init()

SCREEN_SIZE = (1280, 720)
# TITLE = ... DE SCRIS

screen = pg.display.set_mode(SCREEN_SIZE, pg.RESIZABLE)
clock = pg.time.Clock()
player = Player()

all_sprites_group = pg.sprite.Group()
all_sprites_group.add(player)

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    if pg.mouse.get_pressed()[0]:   # apasat click stanga
        new_bullet = player.is_shooting()

        if new_bullet is not None:
            all_sprites_group.add(new_bullet)

    all_sprites_group.update() # toate functionalitatile 

    screen.fill((0, 0, 0))
    all_sprites_group.draw(screen)
    pg.display.flip() # update screen
    clock.tick(60) # 60fps

pg.quit()