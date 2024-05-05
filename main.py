import pygame
import random
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Игра Тир")
icon = pygame.image.load("img/robot.png")
pygame.display.set_icon(icon)

target_img = pygame.image.load("img/robot.png")
target_width = 80
target_height = 80

target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(0, SCREEN_HEIGHT - target_height)
target_speed_x = random.choice([-10, 10])  # Скорость движения мишени по горизонтали
target_speed_y = random.choice([-10, 10])  # Скорость движения мишени по вертикали

# Переменные для управления остановкой
stop_target = False
stop_time = 0

color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

font = pygame.font.Font(None, 36)
score = 0


def move_target():
    """ Обновляет позицию мишени на каждом кадре """
    global target_x, target_y, target_speed_x, target_speed_y, stop_target, stop_time  # Добавляем объявление глобальных переменных

    current_time = time.time()

    # Проверяем, не пора ли остановить мишень
    if not stop_target and random.random() < 0.01:  # 10% шанс остановки
        stop_target = True
        stop_time = current_time + random.uniform(0.2, 0.5)  # Остановка на 0.2-0.5 секунд

    # Проверяем, не пора ли возобновить движение
    if stop_target and current_time > stop_time:
        stop_target = False

    # Если мишень не остановлена, двигаем её
    if not stop_target:
        target_x += target_speed_x
        target_y += target_speed_y

    # Проверяем, не ударилась ли мишень о границы экрана
    if target_x <= 0 or target_x + target_width >= SCREEN_WIDTH:
        target_speed_x *= -1  # Меняем направление движения по X
    if target_y <= 0 or target_y + target_height >= SCREEN_HEIGHT:
        target_speed_y *= -1  # Меняем направление движения по Y


def update_score():
    """ Обновляет счет после попадания """
    global score
    score += 1


running = True
while running:
    screen.fill(color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                update_score()

    move_target()  # Вызываем функцию движения мишени в каждом кадре
    time.sleep(0.016)  # Примерная задержка для 60 кадров в секунду
    screen.blit(target_img, (target_x, target_y))

    score_text = font.render(f"Счет: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
