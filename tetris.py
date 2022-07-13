import pygame
from copy import deepcopy
from random import choice, randrange


# создаем пустое черное окно заданного расширения
W = 10  # игровое поле, 10 х 20 плиток
H = 20
TILE = 30  # размер самой плитки
GAME_RES = W * TILE, H * TILE
RES = 600, 670
FPS = 60  # количество кадров

pygame.init()
sc = pygame.display.set_mode(RES)                  #метод, который инициализирует Surface, который устанавливает окно
game_sc = pygame.Surface(GAME_RES)  # создаем доплнительную поверхность, игровое поле  отдельно
clock = pygame.time.Clock()  # создать объект, чтобы помочь отслеживать время.

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]  # рисуем сетку,
# Rect -  КЛАСС, прямоугольные области, имеющие координаты, длину и ширин

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in
           figures_pos]  # отцентрировали нашу фигуру, падает по середине
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for i in range(H)]  # поле, где храним положение упавших фигур
anim_count = 0  # для спуска фигур, счетчик для количество плиток, скорость, предельное количество плиток
anim_speed = 60
anim_limit = 2000

figure = deepcopy(choice(figures))

bg = pygame.image.load('img/bg2.jpg').convert()
game_bg = pygame.image.load('img/bg.jpg').convert()

main_font = pygame.font.Font('font/font.ttf', 55)                   #надписи
font = pygame.font.Font('font/font.ttf', 40)

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkred'))
title_score = font.render('SCORE:', True, pygame.Color('darkred'))
title_record = font.render('RECORD:', True, pygame.Color('darkred'))


get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))        #аноним функция, разукрашиваем фигуры
figure = deepcopy(choice(figures))
next_figure = deepcopy(choice(figures))
color = get_color()
next_color = get_color()

for i in range(4):  # рисуем саму фигу, диапазон до 4, так как в фигуре 4 плитки
    figure_rect.x = figure[
                        i].x * TILE  # в списке берем по индексу фигуру, получаем ее координаты и умножаем на размер плитки
    figure_rect.y = figure[i].y * TILE
    pygame.draw.rect(game_sc, color,figure_rect)  # еще экранная поверхность белого цвета = 0              #счетчик для очков

score = 0               #счетч
lines = 0              #счетчик для линий
scores = {0:0, 1:100, 2:400, 3:600, 4:800}    #система оценки

def check_borders():  # функция для границ
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    if figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:  # вышли за вертикальную границу или там уже лежит фигура
        return False
    return True

def get_record():                      #функция для рекорда
    try:
       with open('record')  as f:     #открываем файл с рекордом
           return f.readline()
    except FileNotFoundError:          #если файла нет, создаем его и записываем 0 очков
        with open('record', 'w') as f:
            f.write('0')

def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


while True:
    record = get_record()
    dx = 0  # для сдвига
    rotate = False  # для вращения
    sc.blit(bg, (0, 0))                     #загрузили картинки на фон
    sc.blit(game_sc, (20, 20))              #загрузили картинки на фон
    game_sc.blit(game_bg, (0, 0))            #игровое поле на основное окно

    for i in range(lines):                     #задержка времени при полной линии
        pygame.time.wait(200)                 #time.wait делает окно зависшим
    # control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # после выполнения этой функции отключаются модули библиотеки pygame,
            exit()  # но выхода из цикла и программы не происходит
        if event.type == pygame.KEYDOWN:  # модуль клавиатуры для сдвига фигур
            if event.key == pygame.K_LEFT:
                dx = -1  # изменяем координаты
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:  # вниз
                anim_limit = 100
            elif event.key == pygame.K_UP:  # вращение
                rotate = True

    # move x
    figure_old = deepcopy(figure)  # копия фигуры
    for i in range(4):  # цикл для сдвига фигур
        figure[i].x += dx
        if not check_borders():  # если фигура вышла за границу, то мы берем копия и возвращаем ее первоначальное положение
            figure = deepcopy(figure_old)
            break
    # move y
    anim_count += anim_speed  # падение фигуры
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)  # копия фигуры
        for i in range(4):  # цикл для сдвига фигур
            figure[i].y += 1  # по оси у спускаемся
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure = next_figure                                #следующая фигура
                color = next_color
                next_figure = deepcopy(choice(figures))          # если фиугра дошла до нижней границы, выбираем новую
                next_color = get_color()
                anim_limit = 2000
                break
    # rotate
    center = figure[0]                               # центра вращения фигур
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[
                    i].y - center.y               # вращаем по часовой стрелке, считаем разницу между коорд. плитки и центром вращения
            y = figure[i].x - center.x
            figure[i].x = center.x - x          # полуаем новые координаты фигуры, от центра отнимаем разницу
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure)
                break
    # check lines
    line = H - 1                                   # последняя линия на игровом поле
    lines = 0
    for row in range(H - 1, -1, -1):
        count = 0                                    # счетчик для заполненных плиток
        for i in range(W):
            if field[row][i]:
                count += 1                             # счетчик для заполненных плиток
            field[line][i] = field[row][i]            # заполненные линии переписываются сверху пустыми
        if count < W:
            line -= 1
        else:
            anim_speed += 3                          #увеличиваем скорость падения
            lines += 1                               #счетчик линий
    # compute score
    score += scores[lines]                            #для подсчета очков

    # grid
    [pygame.draw.rect(game_sc, (25, 25, 25), i_rect, 1) for i_rect in grid]  # rect - функция модуля draw, не путать с классом

    # figure
    for i in range(4):                                    # рисуем саму фигу, диапазон до 4, так как в фигуре 4 плитки
        figure_rect.x = figure[i].x * TILE                # в списке берем по индексу фигуру, получаем ее координаты и умножаем на размер плитки
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)     # еще экранная поверхность белого цвета

    # field                                             #рисуем  на поле для фигур упавшие фигуры
    for y, raw in enumerate(
            field):                                   # enumerate(), функция возвращает две переменные цикла: количество текущих итераций и значение элемента на текущей итерации
        for x, col in enumerate(raw):
            if col:
                figure_rect.x = x * TILE
                figure_rect.y = y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
    # next figure
    for i in range(4):                                    # рисуем следующую фигу, диапазон до 4, так как в фигуре 4 плитки
        figure_rect.x = next_figure[i].x * TILE + 310          # в списке берем по индексу фигуру, получаем ее координаты и умножаем на размер плитки
        figure_rect.y = next_figure[i].y * TILE + 130
        pygame.draw.rect(sc, next_color, figure_rect)      # еще экранная поверхность белого цвета



    # titles
    sc.blit(title_tetris, (350, 20))      #надписи
    sc.blit(title_score, (380, 500))
    sc.blit(font.render(str(score), True, pygame.Color('black')), (430, 550))
    sc.blit(title_record, (380, 400))
    sc.blit(font.render(record, True, pygame.Color('black')), (430, 450))

    # game over
    for i in range(W):                      #концовка игры
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]                #делаем игровое поле чистым
            anim_count = 0                                                   #возвращаем изначальные параметры
            anim_speed = 60
            anim_limit = 2000
            score = 0                                                     #обнуляем счет
            for i_rect in grid:                                            # делаем разноцветные квадраты заполняют фон
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()                                   # располагает элементы в обратном порядке вдоль указанной оси, при этом размеры массива не изменяются
    clock.tick(FPS)                                      # считает время
