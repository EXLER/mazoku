import random
from enum import StrEnum
from typing import Generator, Iterable, Self


class Direction(StrEnum):
    """
    Enum class for the four cardinal directions.
    """

    N = "n"
    S = "s"
    W = "w"
    E = "e"


class Cell:
    """
    Cell class containing its position and still standing neighboring walls.
    """

    @property
    def is_full(self: Self) -> bool:
        """
        Returns True if all walls are still standing.
        """

        return len(self.walls) == 4

    def __init__(self: Self, x: int, y: int, walls: Iterable[Direction]) -> None:
        self.x = x
        self.y = y
        self.walls = set(walls)

        self.target = False

    def __repr__(self: Self) -> str:
        return f"Cell <{self.x}, {self.y}, {''.join(sorted(self.walls))}>"

    def __contains__(self: Self, wall: Direction) -> bool:
        return wall in self.walls

    def _wall_to(self: Self, other: Self) -> Direction:
        """
        Returns the direction to the given adjacent cell from the current one.
        """

        if abs(self.x - other.x) + abs(self.y - other.y) != 1:
            raise ValueError("Cells are not adjacent")  # noqa: TRY003

        if other.y < self.y:
            return Direction.N
        elif other.y > self.y:
            return Direction.S
        elif other.x < self.x:
            return Direction.W
        else:
            return Direction.E

    def connect(self: Self, other: Self) -> None:
        """
        Removes the wall between two adjacent cells.
        """

        self.walls.remove(self._wall_to(other))
        other.walls.remove(other._wall_to(self))


class Maze:
    """
    Maze container containing maze generation algorithm.
    """

    def __init__(self: Self, width: int = 16, height: int = 16) -> None:
        """
        Create a new maze of given size.
        """
        self.width = width
        self.height = height
        self.cells = []

        for y in range(self.height):
            for x in range(self.width):
                self.cells.append(Cell(x, y, [Direction.N, Direction.S, Direction.W, Direction.E]))

    def __getitem__(self: Self, coords: tuple[int, int]) -> Cell | None:
        """
        Returns the cell at coords = (x, y).
        """

        x, y = coords

        if 0 <= x < self.width and 0 <= y < self.height:
            # The cell is inside the maze
            return self.cells[x + y * self.width]
        else:
            return None

    def neighbors(self: Self, cell: Cell) -> Generator[Cell, None, None]:
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

    def randomize(self: Self) -> None:
        """
        Depth-First Search maze generation algorithm.

        Knocks down random walls to build a random maze.
        """
        cell_stack = []
        cell = random.choice(self.cells)  # noqa: S311
        n_visited_cells = 1

        while n_visited_cells < len(self.cells):
            neighbors = [c for c in self.neighbors(cell) if c.is_full]

            if len(neighbors):
                neighbor = random.choice(neighbors)  # noqa: S311
                cell.connect(neighbor)
                cell_stack.append(cell)
                cell = neighbor
                n_visited_cells += 1
            else:
                cell = cell_stack.pop()

        random.choice(self.cells).target = True  # noqa: S311

    def to_string(self: Self) -> str:
        """
        Returns a string representation of the maze matrix.
        """
        str_matrix = [["#"] * (self.width * 2 + 1) for i in range(self.height * 2 + 1)]

        for cell in self.cells:
            x = cell.x * 2 + 1
            y = cell.y * 2 + 1
            str_matrix[y][x] = "."
            if Direction.N not in cell and y > 0:
                str_matrix[y - 1][x] = "."
            if Direction.S not in cell and y + 1 < self.width:
                str_matrix[y + 1][x] = "."
            if Direction.W not in cell and x > 0:
                str_matrix[y][x - 1] = "."
            if Direction.E not in cell and x + 1 < self.width:
                str_matrix[y][x + 1] = "."
            if cell.target:
                str_matrix[y][x] = "%"

        return "\n".join("".join(line) for line in str_matrix)

    @staticmethod
    def generate(width: int = 16, height: int = 16) -> str:
        """
        Returns a string representation of a random maze of given size.
        """
        m = Maze(width, height)
        m.randomize()
        return m.to_string()
