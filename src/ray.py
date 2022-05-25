import pygame
import math

class Ray:
    def __init__(self, x, y, angle):
        self.position = pygame.Vector2(x, y)
        self.direction = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.angle = angle
        self.last_cast = pygame.Vector2()
    
    def update_pos(self, new_x, new_y):
        self.position.x = new_x
        self.position.y = new_y

    def set_angle(self, angle):
        self.direction = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.angle = angle

    def draw(self, screen):
        pygame.draw.line(screen, (170, 170, 170), self.position, 
        self.last_cast)

    def cast(self, wall):
        # Line intersection formula
        x1 = wall.point_one.x
        y1 = wall.point_one.y
        x2 = wall.point_two.x
        y2 = wall.point_two.y

        x3 = self.position.x
        y3 = self.position.y
        x4 = self.position.x + self.direction.x
        y4 = self.position.y + self.direction.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return False

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        # If intersection
        if t > 0 and t < 1 and u > 0:
            # Calculate point of intersection and return
            intersect = pygame.Vector2()
            intersect.x = x1 + t * (x2 - x1)
            intersect.y = y1 + t * (y2 - y1)
            return intersect
		
        return False
