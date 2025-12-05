import pygame as pg
from game.player import Player

pg.init()

SCREEN_SIZE = (1280, 720)
# TITLE = ... DE SCRIS

screen = pg.display.set_mode(SCREEN_SIZE, pg.RESIZABLE)
clock = pg.time.Clock()
player = Player()

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    player.update() # toate functionalitatile player-ului

    screen.fill((0, 0, 0))
    player.draw(screen)
    pg.display.flip() # update screen
    clock.tick(60) # 60fps

pg.quit()