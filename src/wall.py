import pygame

class Wall:
    def __init__(self, x1, y1, x2, y2, color=(255, 255, 0)):
        self.point_one = pygame.Vector2(x1, y1)
        self.point_two = pygame.Vector2(x2, y2)
        self.color = color
    
    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.point_one, self.point_two, 2)
