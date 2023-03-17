import pygame

pygame.init()
win = pygame.display.set_mode((1000, 500))

bg_img = pygame.image.load('./studyPyGame/Assets/Background.png')
BG = pygame.transform.scale(bg_img, (1000, 500)) # 사이즈 업
pygame.display.set_caption('게임만들기')
icon = pygame.image.load('./studypyGame/game.png')
pygame.display.set_icon(icon)

width = 1000
loop = 0
run = True

while run:
    win. fill((0,0,0))

    for event in pygame.event.get(): # 2. get()으로 이벤트를 받음
        if event.type == pygame.QUIT:
            run = False

    # 배경 그리기
    win.blit(BG, (loop,0))
    win.blit(BG, (width + loop, 0)) # 이부분을 빼면 중간에 검은색 화면이 나옴
    if loop == -width: # -1000이랑 같아지면
        # win.blit(BG, (width + loop, 0))
        loop = 0
    
    loop -= 1


    pygame.display.update()