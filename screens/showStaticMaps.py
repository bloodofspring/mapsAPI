import argparse
import io

import pygame
import requests

from constants import bottom_spn_limit, top_spn_limit, window_width, window_height, latitude_range, longitude_range
from screens.abc import AbstractScreen


class ShowStaticMapsScreen(AbstractScreen):
    def __init__(self, screen: pygame.Surface, runner, args: argparse.Namespace):
        super().__init__(screen=screen, runner=runner)

        self.theme_update_flag: bool = False
        self.theme = 'light'
        self.ll = args.ll
        self.check_ll()
        self.spn = args.spn
        self.check_spn()

        self.last_request_params = {"ll": self.ll, "spn": self.spn}
        self.last_request_image: io.BytesIO | None = None
        self.show_scale_limit_text: bool = False
        self.font = pygame.font.Font("static/fonts/pixelFont.TTF", 40)

    def check_spn(self):
        a, b = map(float, self.spn.split(","))
        if a < bottom_spn_limit:
            a = bottom_spn_limit
            self.show_scale_limit_text = True
        elif a > top_spn_limit:
            a = top_spn_limit
            self.show_scale_limit_text = True

        if b < bottom_spn_limit:
            b = bottom_spn_limit
            self.show_scale_limit_text = True
        elif b > top_spn_limit:
            b = top_spn_limit
            self.show_scale_limit_text = True

        self.spn = ",".join(map(str, (a, b,)))

    def check_ll(self):
        ln, ll = map(float, self.ll.split(","))

        if ln < longitude_range[0]:
            ln = longitude_range[0]
        elif ln > longitude_range[1]:
            ln = longitude_range[1]

        if ll < latitude_range[0]:
            ll = latitude_range[0]
        elif ll > latitude_range[1]:
            ll = latitude_range[1]

        self.ll = ",".join(map(str, (ln, ll,)))

    @property
    def should_update(self):
        if self.last_request_image is None:
            return True

        return self.last_request_params["ll"] != self.ll or self.last_request_params["spn"] != self.spn

    def request_map_image(self) -> io.BytesIO:
        map_params = {
            'll': self.ll,
            'theme': self.theme,
            'spn': self.spn,
            'l': 'map',
            'apikey': 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        }

        response = requests.get('https://static-maps.yandex.ru/v1', params=map_params)

        return io.BytesIO(response.content)

    def change_spn(self, d: float):
        a, b = map(float, self.spn.split(","))
        self.show_scale_limit_text = False

        a += d
        b += d
        self.spn = ",".join(map(str, (a, b,)))
        self.check_spn()

    @property
    def scale(self):
        return float(self.spn.split(",")[0])

    def change_position(self, *, ll_d: float = 0.0, ln_d: float = 0.0):
        ln, ll = map(float, self.ll.split(","))

        ll += ll_d
        ln += ln_d

        self.ll = ",".join(map(str, (ln, ll,)))
        self.check_ll()

    def change_theme(self):
        self.theme = ['dark', 'light'][['dark', 'light'].index(self.theme) - 1]
        self.theme_update_flag = True

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYUP:
                continue

            if event.key == pygame.K_PAGEUP:  # pygame.K_q:
                self.change_spn(-0.005)
                continue

            if event.key == pygame.K_PAGEDOWN:  # pygame.K_w:
                self.change_spn(0.005)
                continue

            if event.key == pygame.K_t:
                self.change_theme()

            if event.key == pygame.K_UP:
                self.change_position(ll_d=self.scale)

            if event.key == pygame.K_RIGHT:
                self.change_position(ln_d=self.scale)

            if event.key == pygame.K_DOWN:
                self.change_position(ll_d=-self.scale)

            if event.key == pygame.K_LEFT:
                self.change_position(ln_d=-self.scale)

    def update(self, events, **kwargs):
        self.handle_events(events)

        if self.should_update or self.theme_update_flag:
            self.last_request_image = self.request_map_image()
            self.theme_update_flag = False

        self.last_request_image.close = lambda: None
        self.last_request_image.seek(0)

        pg_image = pygame.image.load(self.last_request_image)
        self.screen.blit(pg_image, ((window_width - pg_image.get_width()) // 2, (window_height - pg_image.get_height()) // 2))

        rendered_text = self.font.render("You  reached  scale  limit!", True, "white" if self.show_scale_limit_text else "black")
        self.screen.blit(rendered_text, ((window_width - rendered_text.get_width()) // 2, window_height - 50))
