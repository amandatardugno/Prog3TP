from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        node = Node("", grid.start, 0)

        if node.state == grid.end:
            return Solution(node, reached={node.state: 0})

        frontier = PriorityQueueFrontier()
        frontier.add(node, priority=0)

        explored = {node.state: 0}

        while frontier.frontier:
            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, explored)

            for action, new_state in grid.get_neighbours(node.state).items():
                new_cost = node.cost + grid.get_cost(new_state)

                if new_state not in explored or new_cost < explored[new_state]:
                    explored[new_state] = new_cost
                    new_node = Node(
                        "",
                        state=new_state,
                        cost=new_cost,
                        parent=node,
                        action=action
                    )
                    frontier.add(new_node, priority=new_cost)

        return NoSolution(explored)
