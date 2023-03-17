# dinoRun 
import pygame
import os
import random

pygame.init()

ASSETS = './studyPyGame/Assets/'
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, 600))

# 아이콘
icon = pygame.image.load('./studypyGame/dinoRun2.png')
pygame.display.set_icon(icon)

# 배경이미지 로드
BG = pygame.image.load(os.path.join(f'{ASSETS}Other', 'Track.png'))

# 공룡 이미지 로드
RUNNING = [pygame.image.load(f'./studyPyGame/Assets/Dino/DinoRun1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoRun2.png')]

DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')]    # Dodge

JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')

# 구름이미지
CLOUD = pygame.image.load(f'{ASSETS}Other/Cloud.png')

# 익룡이미지
BIRD = [pygame.image.load(f'{ASSETS}Bird/Bird1.png'),
           pygame.image.load(f'{ASSETS}Bird/Bird2.png')] 

# 선인장이미지
LARGE_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/LargeCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus3.png')]
SMALL_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/SmallCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus3.png')]
'''
이미지 로드하는 방법
1. ('./경로적기.png')
2. os.path.join(f'{큰 경로}'나머지, .png)
3. (f'{큰 경로}나머지경로.png')
'''

# 공룡 클래스
class Dino: 
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 9.0

    def __init__(self) -> None:
        # 공룡 상태
        self.run_img = RUNNING
        self.duck_img = DUCKING
        self.jump_img = JUMPING

        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL # 점프 초기값 : 9.0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect() # 이미지의 사각형 정보
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS 

    def update(self, userInput) -> None:
        if self.dino_run:
            self.run()
        elif self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0  # 애니메이션 스텝을 위해 사용

        if userInput[pygame.K_UP] and not self.dino_jump: # 점프
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
            self.dino_rect.y = self.Y_POS # 이게 없으면 공룡이 하늘로 날아감 (up키를 누르면 계속 위로 올라가지는 것을 방지)

        elif userInput[pygame.K_DOWN] and not self.dino_jump : # 숙이기
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        
        elif not(self.dino_jump or userInput[pygame.K_DOWN]): # 점프, 숙이기 상황 아닌 경우 -> 달리기
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

    def run(self):
        self.image = self.run_img[self.step_index // 5] # run_img / step 이 10까지 있음 0 ~ 4 ->0 /  5 -> 1 / 6 ~ 9 -> 0 / 10 -> 2
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS 
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img[self.step_index // 5] # duck_img
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK  # duck은 이미지 높이가 낮아져야 하기 때문에 Y_POS_DUCK 사용 
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL: # -9.0 이 되면 점프 중단
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL # 이걸 안해줄 경우 공룡이 아래로 내려감

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

# 구름 클래스
class Cloud:  
    def __init__(self) -> None:
        self.x = SCREEN_WIDTH + random.randint(300, 500)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self) -> None:
        self.x -= game_speed
        if self.x < -self.width:    # 화면 밖으로 벗어나면
            self.x = SCREEN_WIDTH + random.randint(1300, 2000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.x, self.y))

# 장애물 클래스
class Obstacle:
    def __init__(self, image, type) -> None:
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH  # 1100

    def update(self) -> None:
        self.rect.x -= game_speed
        if self.rect.x <= -self.rect.width: # 왼쪽 화면 밖으로 벗어나면
            obstacles.pop()      # 장애물 리스트에서 하나 꺼내오기


    def draw(self) -> None:
        SCREEN.blit(self.image[self.type], self.rect)

class Bird(Obstacle):   # 장애물 클래스 상속클래스
    def __init__(self, image) -> None:
        self.type = 0   # 새는 0
        super().__init__(image, self.type)
        self.rect.y = 250       # 새니까 하늘에
        self.index = 0  # 0 이미지로 시작

    def draw(self, SCREEN) -> None:  # draw 재정의
        if self.index >= 9:
            self.index = 0

        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class LargeCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type = random.randint(0,2) 
        super().__init__(image, self.type)
        self.rect.y = 300

class SmallCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325


# 메인함수
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    run = True
    clock = pygame.time.Clock()
    dino = Dino()   # 공룡 객체 생성
    cloud = Cloud() # 구름 객체 생성
    game_speed = 14
    obstacles = []

    font = pygame.font.Font(f'{ASSETS}NanumGothicBold.ttf', 20)

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:   # 100, 200, 300
            game_speed += 1

        txtScore = font.render(f'SCORE : {points}', True, (83,83,83))   # 공룡색(회색)
        txtRect = txtScore.get_rect()
        txtRect.center = (1000, 40)
        SCREEN.blit(txtScore, txtRect)

