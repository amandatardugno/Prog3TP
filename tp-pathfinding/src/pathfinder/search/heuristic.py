from ..models.node import Node
from ..models.grid import Grid

class Heuristic:
    def manhattan(self, node: Node, grid: Grid) -> float:
        return abs(node.state[0] - grid.end[0]) + abs(node.state[1] - grid.end[1])

    def euclidean(self, node: Node, grid: Grid) -> float:
        dx = node.state[0] - grid.end[0]
        dy = node.state[1] - grid.end[1]
        return (dx ** 2 + dy ** 2) ** 0.5
