import pygame as pg
from pygame.surface import Surface

walls_path = "resources/tiles/walls"
walls_img = {
    "all": f"{walls_path}/all.png",
    "center": f"{walls_path}/left-right-top-bottom.png",
    "top-left": f"{walls_path}/top-left.png",
    "top-right": f"{walls_path}/top-right.png",
    "top-center": f"{walls_path}/top-center.png",
    "left": f"{walls_path}/left.png",
    "right": f"{walls_path}/right.png",
    "left-right": f"{walls_path}/left-right.png",
    "bottom-left": f"{walls_path}/bottom-left.png",
    "bottom-right": f"{walls_path}/bottom-right.png",
    "bottom-center": f"{walls_path}/bottom-center.png",
    "top-right-bottom": f"{walls_path}/top-right-bottom.png",
    "left-bottom-right": f"{walls_path}/left-bottom-right.png",
    "top-left-bottom": f"{walls_path}/top-left-bottom.png",
    "top-left-right": f"{walls_path}/top-left-right.png",
    "top-bottom": f"{walls_path}/top-bottom.png"
}

class Editor:
    def __init__(self):
        self.cell_size = 40
        self.walls = {}
        self.scroll = [0, 0]
        self.camera_speed = 10

        self.assets = {
            "all": pg.image.load(walls_img["all"]).convert_alpha(),
            "center": pg.image.load(walls_img["center"]).convert_alpha(),
            "top-left": pg.image.load(walls_img["top-left"]).convert_alpha(),
            "top-right": pg.image.load(walls_img["top-right"]).convert_alpha(),
            "top-center": pg.image.load(walls_img["top-center"]).convert_alpha(),
            "left": pg.image.load(walls_img["left"]).convert_alpha(),
            "right": pg.image.load(walls_img["right"]).convert_alpha(),
            "left-right": pg.image.load(walls_img["left-right"]).convert_alpha(),
            "bottom-left": pg.image.load(walls_img["bottom-left"]).convert_alpha(),
            "bottom-right": pg.image.load(walls_img["bottom-right"]).convert_alpha(),
            "bottom-center": pg.image.load(walls_img["bottom-center"]).convert_alpha(),
            "top-right-bottom": pg.image.load(walls_img["top-right-bottom"]).convert_alpha(),
            "left-bottom-right": pg.image.load(walls_img["left-bottom-right"]).convert_alpha(),
            "top-left-bottom": pg.image.load(walls_img["top-left-bottom"]).convert_alpha(),
            "top-left-right": pg.image.load(walls_img["top-left-right"]).convert_alpha(),
            "top-bottom": pg.image.load(walls_img["top-bottom"]).convert_alpha(),
        }

    def update(self, screen):
        self.move_camera()
        self.make_grid(screen)
        self.edit()
        self.draw(screen, self.scroll)

    def move_camera(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.scroll[1] -= self.camera_speed
        if keys[pg.K_s]:
            self.scroll[1] += self.camera_speed
        if keys[pg.K_a]:
            self.scroll[0] -= self.camera_speed
        if keys[pg.K_d]:
            self.scroll[0] += self.camera_speed

    def auto_tile(self, pos):
        x, y = pos
        size = self.cell_size

        top = (x, y - size) in self.walls
        bottom = (x, y + size) in self.walls
        right = (x + size, y) in self.walls
        left = (x - size, y) in self.walls

        if right and left and top and bottom:
            return self.assets["all"]
        elif top and right and bottom:
            return self.assets["left"]
        elif top and left and bottom:
            return self.assets["right"]
        elif right and left and bottom:
            return self.assets["top-center"]
        elif right and left and top:
            return self.assets["bottom-center"]
        elif right and left:
            return self.assets["top-bottom"]
        elif right and bottom:
            return self.assets["top-left"]
        elif left and bottom:
            return self.assets["top-right"]
        elif top and bottom:
            return self.assets["left-right"]
        elif top and right:
            return self.assets["bottom-left"]
        elif top and left:
            return self.assets["bottom-right"]
        elif left:
            return self.assets["top-right-bottom"]
        elif right:
            return self.assets["top-left-bottom"]
        elif top:
            return self.assets["left-bottom-right"]
        elif bottom:
            return self.assets["top-left-right"]
        else:
            return self.assets["center"]

    def update_wall(self, pos):
        if pos in self.walls:
            new_img = self.auto_tile(pos)
            self.walls[pos] = new_img

    def update_neighbours(self, pos):
        x, y = pos
        size = self.cell_size

        self.update_wall(pos)
        neighbours = [
            (x, y - size),
            (x, y + size),
            (x - size, y),
            (x + size, y)
        ]
        for n_pos in neighbours:
            self.update_wall(n_pos)

    def edit(self):
        mousex, mousey = pg.mouse.get_pos()
        has_click = pg.mouse.get_pressed()

        world_mouse_x = mousex + self.scroll[0]
        world_mouse_y = mousey + self.scroll[1]

        col_index = world_mouse_x // self.cell_size
        row_index = world_mouse_y // self.cell_size
        x_pos = col_index * self.cell_size
        y_pos = row_index * self.cell_size

        pos_key = (x_pos, y_pos)
        if has_click[0]:
            if pos_key not in self.walls:
                self.walls[pos_key] = self.assets["center"]
                self.update_neighbours(pos_key)

        elif has_click[2]:
            if pos_key in self.walls:
                del self.walls[pos_key]
                self.update_neighbours(pos_key)

    def draw(self, screen, offset=(0, 0)):
        for pos, asset in self.walls.items():
            screen_pos_x = pos[0] - offset[0]
            screen_pos_y = pos[1] - offset[1]

            if -self.cell_size < screen_pos_x < screen.get_width() and \
               -self.cell_size < screen_pos_y < screen.get_height():
                screen.blit(asset, (screen_pos_x, screen_pos_y))

    def make_grid(self, screen):
        height = screen.get_height()
        width = screen.get_width()

        grid_surface = Surface((width, height), pg.SRCALPHA)
        opacity_level = 128
        color_line = (255, 255, 255, opacity_level)

        start_x = -(self.scroll[0] % self.cell_size)
        start_y = -(self.scroll[1] % self.cell_size)

        for y in range(start_y, height, self.cell_size):
            pg.draw.line(grid_surface, color_line, (0, y), (width, y), 1)
        for x in range(start_x, width, self.cell_size):
            pg.draw.line(grid_surface, color_line, (x, 0), (x, height), 1)

        screen.blit(grid_surface, (0, 0))