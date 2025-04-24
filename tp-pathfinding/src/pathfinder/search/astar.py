from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from .heuristic import Heuristic


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        node = Node("", grid.start, 0)
        heuristic = Heuristic()  # instancia de la clase

        if node.state == grid.end:
            return Solution(node, reached={node.state: 0})

        frontier = PriorityQueueFrontier()
        f_cost = node.cost + heuristic.manhattan(node, grid)
        frontier.add(node, priority=int(f_cost))

        reached = {node.state: node.cost}

        while frontier.frontier:
            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, reached)

            for action, new_state in grid.get_neighbours(node.state).items():
                g_cost = node.cost + grid.get_cost(new_state)

                if new_state not in reached or g_cost < reached[new_state]:
                    reached[new_state] = g_cost
                    new_node = Node(
                        "",
                        state=new_state,
                        cost=g_cost,
                        parent=node,
                        action=action
                    )
                    f_cost = g_cost + heuristic.manhattan(new_node, grid)
                    frontier.add(new_node, priority=int(f_cost))

        return NoSolution(reached)