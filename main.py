import os
import sys
import pygame
import requests


if __name__ == '__main__':
    print('Введите долготу координат')
    a = int(input())
    print('Введите широту координат')
    b = int(input())
    print('Введите масштаб карты')
    z = int(input())
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={a},{b}&z={z}&l=map"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    os.remove(map_file)