# dinoRun 
import pygame
import os
import random

pygame.init()

ASSETS = './studyPyGame/Assets/'
SCREEN_WIDTH = 1100  # 게임 윈도우 넓이
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, 600))

# 아이콘
icon = pygame.image.load('./studypyGame/dinoRun2.png')
pygame.display.set_icon(icon)

# 배경이미지 로드
BG = pygame.image.load(os.path.join(f'{ASSETS}Other', 'Track.png'))

# 공룡 이미지 로드
RUNNING = [pygame.image.load(f'./studyPyGame/Assets/Dino/DinoRun1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoRun2.png')]

DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')]        # Dodge -> 피하다

JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')

# 구름 이미지 로드
CLOUD = pygame.image.load(f'{ASSETS}Other/Cloud.png')

# 익룡 이미지 로드
BIRD = [pygame.image.load(f'{ASSETS}Bird/Bird1.png'),
        pygame.image.load(f'{ASSETS}Bird/Bird2.png')]

# 선인장 이미지 로드 / 애니메이션을 위한 것이 아니고 선인장 종류가 세개씩인것임
LARGE_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/LargeCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus3.png')]

SMALL_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/SmallCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus3.png')]

''' 이미지 로드하는 방법
1. ('./경로적기.png')
2. os.path.join(f'{큰 경로}'나머지, .png)
3. (f'{큰 경로}나머지경로.png')
'''

# 공룡 클래스
class Dino: 
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 9.0

    def __init__(self) -> None:
        # 공룡 상태
        self.run_img = RUNNING
        self.duck_img = DUCKING
        self.jump_img = JUMPING

        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL # 점프 초기값 : 9.0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect() # 이미지의 사각형 정보
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS 

    def update(self, userInput) -> None:
        if self.dino_run:
            self.run()
        elif self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0  # 애니메이션 스텝을 위해 사용

        if userInput[pygame.K_UP] and not self.dino_jump: # 점프
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
            self.dino_rect.y = self.Y_POS # 이게 없으면 공룡이 하늘로 날아감 (up키를 누르면 계속 위로 올라가지는 것을 방지)

        elif userInput[pygame.K_DOWN] and not self.dino_jump : # 숙이기
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        
        elif not(self.dino_jump or userInput[pygame.K_DOWN]): # 점프, 숙이기 상황 아닌 경우 -> 달리기
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

    def run(self):
        self.image = self.run_img[self.step_index // 5] # run_img / step 이 10까지 있음 0 ~ 4 ->0 /  5 -> 1 / 6 ~ 9 -> 0 / 10 -> 2
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS 
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img[self.step_index // 5] # duck_img
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK  # duck은 이미지 높이가 낮아져야 하기 때문에 Y_POS_DUCK 사용 
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL: # -9.0 이 되면 점프 중단
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL # 이걸 안해줄 경우 공룡이 아래로 내려감

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

# 구름 클래스
class Cloud():
    def __init__(self) -> None: # class 만들때 무조건 __init__ 하기!!
        self.x = SCREEN_WIDTH + random.randint(300, 500) # SCREEN_WIDTH + 300 ~ 500 사이 랜덤 값 (if 랜덤값을 추가 하기 않을 경우 구름이 계속 지나감)
        self.y = random.randint(50, 100)                 # 50 ~ 100 사이 랜덤 값 (그냥 50만 해놓을 경우 일정한 위치에 있음)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self) -> None:
        self.x -= game_speed
        if self.x < -self.width: # x축 화면 밖으로 벗어나면
            self.x = SCREEN_WIDTH + random.randint(1300, 2000) # 이렇게 해야 다음 구름 나올 때 까지 시간이 생김
            self.y = random.randint(50, 100)

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.x, self.y))

# 장애물 클래스 (부모클래스)
class Obstacle:
    def __init__(self, image, type) -> None:
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH #1100

    def update(self) -> None:
        self.rect.x -= game_speed
        if self.rect.x <= -self.rect.width: # 왼쪽 화면 밖으로 벗어나면
            obstacles.pop()                  # 장애물(배열)에서 하나 꺼내오기

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image[self.type], self.rect)

