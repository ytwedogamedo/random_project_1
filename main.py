import pygame as pg

from game_states import (
    GamePausedState,
    GamePlayingState,
    GameStartState,
)
from settings import *
from sprites import RectOne, RectTwo
from state_machine import StateMachine


# Main game class that owns the window, sprite groups, state machine, and HUD.
class Game:
    def __init__(self):
        pg.init()
        # setting up pygame screen using tuple value for width height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False
        self.is_colliding = False
        self.collision_message = "No collision"

        self.state_machine = StateMachine()
        self.game_states = [
            GameStartState(self),
            GamePlayingState(self),
            GamePausedState(self),
        ]
        self.state_machine.start_machine(self.game_states)

    def new(self):
        # these sprite groups mirror the framework style from the reference game
        self.all_sprites = pg.sprite.Group()
        self.rect_one_group = pg.sprite.Group()
        self.rect_two_group = pg.sprite.Group()

        # instanciates both test rectangles and places them at their start positions
        self.rect_one = RectOne(self, *RECT_ONE_START)
        self.rect_two = RectTwo(self, *RECT_TWO_START)
        self.update_collision_state()

    def reset(self):
        # puts both rectangles back to their starting coordinates for another test run
        self.rect_one.reset_position(*RECT_ONE_START)
        self.rect_two.reset_position(*RECT_TWO_START)
        self.update_collision_state()

    def update_collision_state(self):
        # checks overlap directly from the hitboxes and updates the HUD message
        self.is_colliding = self.rect_one.hit_rect.colliderect(self.rect_two.hit_rect)
        self.collision_message = "Collision detected" if self.is_colliding else "No collision"

    def run(self):
        while self.running:
            # divided by 1000 because pygame returns milliseconds and movement uses seconds
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        # all global keyboard and window events are handled here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_RETURN:
                    current_state = self.state_machine.current_state.get_state_name()
                    if current_state == "start":
                        self.state_machine.transition("playing")
                elif event.key == pg.K_p:
                    current_state = self.state_machine.current_state.get_state_name()
                    if current_state == "playing":
                        self.state_machine.transition("paused")
                    elif current_state == "paused":
                        self.state_machine.transition("playing")
                elif event.key == pg.K_r:
                    self.reset()

    def update(self):
        # lets the active game-flow state decide what should update this frame
        self.state_machine.update()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        current_state = self.state_machine.current_state.get_state_name()
        if current_state != "start":
            # draws the active collision test scene once gameplay has started
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, sprite.rect)

            self.draw_text(
                "Rect 1: WASD",
                24,
                HUD_TEXT_COLOR,
                WIDTH / 2,
                12,
            )
            self.draw_text(
                "Rect 2: Arrow Keys",
                24,
                HUD_TEXT_COLOR,
                WIDTH / 2,
                42,
            )
            self.draw_text(
                self.collision_message,
                30,
                COLLISION_COLOR if self.is_colliding else SAFE_COLOR,
                WIDTH / 2,
                HEIGHT - 70,
            )
            self.draw_text(
                "P: pause/resume   R: reset   ESC: quit",
                20,
                HUD_TEXT_COLOR,
                WIDTH / 2,
                HEIGHT - 36,
            )

        if current_state == "start":
            # start screen text matches the state-driven flow from the reference repo
            self.draw_text("Collision Tester", 58, HUD_TEXT_COLOR, WIDTH / 2, HEIGHT / 3)
            self.draw_text(
                "Move two rectangles and test overlap",
                28,
                HUD_TEXT_COLOR,
                WIDTH / 2,
                HEIGHT / 2 - 10,
            )
            self.draw_text(
                "Press ENTER to start",
                24,
                HUD_TEXT_COLOR,
                WIDTH / 2,
                HEIGHT / 2 + 40,
            )

        if current_state == "paused":
            # paused keeps the last frame visible while movement updates stop
            self.draw_text("PAUSED", 52, HUD_TEXT_COLOR, WIDTH / 2, HEIGHT / 2 - 24)

        pg.display.flip()

    def draw_text(self, text, size, color, x, y):  # function that draws text on the screen
        font_name = pg.font.match_font("arial")
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)  # actually renders the text
        text_rect = text_surface.get_rect()  # makes it a rect
        text_rect.midtop = (x, y)  # pos of text
        self.screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    game = Game()  # instanciates game class, so it can be used
    game.new()
    game.run()
    pg.quit()
