import argparse
import io

import pygame
import requests

from constants import bottom_spn_limit, top_spn_limit, window_width, window_height
from screens.abc import AbstractScreen


class ShowStaticMapsScreen(AbstractScreen):
    def __init__(self, screen: pygame.Surface, runner, args: argparse.Namespace):
        super().__init__(screen=screen, runner=runner)

        self.ll = args.ll
        self.spn = args.spn
        self.last_request_params = {"ll": self.ll, "spn": self.spn}
        self.last_request_image: io.BytesIO | None = None
        self.show_limit_text: bool = False
        self.font = pygame.font.Font("static/fonts/pixelFont.TTF", 40)

    @property
    def should_update(self):
        if self.last_request_image is None:
            return True

        return self.last_request_params["ll"] != self.ll or self.last_request_params["spn"] != self.spn

    def request_map_image(self) -> io.BytesIO:
        map_params = {
            'll': self.ll,
            'spn': self.spn,
            'l': 'map',
            'apikey': 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        }

        response = requests.get('https://static-maps.yandex.ru/v1', params=map_params)

        return io.BytesIO(response.content)

    def change_spn(self, d: float):
        a, b = map(float, self.spn.split(","))

        if not (bottom_spn_limit <= a + d <= top_spn_limit and bottom_spn_limit <= b + d <= top_spn_limit):
            self.show_limit_text = True
            return

        self.show_limit_text = False

        a += d
        b += d
        self.spn = ",".join(map(str, (a, b,)))

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYUP:
                continue

            if event.key == pygame.K_UP:  # pygame.K_PAGEUP
                self.change_spn(-0.005)

            if event.key == pygame.K_DOWN:  # pygame.K_PAGEDOWN
                self.change_spn(0.005)

    def update(self, events, **kwargs):
        self.handle_events(events)

        if self.should_update:
            self.last_request_image = self.request_map_image()

        self.last_request_image.close = lambda: None
        self.last_request_image.seek(0)

        pg_image = pygame.image.load(self.last_request_image)
        self.screen.blit(pg_image,
                         ((window_width - pg_image.get_width()) // 2, (window_height - pg_image.get_height()) // 2))

        rendered_text = self.font.render("You  reached  scale  limit!", True,
                                         "white" if self.show_limit_text else "black")
        self.screen.blit(rendered_text, ((window_width - rendered_text.get_width()) // 2, window_height - 50))
