from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        node = Node("", grid.start, 0)

        if node.state == grid.end:
            return Solution(node, reached={node.state: True})

        explored = {} 
        
        explored[node.state] = True

        frontier = StackFrontier()
        frontier.add(node)

        while not frontier.is_empty():
            node = frontier.remove()

            for action, new_state in grid.get_neighbours(node.state).items():
                if new_state not in explored:
                    new_node = Node(
                        "", 
                        state=new_state,
                        cost=node.cost + grid.get_cost(new_state),
                        parent=node,
                        action=action
                    )

                    if new_state == grid.end:
                        return Solution(new_node, explored)

                    explored[new_state] = True
                    frontier.add(new_node)

        return NoSolution(explored)

