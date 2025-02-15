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
        'spn': spn
    }
    server_address = 'https://static-maps.yandex.ru/v1?'
    api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
    ll_spn = 'll=37.530887,55.703118&spn=0.002,0.002'
    map_request = f"{server_address}{ll_spn}&apikey={api_key}"
    response = requests.get(map_request)

    map_file = "map.jpg"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file

def main():
    screen = setup_screen()
    parser = argparse.ArgumentParser()
    parser.add_argument('ll', nargs=2)
    parser.add_argument('spn', nargs=2)
    args = parser.parse_args()
    map_image = request_map_image(ll=args.ll, spn=args.spn)
    screen.blit(pygame.image.load(map_image), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_image)


if __name__ == '__main__':
    main()