
def construct_map():

    from src.map.map_colormap import MAP_COLORS
    from src.wall import Wall

    walls = []

    with open("src/map/map_data.raymap", "r") as file:
        map_data = file.read().splitlines()
    
    for i_line, line in enumerate(map_data):
        for i_char, char in enumerate(line):
            if char != "0":

                wall_1 = Wall(i_char * 20, i_line * 20, 
                i_char * 20 + 20, i_line * 20, MAP_COLORS[char])

                wall_2 = Wall(i_char * 20, i_line * 20, 
                i_char * 20, i_line * 20 + 20, MAP_COLORS[char])

                wall_3 = Wall(i_char * 20, i_line * 20 + 20, 
                i_char * 20 + 20, i_line * 20 + 20, MAP_COLORS[char])

                wall_4 = Wall(i_char * 20 + 20, i_line * 20, 
                i_char * 20 + 20, i_line * 20 + 20, MAP_COLORS[char])

                walls += [wall_1, wall_2, wall_3, wall_4]
    
    for wall in walls:
        test_walls = walls.copy()
        test_walls.remove(wall)
        for test_wall in test_walls:
            if (wall.point_one.x == test_wall.point_one.x and
                wall.point_one.y == test_wall.point_one.y and
                wall.point_two.x == test_wall.point_two.x and
                wall.point_two.y == test_wall.point_two.y):
                walls.remove(test_wall)
    
    return walls
