# Python Game - PyGame -> Game Framework
# pip install pygame
import pygame

# pygame 할때 필요한 3요소 -> init() -> 초기화 , event.get() -> 이벤트 받기, display.update() -> 화면 업데이트, 전환

pygame.init() # 1. 게임 초기화 필수
width = 500
height = 500

# pygame.display -> 화면을 그리는 역할, 이벤트를 받는 역할(키보드, 조이스틱, 마우스 등등에서 사용하는 이벤트), 쓰레드 등등
# set -> 세팅 / get -> 현재 상태를 가져오는 것
win = pygame.display.set_mode((width, height)) # 윈도우 사이즈를 500 * 500으로 만들겠다.
pygame.display.set_caption('게임만들기')

# 아이콘 설정하기
icon = pygame.image.load('./studypyGame/game.png')
pygame.display.set_icon(icon)

# object를 위한 설정
x = 250
y = 250
radius = 10
vel_x = 10    # 속도
vel_y = 10
jump = False

run = True

while run:
    win.fill((0,0,0)) # 윈도우 전체(배경)를 다시 검은색으로 변환
    pygame.draw.circle(win, (255,255,255), (x, y), radius)

    # 이벤트 = 시그널
    for event in pygame.event.get(): # 2. get()으로 이벤트를 받음
        if event.type == pygame.QUIT:
            run = False

    # object(객체) 이동 + 밖으로 나가지 않게 설정하기
    # 0,0 => 왼쪽 제일 위쪽
    userInput = pygame.key.get_pressed()
    if userInput[pygame.K_LEFT] and x > 10:
        x -= vel_x # 왼쪽으로 10씩 이동

    if userInput[pygame.K_RIGHT] and x < width - 10:
        x += vel_x # 오른쪽으로 10씩 이동

    # if userInput[pygame.K_UP] and y > 10: 
    #     y -= vel_x # 위로 10씩 이동

    # if userInput[pygame.K_DOWN] and y < height - 10:
    #     y += vel_x # 아래로 10씩 이동

    # 객체 점프
    if jump is False and userInput[pygame.K_SPACE]:
        jump = True
    
    if jump == True:
        y -= vel_y * 3
        vel_y -= 1
        if vel_y < -10:
            jump = False
            vel_y = 10
    


    pygame.time.delay(10)
    pygame.display.update()         # 3. 화면 업데이트(전환) 
