from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch: 
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Check if the start is the goal
        if node.state == grid.end:
            return Solution(node, reached={node.state: True})

        # Initialize the explored dictionary to be empty
        explored = {}

        # Add the node to the explored dictionary
        explored[node.state] = True

        # Initialize the frontier with the initial node
        frontier = QueueFrontier()
        frontier.add(node)

        while not frontier.is_empty():
            # Remove a node from the frontier
            node = frontier.remove()

            # Explore all neighboring states
            for action, new_state in grid.get_neighbours(node.state).items():
                if new_state not in explored:
                    # Create a new node
                    new_node = Node(
                        "", 
                        state=new_state,
                        cost=node.cost + grid.get_cost(new_state),
                        parent=node,
                        action=action
                    )

                    # Check if it's the goal
                    if new_state == grid.end:
                        return Solution(new_node, explored)

                    # Mark as explored and add to frontier
                    explored[new_state] = True
                    frontier.add(new_node)

        # If no solution is found
        return NoSolution(explored)
    