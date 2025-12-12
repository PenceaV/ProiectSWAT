import pygame as pg
from game.player import Player
from game.editor import Editor
from game.camera import CameraGroup

pg.init()

SCREEN_SIZE = (1280, 720)
# TITLE = ... DE SCRIS

screen = pg.display.set_mode(SCREEN_SIZE, pg.RESIZABLE)
clock = pg.time.Clock()
player = Player()
editor = Editor()

camera_group = CameraGroup()
camera_group.add(player)

level_edit = False
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN and event.key == pg.K_F1:
            level_edit = not level_edit

    if pg.mouse.get_pressed()[0]: # apasat click stanga
        new_bullet = player.is_shooting()

        if new_bullet is not None:
            camera_group.add(new_bullet)
    wall_rects = [pg.Rect(pos[0], pos[1], editor.cell_size, editor.cell_size) for pos in editor.walls]

    screen.fill((0, 0, 0))
    if level_edit:
        editor.update(screen)
    else:
        camera_group.update(wall_rects)

        offset_x = player.rect.centerx - (SCREEN_SIZE[0] // 2)
        offset_y = player.rect.centery - (SCREEN_SIZE[1] // 2)
        camera_offset = (offset_x, offset_y)

        editor.draw(screen, offset=camera_offset)
        camera_group.custom_draw(player)


    pg.display.flip() # update screen
    clock.tick(60) # 60fps

pg.quit()