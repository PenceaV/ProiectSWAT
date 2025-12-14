import random

import pygame as pg
from game.player import Player
from game.editor import Editor
from game.camera import CameraGroup
from game.enemy import Enemy, spawn_enemies
from game.ui import UI
from game.shadows.manager import ShadowManager

pg.init()
pg.mixer.init()

SCREEN_SIZE = (1280, 720)
# TITLE = ... DE SCRIS

intro_screen = pg.Surface(SCREEN_SIZE)
intro_screen.fill((0, 0, 0))
intro_start_time = pg.time.get_ticks()
black_duration = 8000
fade_duration = 3000

screen = pg.display.set_mode(SCREEN_SIZE, pg.RESIZABLE)
clock = pg.time.Clock()
player = Player()
editor = Editor()
ui = UI(player)

# manager de umbre
shadow_manager = ShadowManager(SCREEN_SIZE)

camera_group = CameraGroup()
camera_group.add(player)
bullets = pg.sprite.Group()
enemy_group = pg.sprite.Group()
enemy_bullets = pg.sprite.Group()

# sunete
grunts = [
    pg.mixer.Sound("resources/sound/grunt1.mp3"),
    pg.mixer.Sound("resources/sound/grunt2.mp3"),
    pg.mixer.Sound("resources/sound/grunt3.mp3")
]

death = pg.mixer.Sound("resources/sound/death.mp3")
helicopter = pg.mixer.Sound("resources/sound/helicopter.mp3")

game_over = False
font_game_over = pg.font.SysFont(None, 100)
dim_screen = pg.Surface(SCREEN_SIZE)
dim_screen.fill((0, 0, 0))
dim_screen.set_alpha(200)


def reset_game():
    global game_over
    game_over = False
    player.health = 5
    bullets.empty()
    enemy_bullets.empty()
    player.rect.center = player.start_pos
    player.hitbox.center = player.start_pos
    if not camera_group.has(player):
        camera_group.add(player)
    spawn_enemies(editor.enemies, player, enemy_group, camera_group)
    # intro_start_time = pg.time.get_ticks() -> ! daca vrem sa dam restart la joc si sa se repete animatia


level_edit = False
run = True
helicopter_sound = False

while run:
    current_time = pg.time.get_ticks()
    time_since_start = current_time - intro_start_time

    is_in_intro_blackout = time_since_start < black_duration

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F1:
                level_edit = not level_edit
                if not level_edit:
                    pg.mixer.stop()
                    spawn_enemies(editor.enemies, player, enemy_group, camera_group)
                    enemy_bullets.empty()
            elif event.key == pg.K_ESCAPE:
                run = False
            elif event.key == pg.K_F5:
                editor.save_level()
            elif event.key == pg.K_F6:
                editor.load_level()
                if not level_edit:
                    spawn_enemies(editor.enemies, player, enemy_group, camera_group)
            elif event.key == pg.K_f:
                if game_over:
                    reset_game()
            elif event.key == pg.K_r:
                player.start_reload()

            if level_edit:
                if event.key == pg.K_1:
                    editor.mode = "wall"
                    pg.display.set_caption("Editor Mode: walls")
                if event.key == pg.K_2:
                    editor.mode = "enemy"
                    pg.display.set_caption("Editor mode: enemy")
                if event.key == pg.K_3:
                    editor.mode = "grass"
                    pg.display.set_caption("Editor Mode: grass")
                if event.key == pg.K_4:
                    editor.mode = "floor1"
                    pg.display.set_caption("Editor Mode: floor1")
                if event.key == pg.K_5:
                    editor.mode = "floor2"
                    pg.display.set_caption("Editor Mode: floor2")
                if event.key == pg.K_6:
                    editor.mode = "tree"
                    pg.display.set_caption("Edito Mode: tree")

    if not is_in_intro_blackout and pg.mouse.get_pressed()[0]:
        new_bullet = player.is_shooting()
        if new_bullet is not None:
            camera_group.add(new_bullet)
            bullets.add(new_bullet)

    wall_rects = [pg.Rect(pos[0], pos[1], editor.cell_size, editor.cell_size) for pos in editor.walls]
    tree_rects = []
    # cat de inalt sa fie hitboxul trunchiului
    trunk_height = editor.cell_size // 2
    trunk_offset_y = editor.cell_size - trunk_height

    for pos in editor.trees:

        trunk_hitbox = pg.Rect(
            pos[0],  # X
            pos[1] + trunk_offset_y,
            editor.cell_size,  # Width
            trunk_height  # Height
        )
        tree_rects.append(trunk_hitbox)

    screen.fill((50, 50, 50))

    if level_edit:
        editor.update(screen)
    else:
        if not is_in_intro_blackout:
            player.update(wall_rects, tree_rects)

            offset_x = player.rect.centerx - (SCREEN_SIZE[0] // 2)
            offset_y = player.rect.centery - (SCREEN_SIZE[1] // 2)
            camera_offset = (offset_x, offset_y)
            player_screen_center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

            shadow_manager.update(
                all_walls_pos=editor.walls.keys(),
                cell_size=editor.cell_size,
                camera_offset=camera_offset,
                player_screen_pos=player_screen_center
            )

            enemy_group.update(wall_rects, shadow_manager.caster.shaded_areas, camera_offset)

            for enemy in enemy_group:
                bullet = enemy.shoot_at_player(player.health)
                if bullet:
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
                grunts[random.randrange(3)].play()
                if player.health <= 0:
                    death.play()
                    game_over = True

            pg.sprite.groupcollide(bullets, enemy_group, True, True)

        offset_x = player.rect.centerx - (SCREEN_SIZE[0] // 2)
        offset_y = player.rect.centery - (SCREEN_SIZE[1] // 2)
        camera_offset = (offset_x, offset_y)

        editor.draw_floors(screen, offset=camera_offset)
        shadow_manager.draw(screen)
        editor.draw_walls(screen, offset=camera_offset)
        camera_group.custom_draw(player)

        if not game_over:
            ui.draw(screen)
        elif game_over:
            player.kill()
            screen.blit(dim_screen, (0, 0))
            text_surf = font_game_over.render("GAME OVER", True, (255, 0, 0))
            text_rect = text_surf.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
            screen.blit(text_surf, text_rect)
            restart_text = editor.font.render("Press F to Restart", True,
                                              (255, 255, 255))  # Am corectat tasta R->F conform codului
            restart_rect = restart_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 60))
            screen.blit(restart_text, restart_rect)

    if time_since_start < black_duration + fade_duration:
        if time_since_start < black_duration:
            intro_screen.set_alpha(255)
            screen.blit(intro_screen, (0, 0))
            # de dat play la helicopter
            if not helicopter_sound:
                helicopter.set_volume(0.65)
                helicopter.play()
                helicopter_sound = True

        # fade out
        else:
            fade_progress = (time_since_start - black_duration) / fade_duration

            current_alpha = 255 - (255 * fade_progress)

            if current_alpha < 0: current_alpha = 0

            intro_screen.set_alpha(int(current_alpha))
            screen.blit(intro_screen, (0, 0))

    pg.display.flip()
    clock.tick(60)

pg.quit()