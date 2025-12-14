import pygame as pg
from shapely import geometry
from game.shadows.map import Map
from game.shadows.cast import ShadowCaster
from game.shadows.obstacle import Obstacle


class ShadowManager:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.map = Map()
        self.caster = ShadowCaster(self.map)

    def update(self, all_walls_pos, cell_size, camera_offset, player_screen_pos):
        """
        Unire pereti, optimizare si randare
        """
        self.map.obstacles.clear()

        merged_walls = self._merge_walls(all_walls_pos, cell_size)

        offset_x, offset_y = camera_offset
        screen_w, screen_h = self.screen_size

        for rect in merged_walls:
            screen_pos_x = rect.x - offset_x
            screen_pos_y = rect.y - offset_y

            # verificam daca e pe ecran + padding
            padding = 100
            if -rect.width - padding < screen_pos_x < screen_w + padding and \
                    -rect.height - padding < screen_pos_y < screen_h + padding:
                # definim colturile
                corners = [
                    (screen_pos_x, screen_pos_y),
                    (screen_pos_x + rect.width, screen_pos_y),
                    (screen_pos_x + rect.width, screen_pos_y + rect.height),
                    (screen_pos_x, screen_pos_y + rect.height)
                ]

                # cream poligonul
                poly = geometry.Polygon(corners)

                # adaugam in harta
                self.map.obstacles.append(Obstacle(corners, poly))

        # generam umbrele
        self.caster.generate_shadows(player_screen_pos)
        self.caster.render_shadows()

    def draw(self, surface):
        self.caster.draw_shadows(surface)

    def _merge_walls(self, walls_positions, cell_size):
        """Functie interna pentru optimizarea peretilor"""
        if not walls_positions: return []

        rects = [pg.Rect(pos[0], pos[1], cell_size, cell_size) for pos in walls_positions]
        rects.sort(key=lambda r: (r.y, r.x))

        merged = []
        if not rects: return merged

        curr = rects[0]
        for next_rect in rects[1:]:
            if curr.y == next_rect.y and curr.right == next_rect.left:
                curr.width += next_rect.width
            else:
                merged.append(curr)
                curr = next_rect
        merged.append(curr)

        return merged