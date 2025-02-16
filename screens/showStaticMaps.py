import argparse

import pygame
import requests
import os
import io
from PIL import Image

from screens.abc import AbstractScreen


class ShowStaticMapsScreen(AbstractScreen):
    def __init__(self, screen: pygame.Surface, runner, args: argparse.Namespace):
        super().__init__(screen=screen, runner=runner)

        self.ll = args.ll
        self.spn = args.spn
        self.last_request_params = {"ll": self.ll, "spn": self.spn}
        self.last_request_image: io.BytesIO | None = None

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

    def update(self, events, **kwargs):
        if self.should_update:
            self.last_request_image = self.request_map_image()

        self.last_request_image.close = lambda: None
        self.last_request_image.seek(0)

        pg_image = pygame.image.load(self.last_request_image)
        self.screen.blit(pg_image, ((1100 - pg_image.get_width()) // 2, (700 - pg_image.get_height()) // 2))
