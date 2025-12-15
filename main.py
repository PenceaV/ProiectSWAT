import random

import pygame as pg
from game.player import Player
from game.editor import Editor
from game.camera import CameraGroup
from game.bomb import Bomb
from game.enemy import Enemy, spawn_enemies
from game.ui import UI
from game.shadows.manager import ShadowManager

pg.init()
pg.mixer.init()

SCREEN_SIZE = (1280, 720)
# TITLE = "SWAT Raid"

intro_screen = pg.Surface(SCREEN_SIZE)
intro_screen.fill((0, 0, 0))
intro_start_time = pg.time.get_ticks()
black_duration = 8000
fade_duration = 3000
playing_intro = False

screen = pg.display.set_mode(SCREEN_SIZE, pg.RESIZABLE)
clock = pg.time.Clock()
game_duration=300000
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
bomb_group = pg.sprite.Group()
# sunete
grunts = [
    pg.mixer.Sound("resources/sound/grunt1.mp3"),
    pg.mixer.Sound("resources/sound/grunt2.mp3"),
    pg.mixer.Sound("resources/sound/grunt3.mp3")
]

death = pg.mixer.Sound("resources/sound/death.mp3")
helicopter = pg.mixer.Sound("resources/sound/helicopter.mp3")
victory_sound = pg.mixer.Sound("resources/sound/victory.mp3")

timer = pg.mixer.Sound("resources/sound/timer.mp3") 
explosion = pg.mixer.Sound("resources/sound/explosion.mp3")

start_menu = True  
font_title = pg.font.SysFont(None, 120)
font_instructions = pg.font.SysFont(None, 60)

victory = False
game_over = False
font_game_over = pg.font.SysFont(None, 100)
font_timer = pg.font.SysFont(None, 50)
dim_screen = pg.Surface(SCREEN_SIZE)
dim_screen.fill((0, 0, 0))
dim_screen.set_alpha(200)

game_start_time = 0
time_left_ms = game_duration

def reset_game(play_intro = False):
    global game_over, intro_start_time, playing_intro, helicopter_sound
    global game_start_time

    game_over = False
    victory = False
    timer.stop()
    victory_sound.stop()
    explosion.stop()
    time_left_ms = game_duration
    player.health = 5
    bullets.empty()
    enemy_bullets.empty()
    player.rect.center = player.start_pos
    player.hitbox.center = player.start_pos
    if not camera_group.has(player):
        camera_group.add(player)
    spawn_enemies(editor.enemies, player, enemy_group, camera_group)
    bomb_group.empty()
    if hasattr(editor, 'bombs'):
        for pos in editor.bombs:
            bomb = Bomb(pos, editor.cell_size)
            bomb_group.add(bomb)
    player.max_mag_ammo = 12
    player.current_mag_ammo = 12
    player.reserve_ammo = 48
    if play_intro:
        intro_start_time = pg.time.get_ticks()
        playing_intro = True
        helicopter_sound = False
        game_start_time = 0
    else:
        playing_intro = False
        helicopter.stop()
        game_start_time = pg.time.get_ticks()
        timer.play()


level_edit = False
run = True
helicopter_sound = False

