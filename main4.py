import os
import sys
import pygame
import requests
type_list = ["map", "sat", "sat,skl"]
type_count = 0
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
    update = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                screen.fill('blue')
                r = 1
                spis = event.pos

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    z -= 1
                    update = True
                elif event.key == pygame.K_s:
                    z += 1
                    update = True

                if event.key == pygame.K_LEFT:
                    a -= 0.5
                    update = True
                elif event.key == pygame.K_RIGHT:
                    a += 0.5
                    update = True

                if event.key == pygame.K_UP:
                    b -= 0.5
                    update = True
                elif event.key == pygame.K_LEFT:
                    b += 0.5
                    update = True
                if event.key == pygame.K_SPACE:
                    type_count += 1
                    type_count %= 3
                    update = True
                    print(type_list[type_count])
                # широта от -90 до 90
                # долгота от -180 до 180
                if b > 90:
                    b = 90
                if b < -90:
                    b = -90
                if a > 180:
                    a = 180
                if a < -180:
                    a = -180

                if z > 18:
                    z = 18
                if z < 0:
                    z = 0
        if update:
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={a},{b}&z={z}&l={type_list[type_count]}"
            response = requests.get(map_request)
            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
            update = False
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    os.remove(map_file)
