import pygame
import random


pygame.init()
# Constants
screenWidth = 800                   
screenHeight = 600

window = pygame.display.set_mode(((screenWidth, screenHeight)))
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
background = pygame.image.load('background.png')       
obstacle = pygame.image.load('bush.png')         
              
class Character:
    def __init__(self):
        self.x = screenWidth // 2 - charWidth // 2
        self.y = screenHeight - charHeight
        self.vel_y = 0
        self.on_ground = True
        self.jump_power = 0             
 
    def jump(self):
        if self.on_ground:
            self.jump_power = 15  # Initial jump power
            self.on_ground = False
            self.vely = 0


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
        pygame.draw.rect(screen, charColor, (self.x, self.y, charWidth, charHeight))

class Obstacle:
    def __init__(self):
        self.x = screenWidth
        self.y = screenHeight - obstacleHeight
        self.vel_x = -obstacleMovingSpeed

    def update(self):
        self.x += self.vel_x
        if self.x + obstacleWidth < 0:
            self.x = screenWidth
            self.y = random.randint(50, screenHeight - 50)

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Character Jump")

    clock = pygame.time.Clock()

    characterRunning = Character()
    obstaclePosition = Obstacle()
    platforms = []

    # Generate initial platforms
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

        screen.fill(bgColor)

        # Draw and move platforms
        for platform in platforms:
            platform.move()
            platform.draw(screen)

        # Draw and move obstaclePosition
        obstaclePosition.update()
        obstaclePosition.draw(screen)

        # Check if characterRunning collides with any platform
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

        # Check if obstaclePosition catches the characterRunning
        if (characterRunning.x < obstaclePosition.x + obstacleWidth and
            characterRunning.x + charWidth > obstaclePosition.x and
            characterRunning.y < obstaclePosition.y + obstacleHeight and
            characterRunning.y + charHeight > obstaclePosition.y):
            print("Game Over")
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()    