# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:50:07 2022
@author: richa
"""
from __future__ import annotations

import pygame
import random
import math
from dataclasses import dataclass
from typing import List
from typing import Tuple


class HexagonTile:
    def __init__(self, position, radius, color, flat_top):
        self.position = position
        self.radius = radius
        self.color = color
        self.flat_top = flat_top

        self.highlight_offset = 3
        self.highlight_tick = 0
        self.max_highlight_ticks = 15
        self.vertices = self.compute_vertices()

    def compute_vertices(self) -> List[Tuple[int, int]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        x, y = self.position
        half_radius = self.radius / 2
        if self.flat_top:
            return [
                (x, y),
                (x - half_radius, y + self.minimal_radius),
                (x, y + 2 * self.minimal_radius),
                (x + self.radius, y + 2 * self.minimal_radius),
                (x + 3 * half_radius, y + self.minimal_radius),
                (x + self.radius, y),
            ]
        else:
            return [
                (x, y),
                (x - self.minimal_radius, y + half_radius),
                (x - self.minimal_radius, y + 3 * half_radius),
                (x, y + 2 * self.radius),
                (x + self.minimal_radius, y + 3 * half_radius),
                (x + self.minimal_radius, y + half_radius),
            ]

    def compute_neighbours(self, hexagons: List[HexagonTile]) -> List[HexagonTile]:
        """Returns hexagons whose centres are two minimal radiuses away from self.centre"""
        return [hexagon for hexagon in hexagons if self.is_neighbour(hexagon)]

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < self.minimal_radius

    def is_neighbour(self, hexagon: HexagonTile) -> bool:
        """Returns True if hexagon centre is approximately 2 minimal radiuses away from own centre"""
        distance = math.dist(hexagon.centre, self.centre)
        return math.isclose(distance, 2 * self.minimal_radius, rel_tol=0.05)

    @property
    def centre(self) -> Tuple[int, int]:
        """Centre of the hexagon"""
        x, y = self.position
        if self.flat_top:
            return x, y + self.minimal_radius
        else:
            return x, y + self.radius

    @property
    def minimal_radius(self) -> float:
        """Horizontal length of the hexagon"""
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return self.radius * math.cos(math.radians(30))

    @property
    def highlight_color(self) -> Tuple[int, ...]:
        """Color of the hexagon tile when rendering highlight"""
        offset = self.highlight_offset * self.highlight_tick
        brighten = lambda x, y: x + y if x + y < 255 else 255
        return tuple(brighten(x, offset) for x in self.color)

    def render(self, gameDisplay) -> None:
        """Renders the hexagon on the gameDisplay"""
        pygame.draw.polygon(gameDisplay, self.highlight_color, self.vertices)

    def render_highlight(self, gameDisplay, border_color) -> None:
        """Draws a border around the hexagon with the specified color"""
        self.highlight_tick = self.max_highlight_ticks
        pygame.draw.polygon(gameDisplay, self.highlight_color, self.vertices)
        pygame.draw.lines(gameDisplay, border_color, True, self.vertices)

    def update(self):
        """Updates tile highlights"""
        if self.highlight_tick > 0:
            self.highlight_tick -= 1


def init_hexagons(position=(50, 50), num_x=20, num_y=20, flat_top=False) -> List[HexagonTile or FlatTopHexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    leftmost_hexagon = create_hexagon(position, flat_top=flat_top)
    radius, minimal_radius = leftmost_hexagon.radius, leftmost_hexagon.minimal_radius
    hexagons = [leftmost_hexagon]
    for line in range(num_y):
        if line != 0:
            # Alternates between the lower left and right vertices of the above hexagon.
            index = 2 if flat_top or line % 2 == 1 else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(leftmost_hexagon)

        # Places hexagons to the right of the leftmost hexagon
        for i in range(num_x-1):
            x, y = leftmost_hexagon.position
            if flat_top:
                if i % 2 == 1:
                    position = (x + (1+i)*3/2*radius, y)
                else:
                    position = (x + (1+i)*3/2*radius, y + minimal_radius)
            else:
                position = (x + (1+i)*2*minimal_radius, y)
            hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(hexagon)

    # Convert position and vertices into integers
    for hexagon in hexagons:
        hexagon.position = int(hexagon.position[0]), int(hexagon.position[1])
        for index in range(len(hexagon.vertices)):
            hexagon.vertices[index] = int(hexagon.vertices[index][0]), int(hexagon.vertices[index][1])

    return hexagons


def create_hexagon(position, radius=50, color=None, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    if color is None:
        color = get_random_color()
    return HexagonTile(position, radius, color, flat_top)


def get_random_color(min_color=120, max_color=255) -> Tuple[int, ...]:
    """Returns a random RGB color with each component between min_color and max_clor"""
    return tuple(random.choices(list(range(min_color, max_color)), k=3))


def draw(gameDisplay, hexagons):
    """Renders hexagons on the gameDisplay"""
    gameDisplay.fill((0, 0, 0))
    draw_hexagon(gameDisplay, hexagons)
    pygame.display.flip()


def draw_hexagon(gameDisplay, hexagons):
    """Template to draw hexagons"""
    # Draw hexagons
    for hexagon in hexagons:
        hexagon.render(gameDisplay)

    # Draw borders around the colliding hexagons and neighboring hexagons
    mouse_pos = pygame.mouse.get_pos()
    colliding_hexagons = [hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)]
    for hexagon in colliding_hexagons:
        for neighbour in hexagon.compute_neighbours(hexagons):
            neighbour.render_highlight(gameDisplay, border_color=(100, 100, 100))
        hexagon.render_highlight(gameDisplay, border_color=(0, 0, 0))


def main():
    """Main function"""
    pygame.init()
    gameDisplay = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    hexagons = init_hexagons(flat_top=False)
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        for hexagon in hexagons:
            hexagon.update()

        draw(gameDisplay, hexagons)
        clock.tick(50)

    pygame.display.quit()


if __name__ == "__main__":
    main()
