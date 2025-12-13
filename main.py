import pygame as pg
from game.player import Player
from game.editor import Editor
from game.camera import CameraGroup
from game.enemy import Enemy, spawn_enemies
from game.ui import UI

pg.init()

SCREEN_SIZE = (1920, 1080)
# TITLE = ... DE SCRIS

screen = pg.display.set_mode(SCREEN_SIZE, pg.RESIZABLE)
clock = pg.time.Clock()
player = Player()
editor = Editor()
ui = UI(player)

camera_group = CameraGroup()
camera_group.add(player)
bullets = pg.sprite.Group()
enemy_group = pg.sprite.Group() 
enemy_bullets = pg.sprite.Group()  

game_over = False
font_game_over = pg.font.SysFont(None, 100)
dim_screen = pg.Surface(SCREEN_SIZE)
dim_screen.fill((0, 0, 0)) 
dim_screen.set_alpha(200)

def reset_game():
    global game_over  # Folosim global ca sa modificam variabila din afara
    game_over = False
    player.health = 5 
    bullets.empty()
    enemy_bullets.empty()
    player.rect.center = player.start_pos
    player.hitbox.center = player.start_pos
    if not camera_group.has(player):
        camera_group.add(player)
    spawn_enemies(editor.enemies, player, enemy_group, camera_group)

level_edit = False
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_F1:
                level_edit = not level_edit
                if not level_edit:
                    spawn_enemies(editor.enemies, player, enemy_group, camera_group)
                    enemy_bullets.empty()

            elif event.key == pg.K_F5:
                editor.save_level()
            
            elif event.key == pg.K_F6:
                editor.load_level()
                if not level_edit:
                    spawn_enemies(editor.enemies, player, enemy_group, camera_group)

            elif event.key == pg.K_r:
                if game_over:
                    reset_game()
            
            if level_edit:
                if event.key == pg.K_1:
                    editor.mode = "wall"
                    pg.display.set_caption("Editor Mode: walls")
                if event.key == pg.K_2:
                    editor.mode = "enemy"
                    pg.display.set_caption("Editor mode: Enemy")

    if pg.mouse.get_pressed()[0]: # apasat click stanga
        new_bullet = player.is_shooting()

        if new_bullet is not None:
            camera_group.add(new_bullet)
            bullets.add(new_bullet)

    wall_rects = [pg.Rect(pos[0], pos[1], editor.cell_size, editor.cell_size) for pos in editor.walls]

    screen.fill((0, 0, 0))
    if level_edit:
        editor.update(screen)
    else:
        enemy_group.update(wall_rects)

        for enemy in enemy_group:
            bullet = enemy.shoot_at_player()
            if bullet: # Daca functia a returnat un glont (nu e cooldown)
                enemy_bullets.add(bullet)
                camera_group.add(bullet)


        for bullet in bullets:
            bullet.update(wall_rects)
        for bullet in enemy_bullets:
            bullet.update(wall_rects)

        hits = pg.sprite.groupcollide(enemy_group, bullets, False, True)       
        for enemy in hits:
            enemy.health -= 1  
            if enemy.health <= 0:
                enemy.kill()  

        hits = pg.sprite.spritecollide(player, enemy_bullets, True)
        for bullet in hits:
            player.health -= 1
            
            if player.health <= 0:
                game_over = True

        pg.sprite.groupcollide(bullets, enemy_group, True, True)
        camera_group.update(wall_rects)

        offset_x = player.rect.centerx - (SCREEN_SIZE[0] // 2)
        offset_y = player.rect.centery - (SCREEN_SIZE[1] // 2)
        camera_offset = (offset_x, offset_y)

        editor.draw(screen, offset=camera_offset, show_enemies=False)
        camera_group.custom_draw(player)

        if not game_over:
            ui.draw(screen)
        
        elif game_over:
            player.kill()

            screen.blit(dim_screen, (0, 0))
            text_surf = font_game_over.render("GAME OVER", True, (255, 0, 0))
            text_rect = text_surf.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2))
            screen.blit(text_surf, text_rect)

            restart_text = editor.font.render("Press R to Restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2 + 60))
            screen.blit(restart_text, restart_rect)

    pg.display.flip() # update screen
    clock.tick(60) # 60fps

pg.quit()