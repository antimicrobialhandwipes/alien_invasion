import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

sparkles = [[random.randint(0, WIDTH),
             random.randint(0, HEIGHT),
             random.randint(1, 3)] for _ in range(100)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    for s in sparkles:
        pygame.draw.circle(screen, (255, 255, 255),
                           (s[0], s[1]), s[2])

        s[0] = s[0] + random.choice([-1, 0, 1])
        s[1] = s[1] + random.choice([-1, 0, 1])
        s[2] = random.randint(1, 3)

    pygame.display.flip()
    clock.tick(60)