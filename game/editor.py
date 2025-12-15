import pygame as pg
from pygame.surface import Surface
import json

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


grass_img = "resources/tiles/grass.png"
grass_sprite = pg.image.load(grass_img)
grass_sprite = pg.transform.scale(grass_sprite, (40, 40))



class Editor:
    def __init__(self):
        self.cell_size = 40
        self.walls = {}
        self.grass = {}
        self.floors = {}
        self.bombs = {}
        self.trees = {}
        self.scroll = [0, 0]
        self.camera_speed = 10
        self.save_path = "level_data.json"
        self.enemies = set()
        self.mode = "walls"
        self.font = pg.font.SysFont(None, 30)
        
        # De inlocuit cu sprite ul
        enemy_surf = pg.image.load("resources/sprites/taliban.png").convert_alpha()
        tree_img = pg.image.load("resources/tiles/tree.png").convert_alpha()

        floors_img = {
            "floor1": pg.image.load("resources/tiles/floors/floor1.png").convert_alpha(),
            "floor2": pg.image.load("resources/tiles/floors/floor2.png").convert_alpha()
        }

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
            "enemy": enemy_surf,
            "grass": grass_sprite.convert_alpha(),
            "floor1": pg.transform.scale(floors_img["floor1"], (40, 40)),
            "floor2": pg.transform.scale(floors_img["floor2"], (40, 40)),
            "tree": pg.transform.scale(tree_img, (100, 100)),
            "bomb": pg.transform.scale(pg.image.load("resources/sprites/bomb.png").convert_alpha(), (self.cell_size, self.cell_size))
        }

    def update(self, screen):
        self.move_camera()
        self.make_grid(screen)
        self.edit()
        #self.draw_floors(screen, self.scroll)
        #self.draw_walls(screen, self.scroll)
        #self.draw_bombs(screen, self.scroll)
        self.draw_enemies(screen, self.scroll)
        self.draw_ui(screen)

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

        if self.mode=="wall":
            if has_click[0]:
                if pos_key not in self.walls:
                    self.walls[pos_key] = self.assets["center"]
                    self.update_neighbours(pos_key)

            elif has_click[2]:
                if pos_key in self.walls:
                    del self.walls[pos_key]
                    self.update_neighbours(pos_key)

        elif self.mode == "tree":
            if has_click[0]:
                if pos_key not in self.trees:
                    self.trees[pos_key] = self.assets["tree"]
            elif has_click[2]:
                if pos_key in self.trees:
                    del self.trees[pos_key]

        elif self.mode == "floor1":
            if has_click[0]:
                if pos_key not in self.grass:
                    self.floors[pos_key] = self.assets["floor1"]
            elif has_click[2]:
                if pos_key in self.floors:
                    del self.floors[pos_key]

        elif self.mode == "floor2":
            if has_click[0]:
                if pos_key not in self.grass:
                    self.floors[pos_key] = self.assets["floor2"]
            elif has_click[2]:
                if pos_key in self.floors:
                    del self.floors[pos_key]

        elif self.mode == "grass":
            if has_click[0]:
                if pos_key not in self.grass:
                    self.grass[pos_key] = self.assets["grass"]
            elif has_click[2]:
                if pos_key in self.grass:
                    del self.grass[pos_key]

        elif self.mode=="enemy":
            if has_click[0]:
                if pos_key not in self.enemies and pos_key not in self.walls:
                    self.enemies.add(pos_key)

            elif has_click[2]:
                if pos_key in self.enemies:
                    self.enemies.remove(pos_key)

        elif self.mode == "bomb":
            if has_click[0]:
                if pos_key not in self.bombs and pos_key not in self.walls and pos_key not in self.enemies:
                    self.bombs[pos_key] = "bomb"

            elif has_click[2]:
                if pos_key in self.bombs:
                    del self.bombs[pos_key]

    def draw_floors(self, screen, offset=(0, 0)):
        for pos, asset in self.grass.items():
            screen_pos_x = pos[0] - offset[0]
            screen_pos_y = pos[1] - offset[1]
            if -self.cell_size < screen_pos_x < screen.get_width() and -self.cell_size < screen_pos_y < screen.get_height():
                screen.blit(asset, (screen_pos_x, screen_pos_y))

        for pos, asset in self.floors.items():
            screen_pos_x = pos[0] - offset[0]
            screen_pos_y = pos[1] - offset[1]
            if -self.cell_size < screen_pos_x < screen.get_width() and -self.cell_size < screen_pos_y < screen.get_height():
                screen.blit(asset, (screen_pos_x, screen_pos_y))

        for pos, asset in self.trees.items():
            screen_pos_x = pos[0] - offset[0]
            screen_pos_y = pos[1] - offset[1]
            if -self.cell_size < screen_pos_x < screen.get_width() and -self.cell_size < screen_pos_y < screen.get_height():
                screen.blit(asset, (screen_pos_x, screen_pos_y))

        for pos in self.bombs:
            screen_pos_x = pos[0] - offset[0]
            screen_pos_y = pos[1] - offset[1]
            if -self.cell_size < screen_pos_x < screen.get_width() and -self.cell_size < screen_pos_y < screen.get_height():
                screen.blit(self.assets["bomb"], (screen_pos_x, screen_pos_y)) 

    def draw_walls(self, screen, offset=(0, 0)):
        for pos, asset in self.walls.items():
            screen_pos_x = pos[0] - offset[0]
            screen_pos_y = pos[1] - offset[1]
            if -self.cell_size < screen_pos_x < screen.get_width() and -self.cell_size < screen_pos_y < screen.get_height():
                screen.blit(asset, (screen_pos_x, screen_pos_y))

    def draw_enemies(self, screen, offset=(0, 0)):
        for pos in self.enemies:
            screen_pos_x = pos[0] - offset[0]
            screen_pos_y = pos[1] - offset[1]
            if -self.cell_size < screen_pos_x < screen.get_width() and -self.cell_size < screen_pos_y < screen.get_height():
                screen.blit(self.assets["enemy"], (screen_pos_x, screen_pos_y))

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

    def save_level(self):
        floors = []
        for pos, asset in self.floors.items():
            floor_type = "floor1"  # default

            if asset == self.assets["floor1"]:
                floor_type = "floor1"
            elif asset == self.assets["floor2"]:
                floor_type = "floor2"

            floors.append({
                "pos": list(pos),
                "type": floor_type
            })

        data = {
            "grass": list(self.grass.keys()),
            "floors": floors,
            "walls": list(self.walls.keys()),
            "enemies": list(self.enemies),
            "trees": list(self.trees),
            "bomb": list(self.bombs)
        }

        with open(self.save_path, "w") as f:
            json.dump(data, f)
        print(f"Map saved in {self.save_path}!")

    def load_level(self):
        try:
            with open(self.save_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("No saved data found.")
            return []

        self.grass = {}
        self.floors = {}
        self.walls = {}
        self.enemies = set()
        self.bombs = {}

        grass_list = data.get("grass", [])
        walls_list = data.get("walls", [])
        enemies_list = data.get("enemies", [])
        trees_list = data.get("trees", [])
        floors_list = data.get("floors", [])
        bombs_list = data.get("bomb", [])

        for pos in walls_list:
            self.walls[tuple(pos)] = self.assets["center"]

        for pos in trees_list:
            self.trees[tuple(pos)] = self.assets["tree"]

        for pos in grass_list:
            self.grass[tuple(pos)] = self.assets["grass"]

        for item in floors_list:

            if isinstance(item, list):

                self.floors[tuple(item)] = self.assets["floor1"]
            elif isinstance(item, dict):
                pos = tuple(item["pos"])
                floor_type = item["type"]

                if floor_type in self.assets:
                    self.floors[pos] = self.assets[floor_type]
                else:
                    self.floors[pos] = self.assets["floor1"]

        for pos in enemies_list:
            self.enemies.add(tuple(pos))

        for pos in bombs_list:
            self.bombs[tuple(pos)] = "bomb"

        for pos in list(self.walls.keys()):
            self.update_wall(pos)

        print("Map loaded succesfully.")
        return list(self.enemies)

    def draw_ui(self, screen):
        text_wall = self.font.render("1 - Wall", True, (255, 255, 0))
        text_enemy = self.font.render("2 - Enemy", True, (255, 255, 0))
        text_grass = self.font.render("3 - Grass", True, (255, 255, 0))
        text_floor1 = self.font.render("4 - Floor1", True, (255, 255, 0))
        text_floor2 = self.font.render("5 - Floor2", True, (255, 255, 0))
        text_tree = self.font.render("6 - Tree", True, (255, 255, 0))
        text_bomb = self.font.render("7 - Bomb", True, (255, 255, 0))
        
        screen.blit(text_wall, (30, 10))
        screen.blit(text_enemy, (30, 40))
        screen.blit(text_grass, (30, 70))
        screen.blit(text_floor1, (30, 100))
        screen.blit(text_floor2, (30, 130))
        screen.blit(text_tree, (30, 160))
        screen.blit(text_bomb, (30, 190))

        mode_text = self.font.render(f"Mode: {self.mode.upper()}", True, (255, 255, 255))
        screen.blit(mode_text, (30, 220))