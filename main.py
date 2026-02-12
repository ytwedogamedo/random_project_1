import pygame as pg
from settings import *


class Game:
    def __init__(self):
        # 1) Initialize pygame
        pg.init()

        # 2) Create window + clock
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Collision Tester")
        self.clock = pg.time.Clock()

        # 3) Game state
        self.running = True

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        pass  # game logic here

    def draw(self):
        self.screen.fill(WHITE)
        pg.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS

        pg.quit()


if __name__ == "__main__":
    Game().run()
