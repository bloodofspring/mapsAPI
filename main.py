import pygame
import argparse
import requests
import io


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
    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = requests.get(map_api_server, params=map_params)
    return io.BytesIO(response.content)


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


if __name__ == '__main__':
    main()