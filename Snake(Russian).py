import pygame, random
from os import path

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Змейка')

mp3_dir = path.join(path.dirname(__file__), 'mp3')

pygame.mixer.music.load(path.join(mp3_dir, "Andreas_Waldetoft_-_Comintern_Theme_Hearts_of_Iron_IV.mp3"
                                  or "Andreas-Waldetoft-heavy-water.mp3"
                                  or "Hearts of Iron IV OST — Song For the Children of WW2.mp3"))
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)

ogg_dir = path.join(path.dirname(__file__), 'ogg')

am = pygame.mixer.Sound(path.join(ogg_dir, 'collision.ogg'))
am.set_volume(0.8)

sprite_dir = path.join(path.dirname(__file__), 'sprite')
bg = pygame.image.load(path.join(sprite_dir, 'background.png')).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bg_rect = bg.get_rect()

food_img = [pygame.image.load(path.join(sprite_dir, '1.png')).convert(),
            pygame.image.load(path.join(sprite_dir, '2.png')).convert(),
            pygame.image.load(path.join(sprite_dir, '3.png')).convert(),
            pygame.image.load(path.join(sprite_dir, '4.png')).convert(),
            pygame.image.load(path.join(sprite_dir, '5.png')).convert(),
            pygame.image.load(path.join(sprite_dir, '6.png')).convert(),
            pygame.image.load(path.join(sprite_dir, '7.png')).convert(),]

head_images = [pygame.image.load(path.join(sprite_dir, 'head_left.png')).convert(),
               pygame.image.load(path.join(sprite_dir, 'head_right.png')).convert(),
               pygame.image.load(path.join(sprite_dir, 'head_up.png')).convert(),
               pygame.image.load(path.join(sprite_dir, 'head_down.png')).convert()]

tail_images = [pygame.image.load(path.join(sprite_dir, 'tail_left.png')).convert(),
               pygame.image.load(path.join(sprite_dir, 'tail_right.png')).convert(),
               pygame.image.load(path.join(sprite_dir, 'tail_up.png')).convert(),
               pygame.image.load(path.join(sprite_dir, 'tail_down.png')).convert()]

body_images = [pygame.image.load(path.join(sprite_dir, 'body_horizontal.png')).convert(),
               pygame.image.load(path.join(sprite_dir, 'body_vertical.png')).convert()]

score = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 118, 189)
LIGHT_GREEN = (51, 204, 102)
GREEN = (51, 153, 102)
RED = (255, 0, 0)

FPS = 5

clock = pygame.time.Clock()

snake_list = []
x1 = WIDTH / 2
y1 = HEIGHT / 2

snake_block = 30
snake_step = 30
x1_change = 0
y1_change = 0
length = 2


def draw_head(i, snake_list):
    snake_head_img = head_images[i]
    snake_head = pygame.transform.scale(snake_head_img, (snake_block, snake_block))
    snake_head.set_colorkey(BLACK)
    snake_head_rect = snake_head.get_rect(x=snake_list[-1][0],
                                          y=snake_list[-1][1])
    screen.blit(snake_head, snake_head_rect)


def draw_tail(i, snake_list):
    if len(snake_list) >= 2:
        tail_x = snake_list[0][0]
        tail_y = snake_list[0][1]
        tail_direction_x = snake_list[0][0] - snake_list[1][0]
        tail_direction_y = snake_list[0][1] - snake_list[1][1]
        
        if tail_direction_x == snake_step:  # Хвост движется вправо
            tail_img = tail_images[0]  # Используем изображение хвоста, повернутого вправо
        elif tail_direction_x == -snake_step:  # Хвост движется влево
            tail_img = tail_images[1]  # Используем изображение хвоста, повернутого влево
        elif tail_direction_y == snake_step:  # Хвост движется вниз
            tail_img = tail_images[2]  # Используем изображение хвоста, повернутого вниз
        elif tail_direction_y == -snake_step:  # Хвост движется вверх
            tail_img = tail_images[3]  # Используем изображение хвоста, повернутого вверх
        else:
            tail_img = tail_images[i]  # Если хвост находится на прямой, используем текущий индекс `i`
        
        snake_tail = pygame.transform.scale(tail_img, (snake_block, snake_block))
        snake_tail.set_colorkey(BLACK)
        snake_tail_rect = snake_tail.get_rect(x=tail_x, y=tail_y)
        screen.blit(snake_tail, snake_tail_rect)


