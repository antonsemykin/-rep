import csv
import os
import random
import sys

import pygame

from pygame.math import Vector2
from pygame.draw import rect

pygame.init()

screen = pygame.display.set_mode([800, 600])

# управляет игрой во время цикла
done = False

# управляет запуском игры из главного меню
start = False

# устанавливает частоту кадров в программе
clock = pygame.time.Clock()

# const
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

color = lambda: tuple([random.randint(0, 255) for i in range(3)])  # лямбда-функция нужна для случайного цвета, и не является const константа.

GRAVITY = Vector2(0, 0.86)  # Vector2 - pygame - сила гравитации


"""
Класс игрока
"""

class Player(pygame.sprite.Sprite):
    
    # Класс для игрока. Содержит метод обновления, переменные "победа" и "смерть", столкновения и многое другое.
    
    win: bool
    died: bool

    def __init__(self, image, platforms, pos, *groups):
        """
        :параметр image: спрайт блока
        :параметр platforms: препятствия, такие как монеты, блоки, шипы и сферы
        :параметр pos: начальная позиция
        :параметр groups: может использоваться любое количество групп спрайтов.
        """
        super().__init__(*groups)
        self.onGround = False  # игрок на земле?
        self.platforms = platforms  # переменная класса для препятствия
        self.died = False  # игрок погиб?
        self.win = False  # игрок победил?

        self.image = pygame.transform.smoothscale(image, (32, 32))
        self.rect = self.image.get_rect(center=pos)  # get rect возвращает прямоугольный объект с изображения
        self.jump_amount = 10.5  # сила прыжка
        self.particles = []  # партиклы за игроком (следы)
        self.isjump = False  # прыгает ли игрок?
        self.vel = Vector2(0, 0)  # скорость начинается с нуля

    def draw_particle_trail(self, x, y, color=(255, 255, 255)):
    # рисует дорожку из прямоугольников частиц в виде линии в случайных местах позади игрока

        self.particles.append(
                [[x - 5, y - 8], [random.randint(0, 25) / 10 - 1, random.choice([0, 0])],
                 random.randint(5, 8)])

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.5
            particle[1][0] -= 0.4
            rect(alpha_surf, color,
                 ([int(particle[0][0]), int(particle[0][1])], [int(particle[2]) for i in range(2)]))
            if particle[2] <= 0:
                self.particles.remove(particle)

    def collide(self, yvel, platforms):
        global coins

        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                # встроенный в pygame метод проверки столкновения,
                # видит, сталкивается ли игрок с какими-либо препятствиями
                if isinstance(p, Orb) and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
                    pygame.draw.circle(alpha_surf, (255, 255, 0), p.rect.center, 18)
                    screen.blit(pygame.image.load("images/editor-0.9s-47px.gif"), p.rect.center)
                    self.jump_amount = 12  # увеличивает прыжок до 12 когда игрок сталкивается со сферой
                    self.jump()
                    self.jump_amount = 10.5  # возвращение обратно значения прыжка

                # 2 батута, вверх и вниз
                if isinstance(p, Teleport):
                    self.jump_amount = 20
                    self.jump()
                    self.jump_amount = 10.5  # возвращение обратно значения прыжка

                if isinstance(p, TeleportMinus):
                    self.jump_amount = 20
                    self.jumpMinus()
                    self.jump_amount = 10.5  # возвращение обратно значения прыжка

                if isinstance(p, End):
                    self.win = True

                if isinstance(p, Spike):
                    self.died = True  # смерть, если ударился об колючку

                if isinstance(p, Coin):
                    # отслеживает количество собранных монет(max 6)
                    coins += 1

                    # стирает монету при соприкосновении
                    p.rect.x = 0
                    p.rect.y = 0

                if isinstance(p, Platform):  # это блоки(не платформа)

                    if yvel > 0:
                        # если игрок находится на земле, то:
                        self.rect.bottom = p.rect.top  # не дает игроку провалиться сквозь землю
                        self.vel.y = 0  # скорость падения = 0, тк игрок находится на земле

                        self.onGround = True  # игрок на земле?
                        
                        self.isjump = False # если игрок на земле, значит он не в прыжке, логично
                    
                    elif yvel < 0:
                        # если игрок столкнулся во время прыжка, то:
                        self.rect.top = p.rect.bottom  
                        """
                        верх игрока(по y) устанавливается так, чтобы игрок ударялся ей
                        об нижнюю часть блока(по y)
                        """
                    
                    else:
                        # любое другое соприкосновениие с блоком - смерть
                        self.vel.x = 0
                        self.rect.right = p.rect.left  # не позволяет игроку проходить сквозь стены
                        self.died = True # смерть)
                        coins = 0


    def jump(self):
        self.vel.y = -self.jump_amount  # ось OY перевернута поэтому минус чтобы прыжок был вверх

    def jumpMinus(self):
        self.vel.y = self.jump_amount

    def update(self):
        # обновляем параметры игрока
        if self.isjump:
            if self.onGround:
                # можно прыгнуть только если ты находишься на земле!
                self.jump()

        if not self.onGround:  # прижимает к земле только если находишься в воздухе
            self.vel += GRAVITY  # Gravity Falls (ускорение свободного падения)

            # максимальная скорость падения
            if self.vel.y > 100: self.vel.y = 100

        # проверяет столкновение по оси OX
        self.collide(0, self.platforms)

        # увеличение в направлении y
        self.rect.top += self.vel.y

        """предполагается, что игрок находится в воздухе, а если нет,
        то после падения он будет перевернут"""
        self.onGround = False

        # проверяет столкновение по оси OY
        self.collide(self.vel.y, self.platforms)

        """если игрок умер, выведется экран поражения
        если пользователь победил(и игрок тоже, в этом уровне),
        то выведется сцена победы"""
        eval_outcome(self.win, self.died)