class Bird(Obstacle): # 장애물 클래스를 상속받는 상속 클래스
    def __init__(self, image) -> None:
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0 # 새 이미지 2개이기 때문에 0번 이미지로 먼저 시작함을 의미함

    def draw(self, SCREEN) -> None: # draw 재정의
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class LargeCactus(Obstacle):
    def __init__(self, image) -> None: 
        self.type = random.randint(0, 2) # 큰 선인장 세 개 중 한 개 고르기
        super().__init__(image, self.type)
        self.rect.y = 300

class SmallCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type = random.randint(0, 2) # 작은 선인장 세 개 중 한 개 고르기
        super().__init__(image, self.type)
        self.rect.y = 325

# 메인함수
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0     # 게임 점수 0부터 시작
    run = True
    clock = pygame.time.Clock()
    dino = Dino()   # 공룡 객체 생성
    cloud = Cloud() # 구름 객체 생성
    game_speed = 14
    obstacles = []   # 장애물 리스트

    font = pygame.font.Font(f'{ASSETS}NanumGothicBold.ttf', 20)

    def score(): # 점수 표시 위한 함수 내 함수
        global points, game_speed
        points += 1
        if points % 100 == 0: # 100, 200, 300, ... 
            game_speed += 1   # 점수가 높아지면 게임 속도 증가
        
        txtScore = font.render(f'SCORE : {points}', True, (83, 83, 83)) # 공룡하고 같은 색으로 score 표시
        txtRect = txtScore.get_rect()
        txtRect.center = (1000, 40)
        SCREEN.blit(txtScore, txtRect) 
        
    def background(): # 배경 update, draw 동시에 해주는 함수 내 함수
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width() # 2404
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg)) # 0, 380에 먼저 그림
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))  # 2404+ 0, 380
        # 2D 게임을 만들 때 그림을 두 번 그려야 흘러가는 것 처럼 보임, 아닐 경우 한번그려지고 끝남
        if x_pos_bg <= -image_width:
            # SCREEN_WIDTH.blit(BG, (x_pos_bg, y_pos_bg))
            x_pos_bg = 0

        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255)) # 배경 흰색
        userInput = pygame.key.get_pressed()

        background()
        score()

        cloud.draw(SCREEN) # 구름이 계속 흘러감 
        cloud.update()     # 구름은 user가 움직일 필요 없기 때문에 userInput 필요 없음
        # if 구름 그리기가 공룡 그리기 뒤에 위치할 경우 공룡 앞으로 구름이 지나감
        # => 구름을 먼저 그려야 함 (배경이기 때문에)

        dino.draw(SCREEN) # 공룡을 게임스크린에 그리기
        dino.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0: # 작은선인장
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0,2) == 1: # 큰선인장
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2: # 새
                obstacles.append(Bird(BIRD))

        for obs in obstacles:
            obs.draw(SCREEN)
            obs.update()
            # Collision Detection 충돌 감지
            if dino.dino_rect.colliderect(obs.rect):
                pygame.draw.rect(SCREEN, (255, 0, 0), dino.dino_rect, 3)

        clock.tick(30)   # 숫자를 늘릴경우 속도가 빨라짐 (30이 기본)
        pygame.display.update() # fps 초당 프레임 수 => 초당 30번 update 수행

if __name__ == '__main__':
    main()
    def background():       # 땅바닥 update, draw 동시에 해주는 함수
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()        # 2404
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))   # 0, 380 먼저 그림
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg)) # 2404+0, 380
        if x_pos_bg <= -image_width:
            x_pos_bg = 0

        x_pos_bg -= game_speed


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255)) # 배경 흰색
        userInput = pygame.key.get_pressed()

        background()
        score()

        cloud.draw(SCREEN)  # 구름 애니메이션
        cloud.update()      # 구름이 공룡앞으로 지나가야함

        dino.draw(SCREEN) # 공룡을 게임스크린에 그리기
        dino.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0,2) == 0:    # 작은 선인장
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:     # 큰 선인장
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:     # 새
                obstacles.append(Bird(BIRD))

        for obs in obstacles:
            obs.draw(SCREEN)
            obs.update()
            # Collision Detection
            if dino.dino_rect.colliderect(obs.rect):
                pygame.draw.rect(SCREEN, (255,0,0), dino.dino_rect, 3)
        

        clock.tick(30)      # 30기본 60이면 빨라짐
        pygame.display.update() # fps 초당 프레임 수 => 초당 30번 update 수행

if __name__ == '__main__':
    main()


