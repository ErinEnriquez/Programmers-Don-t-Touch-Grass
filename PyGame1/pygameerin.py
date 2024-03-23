import pygame
import random
#from game_over_screen import game_over_screen

# width height color
screenWidth = 1280   #800                   
screenHeight = 720   #600
charWidth = 40
charHeight = 60
obstacleWidth = 60
obstacleHeight = 40
platformWidth = 200
platformHeight = 20
platformColor = (0, 255, 0)                   
charColor = (255, 0, 0)
obstacleColor = (0, 0, 255)
bgColor = (0, 0, 0)
gravity = 0.2
platformSpeed = 3            
obstacleMovingSpeed = 3                          
              
class Character:
    def __init__(self):
        self.image = pygame.image.load("genie.png")
        self.rect = self.image.get_rect()
        #self.rect.center = (screenWidth // 2, screenHeight - self.rect.height)
        self.rect.center = (screenWidth // 2 - charWidth // 2, screenHeight - charHeight)
        self.x = screenWidth // 2 - charWidth // 2
        self.y = screenHeight - charHeight
        self.vel_y = 0
        self.on_ground = True
        self.jump_power = 0            
 
    def jump(self):
        self.jump_power = 15  # Initial jump power
        self.on_ground = False
        #self.vel_y = 0

    def update(self):
        if self.jump_power > 0:
            self.vel_y = -self.jump_power
            self.jump_power -= 1

        self.y += self.vel_y
        self.vel_y += gravity

        if self.y >= screenHeight - charHeight:
            self.y = screenHeight - charHeight
            self.vel_y = 0
            self.on_ground = True

    def draw(self, screen):
        #pygame.draw.rect(screen, charColor, (self.x, self.y, charWidth, charHeight))
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
       
class Obstacle:
    def __init__(self):
        self.image=pygame.image.load("bush4.png")
        self.x = screenWidth
        self.y = screenHeight - obstacleHeight
        self.rect = self.image.get_rect()
        self.rect.center = (screenWidth, screenHeight - obstacleHeight )
        self.vel_x = -obstacleMovingSpeed

    def update(self):
        self.x += self.vel_x
        if self.x + obstacleWidth < 0:
            self.x = screenWidth
            self.y = random.randint(50, screenHeight - 50)

    def draw(self, screen):
        #pygame.draw.rect(screen, obstacleColor, (self.x, self.y, obstacleWidth, obstacleHeight))
        self.rect.center =(self.x, self.y)
        screen.blit(self.image, self.rect)

class Platform:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self):
        self.x -= self.speed
        if self.x + self.width < 0:
            self.x = screenWidth
            self.y = random.randint(50, screenHeight - 50)

    def draw(self, screen):
        pygame.draw.rect(screen, platformColor, (self.x, self.y, self.width, self.height))

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Character Jump")

    clock = pygame.time.Clock()

    characterRunning = Character()
    obstaclePosition = Obstacle()
    platforms = []

    background = pygame.image.load('background.png').convert()
    # create platforms
    for i in range(5):
        platform = Platform(random.randint(0, screenWidth), random.randint(50, screenHeight - 50), platformWidth, platformHeight, platformSpeed)
        platforms.append(platform)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    characterRunning.jump()

        #screen.fill(bgColor)
        screen.blit(background,(0,0))

        # draw and move platforms
        for platform in platforms:
            platform.move()
            platform.draw(screen)

        # draw and move obstaclePosition
        obstaclePosition.update()
        obstaclePosition.draw(screen)

        # see if characterRunning collides with any platform
        for platform in platforms:
            if (characterRunning.x < platform.x + platform.width and
                characterRunning.x + charWidth > platform.x and
                characterRunning.y + charHeight >= platform.y and
                characterRunning.y + charHeight <= platform.y + platform.height):
                characterRunning.on_ground = True
                characterRunning.vel_y = 0
                characterRunning.y = platform.y - charHeight

        characterRunning.update()
        characterRunning.draw(screen)

        # see if obstaclePosition catches the characterRunning
        if (characterRunning.x < obstaclePosition.x + obstacleWidth and
            characterRunning.x + charWidth > obstaclePosition.x and
            characterRunning.y < obstaclePosition.y + obstacleHeight and
           characterRunning.y + charHeight > obstaclePosition.y):
                print("Game Over")
                game_over_screen()
                running = False

        pygame.display.flip()
        clock.tick(60)

    #pygame.quit()
def game_over_screen():
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Game Over")

    clock = pygame.time.Clock()

    game_over_image = pygame.image.load("grassy_yes.png")
    restart_button_image = pygame.image.load("gamestart_button.png")
    restart_button_rect = restart_button_image.get_rect(center=(screenWidth // 2, screenHeight // 2))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    start_game()
                    #pygame.quit()
                    #sys.exit()

        screen.fill(bgColor)
        screen.blit(game_over_image, (0, 0))
        screen.blit(restart_button_image, restart_button_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

def main():
    start_game()

if __name__ == "__main__":
    main()    