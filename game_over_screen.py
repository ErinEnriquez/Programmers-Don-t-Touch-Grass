import pygame
import sys
#from pygameerin import start_game

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)

def game_over_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Over")

    clock = pygame.time.Clock()

    game_over_image = pygame.image.load("grassy_yes.png")
    restart_button_image = pygame.image.load("gamestart_button.png")
    restart_button_rect = restart_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

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

        screen.fill(BACKGROUND_COLOR)
        screen.blit(game_over_image, (0, 0))
        screen.blit(restart_button_image, restart_button_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

#if __name__ == "__main__":
#    game_over_screen()