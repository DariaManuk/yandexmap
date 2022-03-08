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
    pygame.init()
    k, m = 360 / 2 ** (z-1), 180 / 2 ** (z)
    screen = pygame.display.set_mode((600, 450))
    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP and z > 0:
                    z -= 1
                    k *= 2
                    m *= 2
                elif event.key == pygame.K_PAGEDOWN and z < 18:
                    z += 1
                    k /= 2
                    m /= 2
                elif event.key == pygame.K_LEFT and a - k > -90:
                    a -= k
                elif event.key == pygame.K_RIGHT and a + k < 90:
                    a += k
                elif event.key == pygame.K_UP and b + m < 180:
                    b += m
                elif event.key == pygame.K_DOWN and b - m > -180:
                    b -= m
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={float(a)},{float(b)}&z={z}&l=map"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    os.remove(map_file)
