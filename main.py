import os
import sys
import pygame
import requests

dol = {}
shir = {}
for i in range(18, -1, -1):
    dol[i] = 180 / 2 ** i
for j in range(18, -1, -1):
    shir[j] = 360 / 2 ** j

if __name__ == '__main__':
    print('Введите долготу координат')
    a = int(input())
    print('Введите широту координат')
    b = int(input())
    print('Введите масштаб карты')
    z = int(input())
    pygame.init()
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
                elif event.key == pygame.K_PAGEDOWN and z < 18:
                    z += 1
                elif event.key == pygame.K_LEFT and a - dol[z] > -90:
                    a -= dol[z]
                elif event.key == pygame.K_RIGHT and a + dol[z] < 90:
                    a += dol[z]
                elif event.key == pygame.K_UP and b + shir[z] < 180:
                    b += shir[z]
                elif event.key == pygame.K_DOWN and b - shir[z] > -180:
                    b -= shir[z]
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
