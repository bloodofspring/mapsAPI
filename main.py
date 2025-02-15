import pygame
import argparse
import requests
import os
import io
from PIL import Image


def setup_screen():
    pygame.init()
    screen = pygame.display.set_mode((1100, 700))
    pygame.display.set_caption("Maps API App")
    return screen


def request_map_image(ll, spn):
    map_params = {
        'll': ll,
        'spn': spn,
        'l': 'map',
        'apikey': 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
    }
    map_request = f'https://static-maps.yandex.ru/v1'
    response = requests.get(map_request, params=map_params)
    print(response.request.url)

    return io.BytesIO(response.content)

def main():
    screen = setup_screen()
    parser = argparse.ArgumentParser()
    parser.add_argument('--ll', type=str)
    parser.add_argument('--spn', type=str)
    args = parser.parse_args()
    map_image = request_map_image(ll=args.ll, spn=args.spn)
    screen.blit(pygame.image.load(map_image), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()


if __name__ == '__main__':
    main()