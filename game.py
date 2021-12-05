import pygame

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

SPAWN_POSITION = (0, 0)

class Ground:

    def __init__(self) -> None:
        self.height = 50
        self.width = SCREEN_WIDTH
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - self.height, SCREEN_WIDTH, self.height)
    
    def draw(self) -> None:
        return pygame.draw.rect(screen, self.color, self.rect)



class Player:

    def __init__(self, color=(26, 0, 26), name='karen') -> None:
        self.color = color
        self.name = name
        self.rect = pygame.Rect(*SPAWN_POSITION, 20, 50)
        self.gravity = 15
        self.jumping = 0
        self.falling = 0.0
        self.jumprange = 400

    def draw(self) -> None:
        return pygame.draw.rect(screen, self.color, self.rect)

    def gravity_fall(self):
        if self.rect.y + self.gravity <= 500:
            self.rect.y += self.gravity
        else:
            self.rect.y += 500 - self.rect.y
    
    def jump(self):
        if not self.jumping:
            self.jumping = self.jumprange // 8
    
    def progjump(self):
        if self.jumprange:
            if self.jumping > self.jumprange:
                self.jumping = self.jumprange
            self.jumping -= 5 if self.jumping > 5 else 0
            self.rect.y -= self.jumping
            self.jumprange -= self.jumping

            if not self.jumprange:
                self.jumprange = 400
                self.jumping = 0

            


    



clock = pygame.time.Clock()
ground = Ground()
mainplayer = Player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                mainplayer.jump()

    screen.fill((0, 153, 255))
    ground.draw()
    mainplayer.draw()
    mainplayer.gravity_fall()
    mainplayer.progjump()
    pygame.display.flip()
    clock.tick(60)