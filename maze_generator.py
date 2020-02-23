import random

# Cardinal directions representation
N, S, W, E = ('n', 's', 'w', 'e')

class Cell:
    """
    Cell class containing its position and still standing neighboring walls.
    """
    def __init__(self, x, y, walls):
        self.x = x
        self.y = y
        self.walls = set(walls)

        self.target = False

    def __repr__(self):
        return f"Cell <{self.x}, {self.y}, {''.join(sorted(self.walls))}>"

    def __contains__(self, wall):
        return wall in self.walls

    def _wall_to(self, other):
        """
        Returns the direction to the given adjacent cell from the current one.
        """
        assert abs(self.x - other.x) + abs(self.y - other.y) == 1, f"{self}, {other}"

        if other.y < self.y:
            return N
        elif other.y > self.y:
            return S
        elif other.x < self.x:
            return W
        elif other.x > self.x:
            return E

    def connect(self, other):
        """
        Removes the wall between two adjacent cells.
        """
        self.walls.remove(self._wall_to(other))
        other.walls.remove(other._wall_to(self))

    def is_full(self):
        """
        Returns True if all walls are still standing.
        """
        return len(self.walls) == 4

class Maze:
    """
    Maze class containing maze generation algorithm.
    """
    def __init__(self, width=16, height=16):
        """
        Create a new maze of given size.
        """
        self.width = width
        self.height = height
        self.cells = []

        for y in range(self.height):
            for x in range(self.width):
                self.cells.append(Cell(x, y, [N, S, W, E]))

    def __getitem__(self, coords):
        """
        Returns the cell at coords = (x, y).
        """
        x, y = coords

        if 0 <= x < self.width and 0 <= y < self.height:
            # The cell is inside the maze
            return self.cells[x + y * self.width]
        else:
            return None

    def neighbors(self, cell):
        """
        Returns the list of neighboring cells (without diagonals).
        Cells on borders or corners may have less than 4 neighbors.
        """
        x = cell.x
        y = cell.y
        for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            neighbor = self[nx, ny]
            if neighbor is not None:
                yield neighbor

    def randomize(self):
        """
        Depth-First Search maze generation algorithm.

        Knocks down random walls to build a random maze.
        """
        cell_stack = []
        cell = random.choice(self.cells)
        n_visited_cells = 1

        while n_visited_cells < len(self.cells):
            neighbors = [c for c in self.neighbors(cell) if c.is_full()]

            if len(neighbors):
                neighbor = random.choice(neighbors)
                cell.connect(neighbor)
                cell_stack.append(cell)
                cell = neighbor
                n_visited_cells += 1
            else:
                cell = cell_stack.pop()

        random.choice(self.cells).target = True

    def to_string(self):
        """
        Returns a string representation of the maze matrix.
        """
        str_matrix = [['#'] * (self.width * 2 + 1) for i in range(self.height * 2 + 1)]

        for cell in self.cells:
            x = cell.x * 2 + 1
            y = cell.y * 2 + 1
            str_matrix[y][x] = '.'
            if N not in cell and y > 0:
                str_matrix[y - 1][x] = '.'
            if S not in cell and y + 1 < self.width:
                str_matrix[y + 1][x] = '.'
            if W not in cell and x > 0:
                str_matrix[y][x - 1] = '.'
            if E not in cell and x + 1 < self.width:
                str_matrix[y][x + 1] = '.'
            if cell.target:
                str_matrix[y][x] = '%'

        return '\n'.join(''.join(line) for line in str_matrix)

    @staticmethod
    def generate(width=16, height=16):
        """
        Returns a random maze of given size.
        """
        m = Maze(width, height)
        m.randomize()
        return m.to_string()