def draw_body(i, snake_list):
    if i >= len(body_images):
        i = i % len(body_images)
    snake_body_img = body_images[i]
    snake_body = pygame.transform.scale(snake_body_img, (snake_block, snake_block))
    snake_body.set_colorkey(BLACK)
    for x, y in snake_list[1:-1]:
        snake_body_rect = snake_body.get_rect(x=x, y=y)
        screen.blit(snake_body, snake_body_rect)


def eating_check(xcor, ycor, foodx, foody):
    if foodx - snake_block <= xcor <= foodx + snake_block:
        if foody - snake_block <= ycor <= foody + snake_block:
            return True
    else:
        return False


foodx = random.randrange(0, WIDTH - snake_block)
foody = random.randrange(0, HEIGHT - snake_block)


def create_mes(msg, color, x, y, font_name, size):
    font_style = pygame.font.SysFont(font_name, size)
    mes = font_style.render(msg, True, color)
    screen.blit(mes, [x, y])


def gameloop():
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0
    length = 2
    i = 0
    snake_list = []
    food = pygame.transform.scale(random.choice(food_img),
                                  (snake_block, snake_block))
    food.set_colorkey(BLACK)
    foodx = random.randrange(0, WIDTH - snake_block)
    foody = random.randrange(0, HEIGHT - snake_block)
    food_rect = food.get_rect(x=foodx, y=foody)
    run = True
    game_close = False
    score = 0

    while run:
        while game_close:
            screen.fill(RED)
            create_mes('Вы проиграли!', BLACK, 200, 200, 'railwaycargorus', 70)
            create_mes('Нажмите клавишу "С" для перезапуска', WHITE,
                       135, 300, 'railwaycargorus', 35)
            create_mes('Для окончания игры нажмите "Q"', WHITE, 170, 400, 'railwaycargorus', 35)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_close = False
                    pygame.quit(False)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        game_close = False
                    elif event.key == pygame.K_c:
                        gameloop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit(False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_step
                    y1_change = 0
                    i = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_step
                    y1_change = 0
                    i = 1
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_step
                    i = 2
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_step
                    i = 3
        for x in snake_list[1:-1]:
            if x == snake_head:
                game_close = True

        screen.fill(BLUE)
        screen.blit(bg, bg_rect)
        screen.blit(food, food_rect)

        for x in snake_list[1:]:
            snake_img = pygame.image.load(path.join(sprite_dir, 'туловище_вертикал.png')).convert()
            snake = pygame.transform.scale(snake_img, (snake_block, snake_block))
            snake.set_colorkey(WHITE)
            snake_rect = snake.get_rect(x=x[0], y=x[1])
            screen.blit(snake, snake_rect)

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]

        draw_head(i, snake_list)
        draw_body(i, snake_list)
        draw_tail(i, snake_list)

        if x1 > WIDTH or x1 <= 0 or y1 >= HEIGHT or y1 <= 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        if eating_check(x1, y1, foodx, foody):
            foodx = random.randrange(0, WIDTH - snake_block)
            foody = random.randrange(0, HEIGHT - snake_block)
            food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))
            food.set_colorkey(BLACK)
            food_rect = food.get_rect(x=foodx, y=foody)
            length += 1
            am.play()
            score += 1

        create_mes(f'Ваш счет: {score}', WHITE, 10, 10, 'railwaycargorus', 20)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    quit()

gameloop()
