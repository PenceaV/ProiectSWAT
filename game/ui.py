import pygame as pg

class UI:
    def __init__(self, player):
        self.player = player
        self.font = pg.font.SysFont("Arial", 30, bold=True)
        self.heart_size = 30
        self.spacing = 10 
        self.heart_img = pg.image.load("resources/sprites/heart.png").convert_alpha()
        self.heart_img = pg.transform.scale(self.heart_img, (30, 30))
        self.ammo_color = (255, 255, 255) 
        self.reload_color = (255, 0, 0)  

    def draw(self, screen):
        start_x = 1280 - 40
        start_y = 20

        for i in range(self.player.health):
            offset = i * (self.heart_size + self.spacing)
            x = start_x - offset  
            y = start_y
            screen.blit(self.heart_img, (x, y))

        if self.player.is_reloading:
            text_str = "RELOADING..."
            color = self.reload_color
        else:
            text_str = f"{self.player.current_mag_ammo} / {self.player.reserve_ammo}"
            color = self.ammo_color

            # Randare text
        ammo_surf = self.font.render(text_str, True, color)

        screen_w = screen.get_width()
        screen_h = screen.get_height()

        x_pos = screen_w - ammo_surf.get_width() - 20  # 20 pixeli padding dreapta
        y_pos = screen_h - ammo_surf.get_height() - 20  # 20 pixeli padding jos

        screen.blit(ammo_surf, (x_pos, y_pos))