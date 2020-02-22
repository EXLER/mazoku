import math

try:
    import pyxel
except ImportError:
    print("Error while trying to import necessary packages. Please run 'pip install -r requirements.txt' and try again!")
    raise SystemExit

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 128

MAP_WIDTH = 16
MAP_HEIGHT = 16

TEMP_MAP = """
################
#..............#
#..#....######.#
#..............#
#..............#
#......##......#
#......##......#
#..............#
###....#####...#
##.............#
#..............#
#........###.###
#........#.....#
#..............#
#........#.....#
################
"""

class Game:
    def __init__(self):
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            caption="Mazoku",
            scale=4
        )
        # pyxel.load("mazoku.pyxel")

        self.maze_map = TEMP_MAP[1:-1].split("\n")
        self.tp1 = pyxel.frame_count
        self.tp2 = pyxel.frame_count
        self.depth = 24
        self.render_alt = True
        self.show_boundaries = True
        self.show_minimap = True

        self.player_x = 7
        self.player_y = 12
        self.player_z = 4
        self.fov = math.pi / 4
        self.speed = 0.2 # Movement speed

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        self.tp2 = pyxel.frame_count
        delta_time = self.tp2 - self.tp1
        self.tp1 = self.tp2

        if pyxel.btn(pyxel.KEY_W):
            self.move_forward(delta_time)

        if pyxel.btn(pyxel.KEY_S):
            self.move_backward(delta_time)

        if pyxel.btn(pyxel.KEY_A):
            self.player_z -= 0.05 * delta_time

        if pyxel.btn(pyxel.KEY_D):
            self.player_z += 0.05 * delta_time

        if pyxel.btnp(pyxel.KEY_P):
            print(f"x: {self.player_x}")
            print(f"y: {self.player_y}")
            print(f"z: {self.player_z}")

    def draw(self):
        start = 0
        if self.render_alt:
            start = 1
        self.render_alt = not self.render_alt

        for x in range(start, SCREEN_WIDTH, 2):
            # For each column, calculate the ray angle projected
            ray_angle = (self.player_z - self.fov / 2) + (x / SCREEN_WIDTH) * self.fov

            ray_distance = 0
            ray_hit_wall = False
            ray_boundary = False

            view_x = math.sin(ray_angle)
            view_y = math.cos(ray_angle)

            while not ray_hit_wall and ray_distance < self.depth:
                ray_distance += 0.1

                # Check if ray is out of map bounds
                test_x = int(self.player_x + view_x * ray_distance)
                test_y = int(self.player_y + view_y * ray_distance)

                if test_x < 0 or test_x >= MAP_WIDTH or test_y < 0 or test_y >= MAP_HEIGHT:
                    ray_hit_wall = True
                    ray_distance = self.depth
                else:
                    # Ray is still inside map space, check if the ray cell is a wall
                    if self.maze_map[test_y][test_x] == "#":
                        ray_hit_wall = True

                        # Cast rays from each wall corner to find boundaries
                        wall_rays = []
                        for wx in range(2):
                            for wy in range(2):
                                vx = test_x + wx - self.player_x
                                vy = test_y + wy - self.player_y
                                d = math.sqrt(vx**2 + vy**2)
                                dot = (view_x * vx / d) + (view_y * vy / d)
                                wall_rays.append((d, dot))

                        # Sort to find the closest
                        wall_rays.sort()

                        # Look for small angles with closest corners
                        bound = 0.01
                        if math.acos(wall_rays[0][1]) < bound or math.acos(wall_rays[1][1]) < bound:
                            ray_boundary = True
                                
            # Calculate distances to ceiling and floor
            ceiling = SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / ray_distance
            floor = SCREEN_HEIGHT - ceiling

            # Using Pyxel image bank as display buffer
            shade = 0
            for y in range(SCREEN_HEIGHT):
                if y < ceiling:
                    pyxel.image(1).set(x, y, 0)
                elif y > ceiling and y <= floor:
                    # Compute wall shading
                    if ray_distance <= self.depth / 7:
                        shade = 6
                    elif ray_distance < self.depth / 6:
                        if x % 2:
                            shade = 6 if y % 2 else 13
                        else:
                            shade = 13 if y % 2 else 6
                    elif ray_distance < self.depth / 5:
                        shade = 13
                    elif ray_distance < self.depth / 4:
                        if x % 2:
                            shade = 13 if y % 2 else 1
                        else:
                            shade = 1 if y % 2 else 13
                    elif ray_distance < self.depth / 3:
                        shade = 1
                    elif ray_distance < self.depth / 2:
                        if x % 2:
                            shade = 1 if y % 2 else 0
                        else:
                            shade = 0 if y % 2 else 1
                    elif ray_distance < self.depth:
                        shade = 0

                    # Change the shade of boundary between walls
                    if self.show_boundaries and ray_boundary:
                        shade = 0

                    pyxel.image(1).set(x, y, shade)
                else:
                    # Compute floor shading
                    b = 1 - (y - SCREEN_HEIGHT / 2) / (SCREEN_HEIGHT / 2)
                    if b < 0.25:
                        shade = 14
                    elif b < 0.5:
                        if x % 2:
                            shade = 14 if y % 2 else 2
                        else:
                            shade = 2 if y % 2 else 14
                    elif b < 0.75:
                        shade = 2
                    elif b < 0.9:
                        if x % 2:
                            shade = 2 if y % 2 else 0
                        else:
                            shade = 0 if y % 2 else 2
                    else:
                        shade = 0

                    pyxel.image(1).set(x, y, shade)

        # Copy the screen from the image bank
        pyxel.blt(0, 0, 1, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Draw minimap
        if self.show_minimap:
            startx = 0
            starty = SCREEN_HEIGHT - MAP_WIDTH * 2
            for nx in range(MAP_HEIGHT):
                for ny in range(MAP_WIDTH):
                    cell = self.maze_map[ny][nx]
                    if cell == "#":
                        col = 6
                    else:
                        col = 7
                    pyxel.rect(
                        nx * 2 + startx,
                        ny * 2 + starty,
                        2, 2, col
                    )
            px = int(self.player_x)
            py = int(self.player_y)
            pyxel.rect(
                px * 2 + startx,
                py * 2 + starty,
                2, 2, 12
            )


    def move_forward(self, delta_time):
        new_x = self.player_x + math.sin(self.player_z) * self.speed * delta_time
        new_y = self.player_y + math.cos(self.player_z) * self.speed * delta_time
        
        if not self.collides(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y

    def move_backward(self, delta_time):
        new_x = self.player_x - math.sin(self.player_z) * self.speed * delta_time
        new_y = self.player_y - math.cos(self.player_z) * self.speed * delta_time
        
        if not self.collides(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y

    def collides(self, x, y):
        return self.maze_map[int(y)][int(x)] == "#"


if __name__ == "__main__":
    game = Game()
    game.run()