"""
Классы препятствий
"""

# "Родительский" класс
class Draw(pygame.sprite.Sprite):
    # Родительский класс - для всех классов препятствий

    # Класс спрайтов
    def __init__(self, image, pos, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


#  ====================================================================================================================#
#  Отдельный класс для каждого препятствия
#  ====================================================================================================================#

# Дочерние классы
class Platform(Draw):
    """Блок"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)


class Spike(Draw):
    """Шип"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)


class Coin(Draw):
    """Монета(собери 6 для победы)"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)


class Orb(Draw):
    """Сфера(дает прыжок)"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)


class Teleport(Draw):
    """телепорт"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)

class TeleportMinus(Draw):
    """телепортMinus"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)

class Trick(Draw):
    """Блок, через который можно пройти"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)


class End(Draw):
    """Большой спрайт игрока, заменяет финиш, зайди в него чтобы выиграть"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)



"""
Функции
"""

def init_level(map):
    """это похоже на 2d-списки. программа просматривает список списков
    и создает экземпляры определенных препятствий в зависимости от элемента в списке"""
    x = 0
    y = 0

    # Создаем карту по нашему .csv файлу
    for row in map:
        for col in row:

            if col == "0":
                Platform(block, (x, y), elements)

            if col == "Coin":
                Coin(coin, (x, y), elements)

            if col == "Spike":
                Spike(spike, (x, y), elements)
            if col == "Orb":
                # orbs.append([x, y])

                Orb(orb, (x, y), elements)

            if col == "T":
                Trick(trick, (x, y), elements)

            if col == "Tp":
                Teleport(teleport, (x, y), elements)

            if col == "TpM":
                TeleportMinus(teleportMinus, (x, y), elements)

            if col == "End":
                End(avatar, (x, y), elements)
            x += 32
        y += 32
        x = 0


def blitRotate(surf, image, pos, originpos: tuple, angle: float):
    """
    Поворот игрока
    :параметр surf: Поверхность
    :параметр image: Изображение для поворота
    :параметр pos: Положение изображения
    :параметр originpos: Координаты x и y вокруг которых нужно повернуть
    :параметр angle: Угол поворота
    """

    # вычислить выровненную по оси ограничивающую рамку повернутого изображения
    w, h = image.get_size()
    box = [Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]

    # убедитесь, что проигрыватель не перекрывает друг друга, используйте несколько лямбда-функций    
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
   
    # рассчитайте перемещение оси поворота
    pivot = Vector2(originpos[0], -originpos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # вычислить начало координат верхнего левого угла повернутого изображения    
    origin = (pos[0] - originpos[0] + min_box[0] - pivot_move[0], pos[1] - originpos[1] - max_box[1] + pivot_move[1])

    # получить повернутое изображение
    rotated_image = pygame.transform.rotozoom(image, angle, 1)

    # повернуть и сделать blit изображения
    surf.blit(rotated_image, origin)


def won_screen():
    """Этот экран появится при прохождении уровня"""
    global attempts, level, fill, coins
    attempts = 0
    player_sprite.clear(player.image, screen)
    screen.fill(pygame.Color("yellow"))
    txt_win1 = txt_win2 = "Ничего"

    local_level = level + 1
    if level == 0:            
        txt_win2 = f"Вы собрали {coins} из 6 монет! [SPACE] - след. уровень."
        if coins == 6:
            txt_win1 = f"Уровень {local_level} пройден!"
        else:
            txt_win1 = f"Уровень {local_level} НЕ пройден до конца!"

    elif level == 1:
        txt_win2 = f"Вы собрали {coins} из 6 монет! [SPACE] - выход."
        if coins == 6:
            txt_win1 = f"Уровень {local_level} пройден!"
        else:
            txt_win1 = f"Уровень {local_level} НЕ пройден до конца!"

    txt_win = f"{txt_win1}"
    txt_win_2 = f"{txt_win2}"
    txt_win_3 = f"YOU WIN"

    won_game = font.render(txt_win, True, BLACK)
    won_game_2 = font.render(txt_win_2, True, BLACK)
    won_game_3 = font2.render(txt_win_3, True, BLUE)

    screen.blits([[won_game, (10, 300)], [won_game_2, (10, 332)], [won_game_3, (350, 200)]])

    level += 1
    coins = 0
    fill = 0

    wait_for_key()
    reset()


def death_screen():
    """Этот экран появится при смерти"""
    global attempts, fill, coins, progress_colors
    coins = 0
    
    player_sprite.clear(player.image, screen)
    attempts += 1
    game_over = font.render("[SPACE] - играть снова, ESC - выход", True, WHITE)
    game_over_2 = font2.render("YOU LOSE", True, RED)

    txt_gameover3 = f"{int(fill/8)-1}%"
    game_over_3 = font2.render(txt_gameover3, True, progress_colors[int(fill / 175)])

    screen.fill(pygame.Color("sienna1"))
    screen.blits([[game_over, (190, 350)], [tip, (220, 450)], [game_over_2, (330, 200)], [game_over_3, (375, 250)]])

    fill = 0
    wait_for_key()
    reset()


def eval_outcome(won: bool, died: bool):
    """Простая функция для вывода нужного экрана"""
    if won:
        won_screen()
    if died:
        death_screen()


def block_map(level_num):
    """
    :введите level_num: rect(screen, BLACK), (0, 0, 32, 32))
    откройте csv-файл, содержащий нужную карту уровня
    """
    lvl = []
    with open(level_num, newline='') as csvfile:
        trash = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in trash:
            lvl.append(row)
    return lvl


def start_screen():
    """Главное меню: выбор уровня, старт игры, управление, подсказка"""
    global level
    if not start:
        screen.fill(BLACK)
        if pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1]:
            level = 0
        if pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2]:
            level = 1

        welcome = font.render(f"Выбери уровень с помощью цифр ({level+1} или {abs(level-2)})", True, WHITE)

        controls = font.render(f"Управление: ПРЫЖОК - Space/Up ВЫХОД - Esc.", True, GREEN)

        screen.blits([[welcome, (100, 100)], [controls, (100, 450)], [tip, (100, 500)]])

        level_memo = font.render(f"Выбранный уровень - {level + 1}", True, (255, 255, 0))
        screen.blit(level_memo, (100, 150))

        gamestart = font2.render(f"[SPACE] - НАЧАТЬ ИГРУ", True, RED)
        screen.blit(gamestart, (100, 300))

