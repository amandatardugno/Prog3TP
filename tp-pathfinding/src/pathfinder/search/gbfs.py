from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from .heuristic import Heuristic


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        node = Node("", grid.start, 0)
        heuristic = Heuristic()  # instancia de la clase

        if node.state == grid.end:
            return Solution(node, reached={node.state: True})

        frontier = PriorityQueueFrontier()
        frontier.add(node, priority=int(heuristic.manhattan(node, grid)))

        reached = {node.state: True}

        while frontier.frontier:
            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, reached)

            for action, new_state in grid.get_neighbours(node.state).items():
                if new_state not in reached:
                    new_node = Node(
                        "", 
                        state=new_state,
                        cost=node.cost + grid.get_cost(new_state),
                        parent=node,
                        action=action
                    )
                    reached[new_state] = True
                    frontier.add(new_node, priority=int(heuristic.manhattan(new_node, grid)))

        return NoSolution(reached)
