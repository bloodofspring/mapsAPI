import argparse
import sys

import pygame

from constants import window_width, window_height, fps
from screens import AbstractScreen, ShowStaticMapsScreen
from util import load_image


def setup_window():
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption("Maps API App")
    pygame.display.set_icon(load_image("app_icon.png"))

    return window


def setup_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--ll', type=str)
    parser.add_argument('--spn', type=str)

    return parser


class GameRunner:
    def __init__(self, game_window, start_with_screen: type[AbstractScreen], **screen_init_additional):
        self.game_window = game_window
        self.current_screen = start_with_screen(screen=game_window, runner=self, **screen_init_additional)

        self.is_running: bool = True
        self.frame: int = 0
        self.clock = pygame.time.Clock()

    def handle_events(self, events):
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.is_running = False

    def change_screen(self, new: AbstractScreen):
        self.current_screen = new

    def start(self):
        while self.is_running:
            self.frame = (self.frame + 1) % fps

            events = pygame.event.get()
            self.handle_events(events=events)

            self.current_screen.update(events)

            self.clock.tick(fps)
            pygame.display.flip()

        self.quit()

    @staticmethod
    def quit():
        pygame.quit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ll', type=str)
    parser.add_argument('--spn', type=str)
    args = parser.parse_args()

    runner = GameRunner(game_window=setup_window(), start_with_screen=ShowStaticMapsScreen, args=args)
    sys.exit(runner.start())


if __name__ == "__main__":
    main()