def reset():
    """возвращает группы спрайтов, музыку и т.д. для смерти и нового уровня"""
    global player, elements, player_sprite, level

    if level == 1:
        pygame.mixer.music.load(os.path.join("music", "Сastle-town.mp3"))
    elif level == 0:
        pygame.mixer.music.load(os.path.join("music", "bossfight-Vextron.mp3"))
    pygame.mixer_music.play()
    player_sprite = pygame.sprite.Group()
    elements = pygame.sprite.Group()
    player = Player(avatar, elements, (150, 450), player_sprite) # положение игрока при начале игры
    init_level(
            block_map(
                    level_num=levels[level]))


def move_map():
    """Перемещение препятствий по экрану"""
    for sprite in elements:
        sprite.rect.x -= CameraX


def draw_stats(surf, money=0):
    """
    отображает индикатор выполнения уровня(полоска свверху), количество попыток, отображает собранные монеты
    и постепенно меняет цвет индикатора выполнения
    """
    global fill, progress_colors
    progress_colors = [pygame.Color("red"), pygame.Color("orange"), pygame.Color("yellow"), pygame.Color("lightgreen"),
                       pygame.Color("green"), pygame.Color("BLUE"), pygame.Color("pink")]

    tries = font.render(f"Попытки - {str(attempts)}", True, WHITE)
    itcoins = font.render(f"Монеты - {coins}", True, WHITE)
    BAR_LENGTH = 800
    BAR_HEIGHT = 10

    for i in range(1, money):
        screen.blit(coin, (BAR_LENGTH, 25))

    if player.win:
        fill = 0
    fill += 1.05
    outline_rect = pygame.Rect(0, 0, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(0, 0, fill, BAR_HEIGHT)
    col = progress_colors[int(fill / 175)]
    rect(surf, col, fill_rect, 0, 4)
    rect(surf, WHITE, outline_rect, 3, 4)
    # screen.blit(tries, (BAR_LENGTH, 0))
    # screen.blit(itcoins, (BAR_LENGTH, 25))
    screen.blit(tries, (5, 20))
    screen.blit(itcoins, (5, 40))

def wait_for_key():
    """
    отдельный цикл для ожидания нажатия клавиши во время
    выполнения игрового цикла
    """
    global level, start
    waiting = True
    while waiting:
        clock.tick(60)
        pygame.display.flip()

        if not start:
            start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    waiting = False
                    if level == 2:
                        pygame.quit()
                        sys.exit()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def coin_count(coins):
    """Счетчик монет"""
    if coins >= 3:
        coins = 3
    coins += 1
    return coins


def resize(img, size=(32, 32)):
    """
    Изменение размера изображений

    :параметр img: картинка, для изменения размера
    :тип img: объект?
    :параметр size: 32 пикселя - дефолт размер
    :тип size: запись
    :return: img с изм. размером

    :rtype:object? что-то сложное
    """
    resized = pygame.transform.smoothscale(img, size)
    return resized


"""
Глобальные переменные
"""
font = pygame.font.SysFont("lucidaconsole", 20)
font2 = pygame.font.SysFont("lucidaconsole", 30)

# квадрат - главный игрок
avatar = pygame.image.load(os.path.join("images", "avatar.png"))  # загрузка изображения игрока
pygame.display.set_icon(avatar)

"""
эта поверхность имеет альфа-значение для цветов,
поэтому след игрока будет исчезать при использовании непрозрачности
"""
alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

# группы спрайтов
player_sprite = pygame.sprite.Group()
elements = pygame.sprite.Group()

# спрайты
spike = pygame.image.load(os.path.join("images", "obj-spike.png"))
spike = resize(spike)
coin = pygame.image.load(os.path.join("images", "coin.png"))
coin = pygame.transform.smoothscale(coin, (32, 32))
block = pygame.image.load(os.path.join("images", "block_1.png"))
block = pygame.transform.smoothscale(block, (32, 32))
orb = pygame.image.load((os.path.join("images", "orb-yellow.png")))
orb = pygame.transform.smoothscale(orb, (32, 32))
teleport = pygame.image.load((os.path.join("images", "tele2.png")))
teleport = pygame.transform.smoothscale(teleport, (96, 32))
teleportMinus = pygame.image.load((os.path.join("images", "CubePortal.png")))
teleportMinus = pygame.transform.smoothscale(teleportMinus, (96, 32))
trick = pygame.image.load((os.path.join("images", "obj-breakable.png")))
trick = pygame.transform.smoothscale(trick, (32, 32))

#  целые переменные
fill = 0
num = 0
CameraX = 0
attempts = 0
coins = 0
angle = 0
level = 0

# списки
progress_colors = []
particles = []

# инициализация уровня
levels = ["level_1.csv", "level_2.csv"]
level_list = block_map(levels[level])
level_width = (len(level_list[0]) * 32)
level_height = len(level_list) * 32
init_level(level_list)

# текст сверху
pygame.display.set_caption('Geometry Dash на Python')

# переменная font, которая будет отрисовыывать текст
text = font.render('image', False, (255, 255, 0))

# музыка
if level == 1:
    pygame.mixer.music.load(os.path.join("music", "Сastle-town.mp3"))
elif level == 0:
    pygame.mixer.music.load(os.path.join("music", "bossfight-Vextron.mp3"))
pygame.mixer_music.play()

# фон
bg = pygame.image.load(os.path.join("images", "bg.png"))

# создаем объект класса player
player = Player(avatar, elements, (150, 450), player_sprite)

# подсказка
tip = font.render("Подсказка: Остерегайся шипов!", True, BLUE)


# главный цикл игры
while not done:
    keys = pygame.key.get_pressed()

    if not start:
        wait_for_key()
        reset()

        start = True

    player.vel.x = 6

    eval_outcome(player.win, player.died)
    if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
        player.isjump = True

    # Уменьшать альфа-значение всех пикселей на этой поверхности в каждом кадре.
    # Контролировать fade2(скорость затухания) с помощью альфа-значения.
    alpha_surf.fill((255, 255, 255, 1), special_flags=pygame.BLEND_RGBA_MULT)

    player_sprite.update()
    CameraX = player.vel.x  # для перемещения препятствий
    move_map()  # применять CameraX ко всем элементам

    screen.blit(bg, (0, 0))  # очистка экрана(bg)

    player.draw_particle_trail(player.rect.left - 1, player.rect.bottom + 2,
                               WHITE)
    screen.blit(alpha_surf, (0, 0))  # выделить на экране alpha_surf
    draw_stats(screen, coin_count(coins))

    if player.isjump:
        # переверни игрока на угол, и отрисуй его если он прыгнет
        """
        это может быть угол, необходимый для поворота на 360 градусов на расстояние,
        пройденное игроком за один прыжок
        """
        angle -= 8.1712  
        # angle -= 15
        blitRotate(screen, player.image, player.rect.center, (16, 16), angle)
    else:
        # если player.isjump == False, то рисуем его обычным способом
        player_sprite.draw(screen)  # рисуем группу спрайтов игрока
    elements.draw(screen)  # рисуем все оставшиеся объекты

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                """User friendly exit"""
                done = True
            # if event.key == pygame.K_2:
            #     """change level by keypad"""
            #     player.jump_amount += 1

            # if event.key == pygame.K_1:
            #     """change level by keypad"""

            #     player.jump_amount -= 1

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