while run:
    current_time = pg.time.get_ticks()
    time_since_start = 0
    
    if not start_menu:
        time_since_start = current_time - intro_start_time
        is_in_intro_blackout = time_since_start < black_duration
    else:
        is_in_intro_blackout = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if start_menu:
                if event.key == pg.K_RETURN:
                    start_menu = False 
                    editor.load_level()
                    reset_game(play_intro=True)
                    if not level_edit:
                        enemy_group.empty() 
                        enemy_bullets.empty()
                        spawn_enemies(editor.enemies, player, enemy_group, camera_group)
            if event.key == pg.K_F6:
                    editor.load_level()
                    if not level_edit:
                        enemy_group.empty() 
                        enemy_bullets.empty()
                        spawn_enemies(editor.enemies, player, enemy_group, camera_group)
            if not start_menu:
                if event.key == pg.K_F1:
                    level_edit = not level_edit
                    if not level_edit:
                        pg.mixer.stop()
                        timer.play()
                        game_start_time = pg.time.get_ticks() - (game_duration - time_left_ms)
                        spawn_enemies(editor.enemies, player, enemy_group, camera_group)
                        enemy_bullets.empty()
                        bomb_group.empty()
                        if hasattr(editor, 'bombs'):
                            for pos in editor.bombs:
                                b = Bomb(pos, editor.cell_size)
                                bomb_group.add(b)
                    else:
                        timer.stop()
                        offset_x = player.rect.centerx - (SCREEN_SIZE[0] // 2)
                        offset_y = player.rect.centery - (SCREEN_SIZE[1] // 2)
                        editor.scroll = [offset_x, offset_y]

                elif event.key == pg.K_ESCAPE:
                    run = False
                elif event.key == pg.K_F5:
                    editor.save_level()
                    if not level_edit:
                        spawn_enemies(editor.enemies, player, enemy_group, camera_group)
                elif event.key == pg.K_e:
                    if not game_over and not level_edit:
                        hits = pg.sprite.spritecollide(player, bomb_group, True)
                        if hits:
                            game_over = True
                            victory = True
                            timer.stop()
                            victory_sound.set_volume(0.65)
                            victory_sound.play()
                elif event.key == pg.K_f:
                    if game_over:
                        reset_game(play_intro=False)
                elif event.key == pg.K_m:
                        start_menu = True
                        pg.mixer.stop()
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
                    pg.display.set_caption("Editor Mode: tree")
                if event.key == pg.K_7:
                    editor.mode = "bomb"
                    pg.display.set_caption("Editor Mode: bomb")

    if not is_in_intro_blackout and not level_edit and not start_menu and not game_over and pg.mouse.get_pressed()[0]:
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
            pos[0],  
            pos[1] + trunk_offset_y,
            editor.cell_size,  
            trunk_height  
        )
        tree_rects.append(trunk_hitbox)

    screen.fill((0, 0, 0))

    if start_menu:
        title_surf = font_title.render("SWAT Raid ", True, (0, 100, 255))
        title_rect = title_surf.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2 - 50))
        screen.blit(title_surf, title_rect)

        instr_surf = font_instructions.render("Press ENTER to start", True, (0, 100, 255))
        instr_rect = instr_surf.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2 + 50))
        screen.blit(instr_surf, instr_rect)
    
    else:
        screen.fill((50, 50, 50))

        if not level_edit:
            if not is_in_intro_blackout and not start_menu and not game_over:
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
                    bullet = enemy.shoot_at_player(player.health, wall_rects)
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
                        grunts[random.randrange(3)].play()

                hits = pg.sprite.spritecollide(player, enemy_bullets, True)
                for bullet in hits:
                    player.health -= 1
                    grunts[random.randrange(3)].play()
                    if player.health <= 0:
                        death.play()
                        game_over = True
                        victory = False
                        timer.stop()

                pg.sprite.groupcollide(bullets, enemy_group, True, True)

        if level_edit:
            camera_offset = tuple(editor.scroll) 
        else:
            offset_x = player.rect.centerx - (SCREEN_SIZE[0] // 2)
            offset_y = player.rect.centery - (SCREEN_SIZE[1] // 2)
            camera_offset = (offset_x, offset_y) 

        editor.draw_floors(screen, offset=camera_offset)
        
        if not level_edit:
            shadow_manager.draw(screen)

        editor.draw_walls(screen, offset=camera_offset)
        camera_group.custom_draw(player)

        if level_edit:
            editor.update(screen)

        if not game_over:
            ui.draw(screen)

            if game_start_time > 0:
                time_elapsed = current_time - game_start_time
                time_left_ms = game_duration - time_elapsed
                
                if time_left_ms <= 0:
                    game_over = True
                    victory = False
                    timer.stop()
                    explosion.play()

                if time_left_ms < 0: time_left_ms = 0
                minutes = (time_left_ms // 1000) // 60
                seconds = (time_left_ms // 1000) % 60
                
                timer_text = font_timer.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))
                screen.blit(timer_text, (0, 30))

        elif game_over and not victory:
            player.kill()
            screen.blit(dim_screen, (0, 0))
            if time_left_ms <= 0:
                screen.fill((0, 0, 0)) 
                text_surf = font_game_over.render("TIME'S UP", True, (255, 0, 0))
                text_rect = text_surf.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
                screen.blit(text_surf, text_rect)
                restart_text = editor.font.render("Press F to Restart", True,(255, 255, 255))  
                restart_rect = restart_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 60))
                screen.blit(restart_text, restart_rect)
            else:    
                text_surf = font_game_over.render("YOU DIED", True, (255, 0, 0))
                text_rect = text_surf.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
                screen.blit(text_surf, text_rect)
                restart_text = editor.font.render("Press F to Restart", True,(255, 255, 255))  
                restart_rect = restart_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 60))
                screen.blit(restart_text, restart_rect)

        elif game_over and victory:
            screen.blit(dim_screen, (0, 0))
            text_surf = font_game_over.render("YOU WON", True, (0, 255, 0))
            text_rect = text_surf.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
            screen.blit(text_surf, text_rect)
            restart_text = editor.font.render("Press M to return to main menu", True,(255, 255, 255))  
            restart_rect = restart_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 60))
            screen.blit(restart_text, restart_rect)

        if playing_intro and not start_menu:
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
        
                playing_intro = False
                helicopter.stop()
                game_start_time = pg.time.get_ticks()
                timer.play()
        
    pg.display.flip()
    clock.tick(60)

pg.quit()