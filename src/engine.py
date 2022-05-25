import pygame
import math

from src.wall import Wall
from src.ray import Ray
from src.constants import RENDER_QUALITY, PLAYER_FOV, PLAYER_SPEED, PLAYER_ROT_SPEED
from src.utils import clamp

def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Raycasting Engine")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Calbri", 32)


    player_pos = pygame.Vector2(400, 150)
    player_rot = 0

    # Create some rays
    # Go from -FOV/2, to +FOV/2 around players centre of POV
    rays = [Ray(player_pos.x + 12.5, player_pos.y + 12.5,
            player_rot - (math.radians(PLAYER_FOV) / 2) + 
            (i / PLAYER_FOV * RENDER_QUALITY) * (math.radians(PLAYER_FOV)))
            for i in range(PLAYER_FOV * RENDER_QUALITY)]

    ray_intersect_distances = [False for _ray in rays]

    #
    #   ---- WALLS GO IN THIS ARRAY ----
    #

    walls = [Wall(0, 0, 800, 0), Wall(0, 300, 800, 300),
            Wall(0, 0, 0, 300), Wall(800, 0, 800, 300),
            Wall(50, 50, 50, 250, (255, 0, 0)), Wall(50, 50, 100, 50, (100, 200, 200)),
            Wall(50, 70, 80, 70, (200, 200, 255))]
    
    #
    #   ---- WALLS GO IN THIS ARRAY ----
    #

    topdown_surf = pygame.Surface((800, 300))
    pov_surf = pygame.Surface((800, 300))

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        player_rot += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_ROT_SPEED

        if keys[pygame.K_w]:
            player_pos += (pygame.Vector2(math.cos(player_rot), math.sin(player_rot))
            * PLAYER_SPEED)
        if keys[pygame.K_s]:
            player_pos += (-pygame.Vector2(math.cos(player_rot), math.sin(player_rot))
            * PLAYER_SPEED)
        if keys[pygame.K_a]:
            player_pos += pygame.Vector2(math.cos(player_rot - 1.571), 
            math.sin(player_rot - 1.571)) * PLAYER_SPEED
        if keys[pygame.K_d]:
            player_pos += pygame.Vector2(math.cos(player_rot + 1.571), 
            math.sin(player_rot + 1.571)) * PLAYER_SPEED


        for i, ray in enumerate(rays):
            # Updating pos and rotation
            ray.update_pos(player_pos.x + 12.5, player_pos.y + 12.5)
            # Set angles of rays based on the centre of players view
            ray.set_angle(player_rot - (math.radians(PLAYER_FOV)/2) +
            (i/PLAYER_FOV*RENDER_QUALITY) * math.radians(PLAYER_FOV))

            # Casting
            closest = False
            closest_color = 0
            for wall in walls:
                # Cast a ray to wall
                intersect = ray.cast(wall)
                # If intersect occurs
                if intersect:
                    # Calculate distance between ray and wall
                    distance = max(math.sqrt(abs(intersect.x - ray.position.x)**2 +
                    abs(intersect.y - ray.position.y)**2), 1)
                    # Multiply by cos of angle distance to reduce "fisheye"
                    distance *= math.cos(ray.angle - player_rot) / 3
                    # If no closest data, use this as closest
                    if closest == False:
                        closest = distance
                        closest_color = wall.color
                    else:
                        # If new closest, set this as closest
                        if closest > distance:
                            closest = distance
                            closest_color = wall.color
            
            # Update this ray's data to new gathered data
            ray_intersect_distances[i] = (closest, closest_color) if closest != False else False

        # Topdown Drawing
        topdown_surf.fill(0)
        for ray in rays:
            ray.draw(topdown_surf)
        pygame.draw.rect(topdown_surf, (255, 255, 255), (player_pos, (25, 25)))
        for wall in walls:
            wall.draw(topdown_surf)

        # POV Drawing
        pov_surf.fill((100, 100, 190))
        pygame.draw.rect(pov_surf, (90, 90, 90), (0, 150, 800, 150))
        # Go through all raycast data
        for i, distance in enumerate(ray_intersect_distances):
            # If distance data available
            if distance != False:
                pygame.draw.line(pov_surf,
                # Color mapping, distance[1] is color data
                # distance[0] is distance from player data
                (clamp(distance[1][0]/distance[0] * 20, 0, distance[1][0]), 
                clamp(distance[1][1]/distance[0] * 20, 0, distance[1][1]),
                clamp(distance[1][2]/distance[0] * 20, 0, distance[1][2])),
                # Line height calculation
                (i * 800 / PLAYER_FOV * RENDER_QUALITY,
                150 - clamp(150/distance[0] * 15, 0, 150)), 
                (i * 800 / PLAYER_FOV * RENDER_QUALITY,
                150 + clamp(150/distance[0] * 15, 0, 150)),
                # Line width
                math.ceil(800 / PLAYER_FOV * RENDER_QUALITY))
        
        pov_surf.blit(font.render("FPS: " + str(int(clock.get_fps())), True, 0), (10, 10))

        # Draw surfs to window
        screen.fill(0)
        screen.blit(topdown_surf, (0, 0))
        screen.blit(pov_surf, (0, 300))

        pygame.display.update()

    pygame.quit()